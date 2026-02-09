

# Gearbox

Gearbox is a configuration‑driven, CLI‑based trading system skeleton focused on
**determinism, safety, and observability**.

At this stage, Gearbox does **not trade**.  
It validates configuration, runs a governed runtime loop, and performs
read‑only market observation against real blockchains.

The goal of this phase is to prove that:
• configuration is the single source of truth  
• runtime control flow is deterministic  
• engines are isolated and callable  
• real‑world observation is truthful and logged  

---

## High‑level architecture

Gearbox is intentionally split into three layers:

```
config  →  runtime (cli.py)  →  engines (read‑only)
```

### 1. Configuration (YAML)

All behavior is defined in static YAML files under `config/`.

These files are validated before runtime starts.

• `runtime.yaml`  
  Controls execution mode, allowed chains, evaluation interval, and safety flags.

• `chain.yaml`  
  Defines chains, networks, and RPC endpoints.  
  Multiple RPCs may be listed; selection is deterministic.

• `risk.yaml`  
  Defines non‑negotiable risk limits (not yet enforced in runtime).

• `strategies.yaml`  
  Defines allowed strategy classes and constraints (not yet executed).

• `oracle.yaml`  
  Defines oracle provider settings and the asset pair for oracle ingestion.

No code runs until all configs pass validation.

---

### 2. Runtime (`cli.py`)

`cli.py` is the **control plane**.

It owns:
• process lifecycle  
• argument parsing  
• logging  
• config validation  
• runtime loop scheduling  
• orchestration of engines  

It explicitly does **not**:
• talk to blockchains directly  
• fetch market data  
• make decisions  
• execute trades  

The runtime loop is deterministic and heartbeat‑driven.

On each tick:
1. emit a heartbeat
2. enter the evaluation phase
3. call observation engines
4. log results
5. sleep until the next interval

---

### 3. Engines (`gearbox/engine/`)

Engines are **pure, callable units**.

They:
• accept resolved config data
• perform one task
• return structured facts
• do not loop
• do not sleep
• do not log lifecycle events

#### Current engine: `market_data.py`

Implements a Phase‑1 observation primitive:

`evaluate_chain(chain_name, chain_cfg)`

This function:
• selects the default network
• selects an RPC endpoint
• performs a real, read‑only JSON‑RPC call (`eth_chainId`)
• returns a structured observation result

Example return:

```json
{
  "chain": "ethereum",
  "network": "mainnet",
  "rpc": "https://cloudflare-eth.com",
  "reachable": true,
  "timestamp": 1768865029,
  "error": null
}
```

No state is mutated.  
No decisions are made.

---

## Logging model

• All important events are written to a run‑scoped log file under `logs/`
• Log filenames are timestamped and deterministic
• `--verbose` mirrors logs to stderr
• Engines never log; runtime decides severity

This ensures complete traceability of every run.

---

## Running Gearbox

### Setup

Create and activate a virtual environment, then install dependencies:

```
pip install requests
```

### Validate configuration only

```
python cli.py --validate
```

This:
• loads configs
• validates structure
• exits without starting the runtime loop

### Run the runtime loop

```
python cli.py
```

Optional verbose output:

```
python cli.py --verbose
```

On each tick you should see:
• heartbeat
• evaluation phase
• chain reachability results

---

## Current state of the project

Implemented:
• CLI framework
• deterministic runtime loop
• config validation
• real Ethereum RPC observation
• structured logging

Not yet implemented:
• trading
• strategy selection
• risk enforcement
• state persistence
• wallets / execution

This is intentional.

---

## Philosophy

Gearbox is designed to:
• fail loudly
• separate observation from decision
• separate control from execution
• minimize loss through structure, not prediction

If something breaks, the logs should tell you **exactly where and why**.

---
