# DESIGN.md — Working Outline (Question-Driven)

This document is intentionally question-based.
Each section is meant to be answered slowly, one at a time.
The answers will become the final DESIGN.md.

---

## 1. Purpose and Scope

• Why does this system exist?

This system exists to minimize avoidable losses caused by trading with the wrong strategy after market conditions change, especially when the user is not actively monitoring it.

• What personal problem am I solving first?

I want a system that does not lose money simply because I wasn’t watching the market when conditions shifted.

• What does success look like if this only ever serves one user (me)?

Success is a system that can run unattended and avoid obvious losses by adapting, pausing, or standing down when a strategy no longer fits the market.

• What would make this system a failure even if it makes money?

If it makes money but is very difficult to configure, use, or monitor, it is a failure. 

• What timeframe am I designing for (weeks, months, years)?

The timeframe should be in a year to stay relevant. 

---

## 2. Explicit Non-Goals (Negative Constraints)

• What will this system *never* do?

a. Allow an agent to place trades directly
b. Invent new strategies at runtime
c. Hide it state, decisions, or processes from the user

• What features am I intentionally refusing to support?

a. Fully autonomous, zero-configuration mode
b. Continuous parameter micro-optimization
c. Emotional or narrative-based signals
 
• What kinds of users am I *not* designing for?

a. Users who prefer abstraction over understanding
b. Users optimizing for excitement or constant activity
c. Users who want ai to replace responsibility

• What shortcuts would undermine trust if added later?

a. Allowing silent strategy shifts
b. Adjusting risk limit without approval
c. Implicit defaults that materially affect behavior

---

## 3. Authority and Decision Boundaries

• What decisions are reserved for the human?

a. Risk limits, loss thresholds, and any condition that can permanently stop or materially damage capital.
b. Which strategies exist, which markets they apply to, and which parameters can change automatically.
c. When the system starts, stops, resumes, or when its core assumptions are changed.

• What decisions may the agent recommend but not enforce?

a. Classifies current market conditions and determines which approved strategy best fits the observed regime.
b. Recommends when to switch strategies, pause execution, or reduce exposure based on confidence and signal decay.
c. Suggests permitted parameter adjustments within predefined bounds and explains why they are appropriate.

• What decisions must always be deterministic?

a. Trade execution, including order placement, sizing, timing, exits, stops, and cancellations.
b. Enforcement of risk limits, drawdown rules, halts, and failure handling.
c. State transitions, logging, and recovery behavior once a strategy is active.

• Where does uncertainty live in the system?

Only in the agent’s view of the market and which strategy fits best, never in execution, risk limits, or trade handling.

---

## 4. Risk Model and Capital Safety

• What is the maximum acceptable loss per day / per strategy?

Maximum acceptable loss is explicitly defined by the user per day and per strategy, and exceeding it immediately halts trading for the affected scope.

• What conditions immediately halt all trading?

a. Any configured loss, drawdown, or exposure limit is exceeded.
b. Market data becomes unavailable, stale, or internally inconsistent.
c. Execution or state validation fails in a way that prevents safe operation.

• How is drawdown measured and enforced?

Drawdown is measured from the most recent account peak.
If it exceeds a user-defined limit, trading stops automatically.

• What is the system allowed to do when confidence is low?

When confidence is low, the system reduces exposure or pauses trading and waits until confidence improves, within limits defined by user risk settings.

• How does the system fail safely?

On any error or unexpected state, the system stops placing new trades, exits or manages existing positions according to configured risk rules, logs the failure, and requires explicit user action to resume.

---

## 5. Strategy Model

• What strategies exist at v0?

a. Trend-following (bullish/bearish)
b. Sideways /range-bound
c. Flat / no-trade

• How is each strategy described in plain language?

a. Trend-following
• Trades in the direction of sustained momentum and exits quickly when momentum weakens.

b. Sideways / range-bound
• Trades within a defined range and assumes mean reversion rather than continuation.

c. No-trade
• Holds no exposure and waits for clearer market conditions.

• What market conditions does each strategy assume?

a. Trend-following assumes clear directional movement and expanding momentum.
b. Sideways assumes low directional conviction and repeated reversals.
c. No-trade assumes uncertainty, transition, or unreliable signals.

• What signals invalidate a strategy?

a. Trend-following is invalidated by momentum decay or repeated failed breakouts.
b. Sideways is invalidated by sustained directional movement.
c. No-trade is invalidated by sustained clarity in either direction.

• How expensive is it to be wrong with each strategy?

a. Trend-following is expensive when wrong due to false breakouts.
b. Sideways is expensive when wrong during strong trends.
c. No-trade is “expensive” only in missed opportunity, not capital loss.

---

## 6. Regime Detection and Reevaluation

• What does “market regime” mean in this system?

A market regime is a classification of current conditions used only to select a strategy, not to predict price movement.

• What signals are allowed to inform regime classification?

Regime classification may use price action, volatility, momentum, volume, and higher-level market structure, but never individual trade outcomes.

• How often is regime reevaluated?

Regime is reevaluated on a fixed, coarse interval and on significant state changes, not continuously on every price update.

• What confidence threshold is required to switch strategies?

A strategy switch requires confidence to exceed a user-defined threshold for a sustained period, not a single evaluation.

• How do I prevent thrashing between strategies?

The system prevents thrashing by requiring confidence decay before exiting a strategy, minimum dwell time per strategy, and asymmetric thresholds for entering versus exiting.

---

## 7. Agent Role and Constraints

• What questions is the agent allowed to answer?

a. Which market regime best describes current conditions.  
b. Which approved strategy fits that regime right now.  
c. Whether confidence is increasing, stable, or decaying.

• What questions is the agent forbidden from answering?

a. Whether to place a specific trade or order.  
b. How much capital to risk beyond configured limits.  
c. How to override halts, stops, or execution rules.

• What structured output must the agent produce?

a. A recommended strategy from the approved set.  
b. A confidence score with a clear range and meaning.  
c. A brief, machine-readable rationale tied to observable signals.

• How is agent confidence represented?

a. As a bounded numeric value defined in configuration.  
b. Evaluated over time, not a single observation.  
c. Used only to gate switching, not to size trades.

• What happens when the agent is unsure?

a. The agent reports low confidence explicitly.  
b. The system reduces exposure or pauses according to risk settings.  
c. No strategy change occurs until confidence recovers.

---

## 8. Execution Engine Behavior

• What guarantees does execution provide?

a. Trades are executed exactly as defined by the active strategy.  
b. Risk limits, halts, and drawdown rules are enforced without exception.  
c. No action is taken unless explicitly permitted by configuration.

• What validations occur before any trade is placed?

a. Strategy is approved and currently active.  
b. Risk, drawdown, and exposure limits are satisfied.  
c. Market data and internal state are valid and up to date.

• How are exits, stops, and limits enforced?

a. Defined as part of the strategy and applied deterministically.  
b. Monitored continuously by the execution engine.  
c. Triggered immediately when conditions are met.

• What is logged for every action?

a. Strategy state and relevant parameters.  
b. Decision source (agent recommendation vs. deterministic rule).  
c. Resulting action or refusal with reason.

• How does execution behave during partial failures?

a. New trades are stopped immediately.  
b. Existing positions are managed according to risk rules.  
c. The system enters a halted state until user intervention.

---

## 9. Configuration and UX (CLI-First)

• What must be configurable via files?

a. Risk limits, drawdown thresholds, and halt behavior.  
b. Available strategies, their parameters, and allowed adjustments.  
c. Agent settings, confidence thresholds, and evaluation intervals.

• What should never be configurable at runtime?

a. Core risk boundaries and loss limits.  
b. Strategy definitions and execution rules.  
c. Authority boundaries between user, agent, and engine.

• What commands must exist for day-to-day use?

a. Start, stop, and status commands for execution.  
b. Validate and inspect configuration without trading.  
c. View current strategy, regime, confidence, and recent actions.

• What information must always be visible to the user?

a. Active strategy and current regime classification.  
b. Confidence level and recent changes.  
c. Any halts, pauses, or enforced limits with reasons.

• What does a “read-only” mode look like?

a. Market observation and agent evaluation without execution.  
b. Full visibility into decisions, logs, and state.  
c. No trades placed and no risk applied.

---

## 10. Observability, Logging, and Audit

• What questions should logs be able to answer?

a. What strategy was active and why.  
b. What the system decided to do or not do.  
c. What changed to cause that decision.

• What state transitions must be recorded?

a. Strategy changes, pauses, resumes, and halts.  
b. Confidence threshold crossings and decay events.  
c. Entry, exit, and risk enforcement events.

• How are decisions separated from outcomes?

a. Agent recommendations are logged before execution.  
b. Execution results are logged independently.  
c. No outcome data is fed back into decision logs.

• What data would I want after a bad loss?

a. Active strategy and assumptions at the time.  
b. Confidence history leading up to the loss.  
c. Any limits reached or rules triggered.

• What data would I want after a long flat period?

a. Regime classifications and confidence over time.  
b. Reasons trades were skipped or paused.  
c. Evidence the system behaved as designed.

---

## 11. On-Chain Interaction (Minimal by Design)

• What absolutely must touch the blockchain?

a. Wallet ownership and transaction execution.  
b. Final trade settlements and transfers.  
c. Optional public verification of executed actions.

• What should never touch the blockchain?

a. Strategy logic or parameters.  
b. Agent reasoning or confidence state.  
c. Private configuration or internal logs.

• Is on-chain anchoring required or optional?

a. Optional and disabled by default.  
b. Used only for audit or verification purposes.  
c. Never required for core operation.

• What privacy assumptions am I making?

a. On-chain activity is public by default.  
b. Off-chain reasoning and configuration remain private.  
c. No attempt is made to obfuscate execution beyond wallet isolation.

• How do I rotate or isolate wallets safely?

a. One wallet per deployment or strategy scope.  
b. Manual rotation with explicit user action.  
c. No automatic key movement or recovery.

---

## 12. Model and Provider Flexibility

• What is the minimum interface a model must satisfy?

a. Accept structured market summaries as input.  
b. Return a strategy recommendation and confidence score.  
c. Produce machine-readable output only.

• How do I swap models without changing core logic?

a. Models are accessed through a fixed adapter interface.  
b. No model-specific logic exists outside the adapter.  
c. Configuration selects the active model.

• What happens if a model degrades or disappears?

a. The agent reports low confidence or fails closed.  
b. Strategy switching pauses automatically.  
c. Execution continues only under the current strategy if allowed.

• What is the fallback if no model is available?

a. No strategy changes are made.  
b. The system may reduce exposure or pause.  
c. Manual intervention is required to resume adaptation.

• How do I test agent behavior deterministically?

a. Use fixed inputs and recorded market snapshots.  
b. Mock agent outputs during testing.  
c. Validate engine behavior independently of models.

---

## 13. Failure Modes and Edge Cases

• What are the most likely ways this system loses money?

a. Incorrect regime classification during transitions.  
b. Delayed strategy switching in fast markets.  
c. Assumptions holding longer than expected.

• What are the most dangerous silent failures?

a. Stale or partial market data.  
b. Confidence drift without clear logging.  
c. Execution continuing with invalid state.

• What happens during extreme volatility?

a. Confidence is expected to drop.  
b. Exposure is reduced or trading pauses.  
c. Risk limits override strategy behavior.

• What happens during data outages?

a. New trades stop immediately.  
b. Existing positions are managed conservatively.  
c. The system halts if safe operation cannot be guaranteed.

• What happens if assumptions break suddenly?

a. Confidence decays rapidly.  
b. Strategy switches or pauses occur.  
c. Human review is required.

---

## 14. MVP Definition (First Vertical Slice)

• What is the smallest usable version?

a. One market.  
b. Two strategies plus no-trade.  
c. Read-only mode plus execution toggle.

• Which single market and strategy pair is enough?

a. A liquid spot market.  
b. One trend-following strategy.  
c. One sideways strategy.

• What can be stubbed or faked initially?

a. Agent reasoning and confidence outputs.  
b. Market data feeds.  
c. Execution endpoints.

• What does “done” look like for v0?

a. The system runs unattended without errors.  
b. Strategy switching behaves as designed.  
c. No avoidable losses occur due to regime mismatch.

• What must be proven before expanding scope?

a. Safety holds under stress.  
b. Logs explain all behavior clearly.  
c. The system is boring to operate.

---

## 15. Open Questions and Unknowns

• What do I not understand yet?

a. Optimal regime definitions.  
b. Long-term confidence calibration.  
c. Edge-case market behavior.

• What decisions am I deferring intentionally?

a. Additional strategies.  
b. Advanced execution logic.  
c. UI beyond CLI.

• What legal or regulatory questions remain open?

a. Jurisdiction-specific trading rules.  
b. Custody and liability boundaries.  
c. Distribution considerations.

• What technical risks feel underexplored?

a. Data quality under stress.  
b. Model drift over time.  
c. Long-running process stability.

• What assumptions might be wrong?

a. Regimes are cleanly separable.  
b. Confidence can be meaningfully quantified.  
c. Inactivity will always be acceptable.

---

## 16. Principles to Revisit Before Shipping

• Is the system still doing less rather than more?

a. Features have been removed, not added.  
b. Behavior remains predictable.  
c. Complexity is contained.

• Is execution still dumb and safe?

a. No adaptive logic has leaked into execution.  
b. All actions are deterministic.  
c. Refusal paths still dominate.

• Can I explain every loss after the fact?

a. Logs show assumptions and decisions.  
b. Risk limits explain outcomes.  
c. No behavior is hidden.

• Does the agent still feel advisory, not authoritative?

a. Recommendations are observable.  
b. Overrides are impossible.  
c. Execution never defers to “model judgment.”

• Would I trust this to run unattended?

a. It fails closed.  
b. It waits when unsure.  
c. It never surprises me.

---

End of outline.
