# Gearbox Roadmap

This roadmap tracks **concrete system capability**, not features.
Each phase is scoped to be small, testable, and irreversible once complete.

Phases are sequential. A later phase should never require redesigning an earlier one.

---

## Phase 0 — Framework (COMPLETE)

**Goal:** Establish a deterministic control plane.

Delivered:
• CLI entrypoint with argument parsing  
• Deterministic logging (run-scoped, timestamped)  
• Initialization and validation flow  
• Explicit exit codes and failure handling  
• Runtime loop with heartbeat and scheduling  
• Clear separation of config, runtime, and engines  

**Outcome:**
A stable process lifecycle that can run indefinitely, fail loudly, and be reasoned about.

---

## Phase 1 — Configuration & Observation (COMPLETE)

**Goal:** Prove the system can observe the real world truthfully.

**Delivered:**
• Structured YAML configuration (`runtime`, `risk`, `strategies`, `chain`)  
• Strict config validation before runtime  
• Config-driven chain and network resolution  
• Read-only market data engine (`market_data`)  
• Real Ethereum RPC observation (`eth_chainId`)  
• Clear logging of reachability and failures  

**Outcome:**
A live observation pipeline with no trading, no risk, and no ambiguity.

---

## Phase 2 — Runtime State & Health

**Goal:** Give the runtime awareness of its own stability and recent history.

**Delivered:**
• Introduced a first-class runtime health object (`RuntimeHealth`)
• Tracked per-tick success and failure deterministically
• Maintained constant-size health state (no unbounded memory growth)
• Recorded last success, last failure, and consecutive failures
• Distinguished transient vs persistent failures via counters
• Computed pause and halt eligibility without altering control flow
• Exposed structured health snapshots for logging and diagnostics
• Integrated health introspection cleanly into the runtime loop
• Centralized all health-related logging through the CLI

**Outcome:**
The system understands recent operational history and can reliably
identify degraded or unsafe runtime conditions without yet enforcing
behavioral changes.

---

## Phase 3 — Chain Orientation (ON-CHAIN PRIMITIVES)

Status: LOCKED

**Goal:** Collect deterministic, execution-relevant data directly from the chain RPC.

**Delivered:**
• New chain orientation engine producing a single per-tick snapshot  
• RPC primitives only: eth_chainId, eth_blockNumber, eth_getBlockByNumber ("latest"), eth_gasPrice  
• Snapshot fields: chain, network, rpc, block_height, block_timestamp, gas_price, observed_at (UTC), success, failure_reason  
• Orientation integrated into the runtime evaluation loop alongside reachability checks  
• Runtime health degrades on orientation failure with explicit logging  

**Outcome:**
The runtime has a truthful, reproducible view of current on-chain state sufficient
to reason about execution cost and temporal alignment.

---

## Phase 4 — Oracle Ingestion (Read-Only)

Goal:
Introduce a non-chain data source and prove we can retrieve external price data deterministically.

Scope:
• Connect to a single oracle provider (one source only)
• Fetch a spot price for a single asset (e.g. ETH-USD)
• Capture oracle response metadata alongside the value
• Return oracle data without interpretation or validation
• Log oracle reachability, latency, and failures
• Treat oracle output as a claim, not a truth

Constraints:
• Read-only only — no trading, no execution
• No comparison against chain data yet
• No aggregation or averaging
• No fallback or redundancy
• No strategy logic
• No health coupling beyond basic success/failure logging

Delivered Artifacts:
• Oracle engine module (new file)
• Deterministic oracle snapshot structure:
  – asset
  – price
  – source
  – observed_at
  – success
  – failure_reason
• CLI wiring to fetch oracle data once per evaluation tick
• Logging consistent with existing runtime + health systems

Non-Goals:
• No oracle trust scoring
• No reconciliation with block data
• No confidence thresholds
• No execution gating
• No caching or smoothing

Outcome:
The system can retrieve external price data on demand, represent it as an explicit claim, and observe failures cleanly — setting the stage for chain-oracle reconciliation in Phase 5.
---
