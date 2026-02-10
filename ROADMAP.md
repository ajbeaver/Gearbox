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

Status: LOCKED

**Goal:**  
Introduce a single external oracle and prove the system can retrieve off-chain price data deterministically.

**Delivered:**  
• New oracle engine producing one snapshot per evaluation tick  
• Single oracle provider (Coinbase spot price, unauthenticated)  
• Single asset pair defined explicitly in `oracle.yaml`  
• Snapshot fields: asset, price (string), source, observed_at (UTC), source_timestamp (UTC), latency_ms, success, failure_reason  
• Oracle ingestion wired into the runtime evaluation loop  
• Explicit logging of oracle success, latency, and failure reasons  
• Oracle failures logged without degrading RuntimeHealth  

**Constraints:**  
• Read-only only — no trading, no execution  
• No comparison against chain data  
• No aggregation, averaging, or smoothing  
• No redundancy or fallback providers  
• No strategy logic  
• No execution gating  

**Outcome:**  
The runtime can retrieve external price data on demand, represent it as an explicit claim with provenance and timing metadata, and observe oracle failures cleanly — without assuming correctness or enforcing behavior.  
This establishes the foundation for chain-oracle reconciliation in Phase 5.

---

## Phase 5 — Chain–Oracle Reconciliation (Trust Gating)

Status: PLANNED

**Goal:**  
Determine whether externally sourced oracle data is *usable right now* by reconciling it against on-chain orientation data.

This phase introduces the concept of **conditional trust** without enabling execution.

---

**Inputs:**
• Chain orientation snapshot (Phase 3)  
• Oracle snapshot (Phase 4)

---

**Delivered:**
• New reconciliation step executed once per evaluation tick  
• Deterministic comparison between chain and oracle data  
• Explicit trust classification for oracle output  
• Structured logging of reconciliation decisions and failures  

---

**Reconciliation Checks (Minimum Set):**
• Oracle timestamp vs chain block timestamp  
• Oracle staleness relative to chain time (configurable threshold)  
• Oracle latency stability across ticks  
• Price validity checks (non-null, non-zero, finite)  

---

**Outputs:**
• Reconciled oracle state with explicit trust status:
  – trusted
  – degraded
  – rejected
• Reason codes explaining reconciliation outcomes  
• No mutation of original chain or oracle snapshots  

---

**Behavioral Rules:**
• Oracle data marked *rejected* must not be consumed by downstream logic  
• Oracle data marked *degraded* is observable but flagged as unsafe  
• Oracle failures still do not degrade RuntimeHealth  
• Reconciliation failures are logged, not acted upon  

---

**Constraints:**
• No execution of trades  
• No strategy logic  
• No aggregation across multiple oracles  
• No fallback or redundancy  
• No capital or risk decisions  
• No caching or smoothing  

---

**Non-Goals:**
• No prediction or forecasting  
• No oracle ranking  
• No cross-oracle consensus  
• No price normalization  
• No execution gating yet  

---

**Outcome:**
The system can distinguish between:
• what the chain reports,
• what an oracle claims,
• and whether that claim is currently trustworthy relative to on-chain reality.

This phase establishes the trust boundary required before any execution logic can safely exist.

---