import datetime
import time
import requests
from email.utils import parsedate_to_datetime


def _format_utc_z(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=None).isoformat() + "Z"


def _parse_http_date(date_header: str):
    if not date_header:
        return None
    try:
        parsed = parsedate_to_datetime(date_header)
    except Exception:
        return None
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed.astimezone(datetime.timezone.utc)


def collect_oracle_snapshot(oracle_cfg: dict) -> dict:
    provider = oracle_cfg.get("provider")
    endpoint_url = oracle_cfg.get("endpoint_url")
    asset_pair = oracle_cfg.get("asset_pair")
    timeout_sec = oracle_cfg.get("timeout_sec", 5)

    observed_at = _format_utc_z(datetime.datetime.utcnow())

    snapshot = {
        "asset": asset_pair,
        "price": None,
        "source": provider,
        "observed_at": observed_at,
        "source_timestamp": observed_at,
        "latency_ms": None,
        "success": False,
        "failure_reason": None,
    }

    if not endpoint_url or "{asset_pair}" not in endpoint_url:
        snapshot["failure_reason"] = "invalid_endpoint_url"
        return snapshot

    if not asset_pair:
        snapshot["failure_reason"] = "missing_asset_pair"
        return snapshot

    url = endpoint_url.format(asset_pair=asset_pair)

    start = time.monotonic()
    try:
        response = requests.get(url, timeout=timeout_sec)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        end = time.monotonic()
        snapshot["latency_ms"] = int((end - start) * 1000)
        snapshot["failure_reason"] = str(e)
        return snapshot

    end = time.monotonic()
    snapshot["latency_ms"] = int((end - start) * 1000)

    date_header = response.headers.get("Date")
    parsed_date = _parse_http_date(date_header)
    if parsed_date is not None:
        snapshot["source_timestamp"] = _format_utc_z(parsed_date)

    try:
        price = data["data"]["amount"]
    except Exception:
        snapshot["failure_reason"] = "missing_price"
        return snapshot

    if not isinstance(price, str):
        snapshot["failure_reason"] = "invalid_price_type"
        return snapshot

    snapshot["price"] = price
    snapshot["success"] = True
    return snapshot
