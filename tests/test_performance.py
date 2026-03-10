"""Tests for CLI performance and startup time."""

import subprocess
import time

def test_cli_startup_time_under_threshold():
    """Ensure CLI startup time is under threshold for --help."""
    start = time.time()
    result = subprocess.run(["jules", "--help"], capture_output=True, text=True)
    elapsed = time.time() - start

    assert result.returncode == 0
    assert elapsed < 0.4, f"CLI startup took {elapsed:.3f}s, expected < 0.4s"
