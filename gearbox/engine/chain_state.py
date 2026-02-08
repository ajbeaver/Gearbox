import datetime
import requests


def _rpc_call(rpc, method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }

    response = requests.post(rpc, json=payload, timeout=5)
    response.raise_for_status()

    data = response.json()
    if "result" not in data:
        raise ValueError("invalid RPC response")

    return data["result"]


def collect_chain_orientation(chain_name, chain_cfg):
    network_name = chain_cfg.get("default_network")
    networks = chain_cfg.get("networks", {})

    observed_at = datetime.datetime.now().isoformat()

    snapshot = {
        "chain": chain_name,
        "network": network_name,
        "rpc": None,
        "block_height_or_slot": None,
        "block_timestamp": None,
        "observed_at": observed_at,
        "success": False,
        "failure_reason": None,
    }

    if not network_name or network_name not in networks:
        snapshot["failure_reason"] = "eth_chainId"
        return snapshot

    network_cfg = networks[network_name]
    rpc_endpoints = network_cfg.get("rpc_endpoints", [])

    if not rpc_endpoints:
        snapshot["failure_reason"] = "eth_chainId"
        return snapshot

    rpc = rpc_endpoints[0]
    snapshot["rpc"] = rpc

    try:
        _rpc_call(rpc, "eth_chainId", [])
    except Exception:
        snapshot["failure_reason"] = "eth_chainId"
        return snapshot

    try:
        block_number_hex = _rpc_call(rpc, "eth_blockNumber", [])
    except Exception:
        snapshot["failure_reason"] = "eth_blockNumber"
        return snapshot

    try:
        block = _rpc_call(rpc, "eth_getBlockByNumber", ["latest", False])
        if not isinstance(block, dict) or "timestamp" not in block:
            raise ValueError("invalid block response")
        block_timestamp_hex = block["timestamp"]
    except Exception:
        snapshot["failure_reason"] = "eth_getBlockByNumber"
        return snapshot

    snapshot["block_height_or_slot"] = int(block_number_hex, 16)
    snapshot["block_timestamp"] = int(block_timestamp_hex, 16)
    snapshot["success"] = True

    return snapshot
