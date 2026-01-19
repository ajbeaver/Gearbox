import time
import requests

def evaluate_chain(chain_name, chain_cfg):
    network_name = chain_cfg.get("default_network")
    networks = chain_cfg.get("networks", {})

    if not network_name or network_name not in networks:
        return {
            "chain": chain_name,
            "network": None,
            "rpc": None,
            "reachable": False,
            "timestamp": int(time.time()),
            "error": "default_network missing or invalid",
        }

    network_cfg = networks[network_name]

    rpc_endpoints = network_cfg.get("rpc_endpoints", [])
    if not rpc_endpoints:
        return {
            "chain": chain_name,
            "network": network_name,
            "rpc": None,
            "reachable": False,
            "timestamp": int(time.time()),
            "error": "no rpc_endpoints configured",
        }

    rpc = rpc_endpoints[0]

    try:
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_chainId",
            "params": [],
            "id": 1,
        }

        response = requests.post(rpc, json=payload, timeout=5)
        response.raise_for_status()

        data = response.json()
        if "result" not in data:
            raise ValueError("invalid RPC response")

        return {
            "chain": chain_name,
            "network": network_name,
            "rpc": rpc,
            "reachable": True,
            "timestamp": int(time.time()),
            "error": None,
        }

    except Exception as e:
        return {
            "chain": chain_name,
            "network": network_name,
            "rpc": rpc,
            "reachable": False,
            "timestamp": int(time.time()),
            "error": str(e),
        }
