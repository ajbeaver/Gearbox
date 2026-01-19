import os
import time
import datetime
import sys
import logging
import argparse
from pathlib import Path
from gearbox.validate import validate
from gearbox.engine.market_data import evaluate_chain

BANNER = r"""
#########################################################
                              __                       
                             /\ \                      
   __      __     __     _ __\ \ \____    ___   __  _  
 /'_ `\  /'__`\ /'__`\  /\`'__\ \ '__`\  / __`\/\ \/'\ 
/\ \L\ \/\  __//\ \L\.\_\ \ \/ \ \ \L\ \/\ \L\ \/>  </ 
\ \____ \ \____\ \__/.\_\\ \_\  \ \_,__/\ \____//\_/\_\
 \/___L\ \/____/\/__/\/_/ \/_/   \/___/  \/___/ \//\/_/
   /\____/
   \_/__/

#########################################################
"""

# Constants
VERSION = "0.2.0"
LOGDIR = "./logs"
CONFIGDIR = "./config"

# Exit Codes
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_LOGDIR_MISSING = 2
EXIT_CONFIG_MISSING = 3
EXIT_INVALID_ARGS = 4
EXIT_VALIDATION_FAILED = 5

class GearboxArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"[!] Invalid arguments: {message}")
        sys.exit(EXIT_INVALID_ARGS)

# Argument Parsing
def parse_args():
    parser = GearboxArgumentParser(
        description=(
            "Gearbox is a deterministic trading automation framework that enforces "
            "explicit risk boundaries and refuses unsafe execution."
        ),
        epilog=(
            "Developed by Offband\n"
            "Documentation: https://offband.dev/gearbox"
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Gearbox {VERSION}"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate configuration files and exit"
    )
    return parser.parse_args()

# Functions
def get_run_timestamp():
    return datetime.datetime.now().strftime("%m%d%y%H%M")

def print_banner():
    print(BANNER.rstrip())
    print(f"Version: {VERSION}\n")

def initialize():
    logging.info("Initialization started")
    if not os.path.exists(os.path.expanduser(LOGDIR)):
        logging.info(f"Log directory not found, creating: {LOGDIR}")
        try:
            os.makedirs(os.path.expanduser(LOGDIR))
        except Exception as e:
            logging.error(f"Failed to create log directory: {e}")
            print(f"[!]Failed to create log directory at {LOGDIR}.")
            sys.exit(EXIT_LOGDIR_MISSING)

    if not os.path.exists(os.path.expanduser(CONFIGDIR)):
        logging.error(f"Configuration directory missing at {CONFIGDIR}")
        print(f"[!]Configuration directory not found at {CONFIGDIR}.")
        print("[!]Gearbox will not run without explicit configuration.")
        print("[!]Create this directory and define risk limits before continuing.")
        sys.exit(EXIT_CONFIG_MISSING)

    logging.info("Initialization complete")

def run(validated_config):
    runtime_cfg = validated_config["parsed"]["runtime.yaml"]["runtime"]

    evaluation_interval = runtime_cfg["evaluation_interval_sec"]
    max_runtime = runtime_cfg["max_runtime_sec"]

    runtime_state = {
        "start_time": datetime.datetime.now(),
        "tick_count": 0,
        "last_tick_time": None,
    }

    logging.info("Runtime loop started")

    while True:
        now = datetime.datetime.now()
        runtime_state["tick_count"] += 1
        runtime_state["last_tick_time"] = now

        elapsed = (now - runtime_state["start_time"]).total_seconds()

        logging.info(
            f"Heartbeat | tick={runtime_state['tick_count']} | elapsed={int(elapsed)}s | interval={evaluation_interval}s"
        )

        logging.info("Evaluation phase started")

        allowed_chains = runtime_cfg.get("allowed_chains", [])
        chain_defs = validated_config["parsed"]["chain.yaml"]["chains"]

        for chain_name in allowed_chains:
            if chain_name not in chain_defs:
                logging.warning(
                    f"Allowed chain '{chain_name}' not found in chain.yaml"
                )
                continue

            result = evaluate_chain(chain_name, chain_defs[chain_name])

            if result["reachable"]:
                logging.info(f"Chain reachable: {result}")
            else:
                logging.warning(f"Chain unreachable: {result}")

        logging.info("Evaluation phase complete")

        if max_runtime > 0 and elapsed >= max_runtime:
            logging.info("Max runtime reached, exiting runtime loop")
            print("[+] Max runtime reached, exiting.")
            break

        try:
            time.sleep(evaluation_interval)
        except KeyboardInterrupt:
            logging.info("Runtime interrupted by user")
            print("[!] Runtime interrupted by user.")
            break

    logging.info("Runtime exited cleanly")

def main():
    args = parse_args()

    run_timestamp = get_run_timestamp()
    logfile = os.path.join(LOGDIR, f"cli-{run_timestamp}.log")

    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    if args.verbose:
        console = logging.StreamHandler(sys.stderr)
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        ))
        logging.getLogger().addHandler(console)

    print_banner()
    logging.info("CLI startup")
    print(f"[+] Log file: {logfile}")

    initialize()

    logging.info("Starting configuration validation")
    validation_result = validate(Path(CONFIGDIR))

    for err in validation_result["errors"]:
        logging.error(err)
        if args.verbose:
            print(f"[!] {err}")

    if not validation_result["ok"]:
        logging.error("Configuration validation failed")
        print("[!] Configuration validation failed. See log for details.")
        return EXIT_VALIDATION_FAILED

    logging.info("Configuration validation passed")

    if args.validate:
        print("[+] Configuration validation passed.")
        return EXIT_OK

    print("[+] Gearbox initialized and validated successfully.")

    run(validation_result)

    return EXIT_OK

# Main Execution
if __name__ == "__main__":
    sys.exit(main())