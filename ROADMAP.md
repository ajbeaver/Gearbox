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

Outcome:
A stable process lifecycle that can run indefinitely, fail loudly, and be reasoned about.

---

## Phase 1 — Configuration & Observation (COMPLETE)

**Goal:** Prove the system can observe the real world truthfully.

Delivered:
• Structured YAML configuration (`runtime`, `risk`, `strategies`, `chain`)  
• Strict config validation before runtime  
• Config-driven chain and network resolution  
• Read-only market data engine (`market_data`)  
• Real Ethereum RPC observation (`eth_chainId`)  
• Clear logging of reachability and failures  

Outcome:
A live observation pipeline with no trading, no risk, and no ambiguity.

---

## Phase 2 — Runtime State & Health

**Goal:** Remember what has happened and react safely.

Scope:
• Accumulate observation results into runtime state  
• Track last success, last failure, consecutive failures  
• Distinguish transient vs persistent chain issues  
• Define when observation failures should pause or halt runtime  

Non-goals:
• No market data yet  
• No trading logic  
• No persistence across restarts  

Outcome:
The system understands *history*, not just the current tick.

---

## Phase 3 — Market Primitives

**Goal:** Observe markets, not just chains.

Scope:
• Read-only market snapshots (price, volume, block height)  
• Deterministic data fetching interfaces  
• Clear separation between observation and interpretation  
• Config-driven selection of observable markets  

Non-goals:
• No strategy selection  
• No execution  
• No optimization  

Outcome:
Agents and risk logic can reason about market conditions using trusted data.

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
