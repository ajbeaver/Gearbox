import yaml

def validate(config_dir):
    errors = []
    required_files = [
        "risk.yaml",
        "runtime.yaml",
        "strategies.yaml",
        "chain.yaml",
        "oracle.yaml",
    ]

    parsed = {}

    for filename in required_files:
        path = config_dir / filename
        if not path.exists():
            errors.append(f"Missing config file: {filename}")
            continue
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            errors.append(f"Invalid YAML syntax in {filename}: {e}")
            continue
        parsed[filename] = data

    if "risk.yaml" in parsed:
        data = parsed["risk.yaml"]
        if not isinstance(data, dict):
            errors.append("risk.yaml must contain a YAML mapping at the top level")
        elif "risk" not in data:
            errors.append("risk.yaml missing required top-level key: 'risk'")
        else:
            risk = data["risk"]

            required_fields = {
                "max_drawdown_pct": (int, float),
                "daily_loss_pct": (int, float),
                "max_trade_loss_pct": (int, float),
                "max_position_pct": (int, float),
                "max_concurrent_positions": int,
            }

            for field, expected_type in required_fields.items():
                if field not in risk:
                    errors.append(f"risk.yaml missing required field: '{field}'")
                elif not isinstance(risk[field], expected_type):
                    errors.append(
                        f"risk.yaml field '{field}' must be of type {expected_type}"
                    )

    if "runtime.yaml" in parsed:
        data = parsed["runtime.yaml"]
        if not isinstance(data, dict):
            errors.append("runtime.yaml must contain a YAML mapping at the top level")
        elif "runtime" not in data:
            errors.append("runtime.yaml missing required top-level key: 'runtime'")
        else:
            runtime = data["runtime"]

            required_fields = {
                "mode": str,
                "execution_enabled": bool,
                "allowed_chains": list,
                "min_expected_gain_pct": (int, float),
                "respect_fees": bool,
                "allow_discovery": bool,
                "allow_strategy_switching": bool,
                "evaluation_interval_sec": int,
                "max_runtime_sec": int,
                "strict_validation": bool,
            }

            for field, expected_type in required_fields.items():
                if field not in runtime:
                    errors.append(f"runtime.yaml missing required field: '{field}'")
                elif not isinstance(runtime[field], expected_type):
                    errors.append(
                        f"runtime.yaml field '{field}' must be of type {expected_type}"
                    )

    if "strategies.yaml" in parsed:
        data = parsed["strategies.yaml"]
        if not isinstance(data, dict):
            errors.append("strategies.yaml must contain a YAML mapping at the top level")
        elif "strategies" not in data:
            errors.append("strategies.yaml missing required top-level key: 'strategies'")
        else:
            strategies = data["strategies"]

            required_fields = {
                "allowed_classes": list,
                "allowed_horizons": list,
                "switching": dict,
                "data_sources": dict,
            }

            for field, expected_type in required_fields.items():
                if field not in strategies:
                    errors.append(f"strategies.yaml missing required field: '{field}'")
                elif not isinstance(strategies[field], expected_type):
                    errors.append(
                        f"strategies.yaml field '{field}' must be of type {expected_type}"
                    )

            if "switching" in strategies and isinstance(strategies["switching"], dict):
                switching = strategies["switching"]

                switching_fields = {
                    "min_dwell_time_sec": int,
                    "max_switches_per_day": int,
                }

                for field, expected_type in switching_fields.items():
                    if field not in switching:
                        errors.append(
                            f"strategies.yaml switching missing required field: '{field}'"
                        )
                    elif not isinstance(switching[field], expected_type):
                        errors.append(
                            f"strategies.yaml switching field '{field}' must be of type {expected_type}"
                        )

            if "data_sources" in strategies and isinstance(strategies["data_sources"], dict):
                data_sources = strategies["data_sources"]

                data_source_fields = {
                    "allow_price_data": bool,
                    "allow_volume_data": bool,
                    "allow_onchain_data": bool,
                    "allow_external_sentiment": bool,
                }

                for field, expected_type in data_source_fields.items():
                    if field not in data_sources:
                        errors.append(
                            f"strategies.yaml data_sources missing required field: '{field}'"
                        )
                    elif not isinstance(data_sources[field], expected_type):
                        errors.append(
                            f"strategies.yaml data_sources field '{field}' must be of type {expected_type}"
                        )

    if "chain.yaml" in parsed:
        data = parsed["chain.yaml"]
        if not isinstance(data, dict):
            errors.append("chain.yaml must contain a YAML mapping at the top level")
        elif "chains" not in data:
            errors.append("chain.yaml missing required top-level key: 'chains'")
        else:
            chains = data["chains"]
            if not isinstance(chains, dict):
                errors.append("chain.yaml 'chains' must be a mapping")
            else:
                for chain_name, chain_cfg in chains.items():
                    if not isinstance(chain_cfg, dict):
                        errors.append(f"chain.yaml chain '{chain_name}' must be a mapping")
                        continue

                    required_chain_fields = {
                        "description": str,
                        "default_network": str,
                        "networks": dict,
                    }

                    for field, expected_type in required_chain_fields.items():
                        if field not in chain_cfg:
                            errors.append(
                                f"chain.yaml chain '{chain_name}' missing required field: '{field}'"
                            )
                        elif not isinstance(chain_cfg[field], expected_type):
                            errors.append(
                                f"chain.yaml chain '{chain_name}' field '{field}' must be of type {expected_type}"
                            )

                    networks = chain_cfg.get("networks")
                    if isinstance(networks, dict):
                        for net_name, net_cfg in networks.items():
                            if not isinstance(net_cfg, dict):
                                errors.append(
                                    f"chain.yaml chain '{chain_name}' network '{net_name}' must be a mapping"
                                )
                                continue

                            if "description" not in net_cfg or not isinstance(net_cfg["description"], str):
                                errors.append(
                                    f"chain.yaml chain '{chain_name}' network '{net_name}' missing or invalid 'description'"
                                )

                            if "rpc_endpoints" not in net_cfg or not isinstance(net_cfg["rpc_endpoints"], list):
                                errors.append(
                                    f"chain.yaml chain '{chain_name}' network '{net_name}' missing or invalid 'rpc_endpoints'"
                                )

                            if not (
                                ("chain_id" in net_cfg and isinstance(net_cfg["chain_id"], int)) or
                                ("cluster" in net_cfg and isinstance(net_cfg["cluster"], str))
                            ):
                                errors.append(
                                    f"chain.yaml chain '{chain_name}' network '{net_name}' must define 'chain_id' (int) or 'cluster' (str)"
                                )

    if "oracle.yaml" in parsed:
        data = parsed["oracle.yaml"]
        if not isinstance(data, dict):
            errors.append("oracle.yaml must contain a YAML mapping at the top level")
        elif "oracle" not in data:
            errors.append("oracle.yaml missing required top-level key: 'oracle'")
        else:
            oracle = data["oracle"]
            if not isinstance(oracle, dict):
                errors.append("oracle.yaml 'oracle' must be a mapping")
            else:
                required_fields = {
                    "provider": str,
                    "endpoint_url": str,
                    "asset_pair": str,
                    "timeout_sec": int,
                }

                for field, expected_type in required_fields.items():
                    if field not in oracle:
                        errors.append(f"oracle.yaml missing required field: '{field}'")
                    elif not isinstance(oracle[field], expected_type):
                        errors.append(
                            f"oracle.yaml field '{field}' must be of type {expected_type}"
                        )

                provider = oracle.get("provider")
                if provider is not None and provider != "coinbase":
                    errors.append("oracle.yaml field 'provider' must be 'coinbase'")

                endpoint_url = oracle.get("endpoint_url")
                if isinstance(endpoint_url, str) and "{asset_pair}" not in endpoint_url:
                    errors.append(
                        "oracle.yaml field 'endpoint_url' must include '{asset_pair}'"
                    )

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "parsed": parsed,
    }
