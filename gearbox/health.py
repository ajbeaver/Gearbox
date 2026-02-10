import time


class RuntimeHealth:
    def __init__(self, pause_after_failures: int, halt_after_failures: int):
        # Timestamps
        self.start_time = time.time()
        self.last_success_ts = None
        self.last_failure_ts = None

        # Counters
        self.total_checks = 0
        self.consecutive_failures = 0
        self.total_warnings = 0

        # Status flags
        self.healthy = True
        self.paused = False
        self.halted = False

        # Last error context (human readable)
        self.last_error = None
        self.last_warning = None

        # Thresholds
        self.pause_after_failures = pause_after_failures
        self.halt_after_failures = halt_after_failures

    def record_success(self):
        """Call when an evaluation cycle succeeds."""
        now = time.time()
        self.total_checks += 1
        self.last_success_ts = now
        self.consecutive_failures = 0
        self.last_error = None
        self.healthy = True
        if self.paused:
            self.clear_pause()

    def record_failure(self, error_msg: str):
        """Call when an evaluation cycle fails."""
        now = time.time()
        self.total_checks += 1
        self.last_failure_ts = now
        self.consecutive_failures += 1
        self.last_error = error_msg
        self.healthy = False
        self.last_warning = None

    def record_warning(self, warning_msg: str):
        """Call when a non-fatal health issue is detected."""
        self.total_warnings += 1
        self.last_warning = warning_msg

    def should_pause(self) -> bool:
        """
        Return True if the runtime should enter a paused (degraded) state.

        Pause is intended for persistent but potentially recoverable issues.
        """
        # Pause after a small number of consecutive failures
        return self.consecutive_failures >= self.pause_after_failures

    def should_halt(self) -> bool:
        """
        Return True if the runtime should halt execution.

        Halt is intended for sustained failure indicating a non-recoverable
        or unsafe operating condition for this run.
        """
        # Halt after sustained consecutive failures
        return self.consecutive_failures >= self.halt_after_failures

    def enter_pause(self):
        """Set the runtime to paused state."""
        self.paused = True
        self.healthy = False

    def clear_pause(self):
        """Clear the paused state and mark as healthy."""
        self.paused = False
        self.healthy = True

    def enter_halt(self):
        """Set the runtime to halted state."""
        self.halted = True
        self.healthy = False
        self.paused = False

    def snapshot(self) -> dict:
        """Return a lightweight summary for logging."""
        return {
            "healthy": self.healthy,
            "paused": self.paused,
            "halted": self.halted,
            "total_checks": self.total_checks,
            "consecutive_failures": self.consecutive_failures,
            "total_warnings": self.total_warnings,
            "last_error": self.last_error,
            "last_warning": self.last_warning,
        }
