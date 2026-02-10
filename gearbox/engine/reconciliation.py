def reconcile(chain_snapshot: dict, oracle_snapshot: dict, cfg: dict) -> dict:
    max_time_skew_sec = cfg.get("max_time_skew_sec")

    chain_epoch = chain_snapshot.get("timestamp_epoch")
    oracle_epoch = oracle_snapshot.get("timestamp_epoch")

    if (
        max_time_skew_sec is None
        or not isinstance(max_time_skew_sec, int)
        or chain_epoch is None
        or oracle_epoch is None
    ):
        return {
            "chain_timestamp_epoch": chain_epoch,
            "oracle_timestamp_epoch": oracle_epoch,
            "delta_sec": None,
            "status": "degraded",
            "reason": "missing_timestamp_epoch",
        }

    delta_sec = abs(oracle_epoch - chain_epoch)
    if delta_sec <= max_time_skew_sec:
        return {
            "chain_timestamp_epoch": chain_epoch,
            "oracle_timestamp_epoch": oracle_epoch,
            "delta_sec": delta_sec,
            "status": "ok",
        }

    return {
        "chain_timestamp_epoch": chain_epoch,
        "oracle_timestamp_epoch": oracle_epoch,
        "delta_sec": delta_sec,
        "status": "degraded",
        "reason": "oracle_time_skew",
    }
