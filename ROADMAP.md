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

Phase 3 — Chain Orientation (ON-CHAIN PRIMITIVES)

Goal:
Collect deterministic, execution-relevant data directly from the chain RPC.
This phase answers: “Where am I on-chain right now?”

Scope:
• Query RPC endpoints for universally supported on-chain primitives
• Extract only data that is guaranteed to exist on standard Ethereum RPCs
• Produce a single per-tick chain orientation snapshot
• Integrate orientation results into the existing runtime evaluation loop
• Degrade runtime health on orientation failure

Allowed RPC Methods (Ethereum):
• eth_blockNumber
• eth_getBlockByNumber ("latest")
• eth_gasPrice (or EIP-1559 equivalent if available)

Snapshot Fields (exact, required):
• chain
• network
• rpc
• block_height
• block_timestamp
• gas_price
• observed_at (ISO 8601 UTC)
• success
• failure_reason

Constraints:
• No market data (price, volume, symbols)
• No oracles
• No execution
• No fallback logic yet
• Success is defined strictly by successful RPC responses
• All fields must come directly from the RPC

Files to Modify:
• gearbox/engine/chain_orientation.py (new)
• cli.py (wire orientation into evaluation phase)
• gearbox/validate.py (validate orientation config only)

Files Explicitly Out of Scope:
• market_data.py
• strategy logic
• execution logic
• risk evaluation

Outcome:
The runtime has a truthful, reproducible view of current on-chain state
sufficient to reason about execution cost and temporal alignment.

---

## Phase 4 — Risk Enforcement

**Goal:** Enforce non-negotiable safety constraints.

Scope:
• Runtime enforcement of `risk.yaml` limits  
• Drawdown tracking  
• Loss-based halts and pauses  
• Safety-first failure modes  

Non-goals:
• No trading yet  
• No strategy logic  

Outcome:
The system refuses to harm itself regardless of agent behavior.

---

## Phase 5 — Agent Reasoning

**Goal:** Allow adaptive strategy selection without execution authority.

Scope:
• Agent evaluates market + runtime state  
• Agent proposes strategies or mode changes  
• Automation validates proposals against risk and config  
• No direct execution power  

Non-goals:
• No wallet access  
• No order placement  

Outcome:
Intelligence without authority.

---

## Phase 6 — Execution (Opt-in)

**Goal:** Deterministic action within strict boundaries.

Scope:
• Explicit opt-in execution modes  
• Wallet and signing isolation  
• Deterministic order placement  
• Full audit logging  

Non-goals:
• No implicit trading  
• No hidden automation  

Outcome:
A controlled system that can act — but only when explicitly allowed.

---

## Guiding principles

• Observation before action  
• Determinism before intelligence  
• Safety before performance  
• Logs over dashboards  
• Boring systems that fail loudly  

---

End of roadmap.
