"""Shared test configuration and fixtures for UV tool testing."""

import subprocess
from typing import List

import pytest


@pytest.fixture
def uv_tool_cleanup():
    """Fixture to track and cleanup UV tools installed during tests.

    This fixture provides a cleanup function that ensures no UV tools
    are left installed after tests complete, preventing test pollution.

    Usage:
        def test_something(uv_tool_cleanup):
            cleanup = uv_tool_cleanup
            # ... install UV tools ...
            cleanup.add("my-tool")  # Track for cleanup
            # ... test logic ...
            # Automatic cleanup happens after test
    """
    installed_tools: List[str] = []

    class UVToolCleanup:
        def add(self, tool_name: str):
            """Add a tool name to the cleanup list."""
            if tool_name not in installed_tools:
                installed_tools.append(tool_name)

        def remove(self, tool_name: str):
            """Remove a specific tool now and from cleanup list."""
            if tool_name in installed_tools:
                installed_tools.remove(tool_name)

            subprocess.run(
                ["uv", "tool", "uninstall", tool_name],
                capture_output=True,
                check=False,  # OK if tool wasn't installed
            )

        def cleanup_all(self):
            """Clean up all tracked tools."""
            for tool_name in installed_tools:
                subprocess.run(
                    ["uv", "tool", "uninstall", tool_name],
                    capture_output=True,
                    check=False,
                )
            installed_tools.clear()

    cleanup = UVToolCleanup()

    yield cleanup

    # Cleanup after test completes
    cleanup.cleanup_all()


@pytest.fixture
def uv_available():
    """Skip test if UV is not available in the environment."""
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            pytest.skip("UV not available in test environment")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pytest.skip("UV not available or not responding")


@pytest.fixture
def git_available():
    """Skip test if git is not available in the environment."""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            pytest.skip("Git not available in test environment")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pytest.skip("Git not available or not responding")


# Performance monitoring fixture
@pytest.fixture
def performance_monitor():
    """Monitor test performance to ensure UV operations stay within limits."""
    import time

    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.thresholds = {
                'generation': 30,  # 30s for cookiecutter generation
                'uv_install': 60,  # 60s for UV tool install
                'uv_command': 30,  # 30s for UV command execution
            }

        def start(self):
            """Start timing an operation."""
            self.start_time = time.time()

        def check(self, operation: str, custom_threshold: float = None):
            """Check if operation completed within threshold."""
            if self.start_time is None:
                raise ValueError("Must call start() before check()")

            duration = time.time() - self.start_time
            threshold = custom_threshold or self.thresholds.get(operation, 60)

            if duration > threshold:
                pytest.fail(
                    f"{operation} took {duration:.2f}s, exceeding {threshold}s threshold"
                )

            self.start_time = None  # Reset for next operation
            return duration

    return PerformanceMonitor()
