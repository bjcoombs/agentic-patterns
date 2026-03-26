"""
Pytest configuration and fixtures for stack tests.

Demonstrates:
- Session-scoped stack initialization
- Dynamic port allocation
- Unique container naming
- Aggressive cleanup
"""

import os
import random
import socket
import string
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

import httpx
import pytest
from docker import DockerClient, from_env as docker_from_env


@dataclass
class StackConfig:
    """Configuration for a running test stack."""
    compose_file: str
    ports: dict[str, int]
    base_url: str


class StackTestManager:
    """
    Manages Docker stack lifecycle for testing.

    Provides:
    - Dynamic port allocation
    - Unique container naming
    - Per-test compose file generation
    - Aggressive cleanup
    """

    def __init__(self, template_path: str):
        self.template_path = template_path
        self.compose_file: str | None = None
        self.ports: dict[str, int] = {}
        self.docker: DockerClient = docker_from_env()

    def allocate_ports(self, count: int, min_port: int = 10000, max_port: int = 65535) -> list[int]:
        """Allocate available ports from the given range."""
        ports = []
        max_attempts = 100

        for _ in range(count):
            for attempt in range(max_attempts):
                port = random.randint(min_port, max_port)
                if self._is_port_available(port):
                    ports.append(port)
                    break
            else:
                raise RuntimeError(f"Could not allocate {count} ports")

        return ports

    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.bind(('127.0.0.1', port))
            return True
        except OSError:
            return False

    def _generate_unique_name(self, prefix: str = "stack-test") -> str:
        """Generate a unique identifier for containers/files."""
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{prefix}-{os.getpid()}-{random_suffix}"

    def start_stack(self) -> StackConfig:
        """Start the Docker stack with isolated configuration."""
        # Allocate dynamic ports
        app_port, postgres_port, redis_port = self.allocate_ports(3)
        self.ports = {
            "app": app_port,
            "postgres": postgres_port,
            "redis": redis_port,
        }

        # Generate unique compose file
        unique_id = self._generate_unique_name()
        self.compose_file = f"docker-compose-{unique_id}-{int(1e6 * pytest.time.time())}.yml"

        # Read and substitute template
        with open(self.template_path) as f:
            content = f.read()

        # Substitute environment variables
        content = (
            content.replace("${APP_PORT:-8000}", str(app_port))
            .replace("${POSTGRES_PORT:-5432}", str(postgres_port))
            .replace("${REDIS_PORT:-6379}", str(redis_port))
            .replace("${CONTAINER_NAME:-stack-test-app}", f"stack-test-{unique_id}-app")
            .replace("${CONTAINER_NAME_POSTGRES:-stack-test-postgres}", f"stack-test-{unique_id}-postgres")
            .replace("${CONTAINER_NAME_REDIS:-stack-test-redis}", f"stack-test-{unique_id}-redis")
        )

        with open(self.compose_file, "w") as f:
            f.write(content)

        # Start containers
        print(f"\nStarting stack with compose file: {self.compose_file}")
        print(f"Ports: app={app_port}, postgres={postgres_port}, redis={redis_port}")

        subprocess.run(
            ["docker", "compose", "-f", self.compose_file, "up", "-d"],
            check=True,
            capture_output=True,
        )

        return StackConfig(
            compose_file=self.compose_file,
            ports=self.ports,
            base_url=f"http://localhost:{app_port}",
        )

    def stop_stack(self) -> None:
        """Stop the stack and clean up all resources."""
        if not self.compose_file:
            return

        print(f"\nCleaning up stack: {self.compose_file}")

        try:
            # Aggressive cleanup: down -v removes volumes, --remove-orphans cleans stray containers
            subprocess.run(
                ["docker", "compose", "-f", self.compose_file, "down", "-v", "--remove-orphans"],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: cleanup error: {e}")
        finally:
            # Remove compose file
            try:
                Path(self.compose_file).unlink()
            except OSError:
                pass

    def get_logs(self, service: str) -> str:
        """Get logs for a specific service."""
        if not self.compose_file:
            raise RuntimeError("Stack not started")
        result = subprocess.run(
            ["docker", "compose", "-f", self.compose_file, "logs", service],
            capture_output=True,
            text=True,
        )
        return result.stdout


@pytest.fixture(scope="session")
def stack_manager() -> Generator[StackTestManager, None, None]:
    """Session-scoped stack manager."""
    manager = StackTestManager("docker-compose.test.yml")
    yield manager
    # Cleanup is handled in stop_stack, called explicitly in tests


@pytest.fixture(scope="session")
def stack_config(stack_manager: StackTestManager) -> Generator[StackConfig, None, None]:
    """Start the stack once per test session and provide configuration."""
    config = stack_manager.start_stack()
    yield config
    # Cleanup after all tests complete
    stack_manager.stop_stack()


@pytest.fixture(scope="session")
def http_client(stack_config: StackConfig) -> Generator[httpx.Client, None, None]:
    """HTTP client configured for the test stack."""
    with httpx.Client(
        base_url=stack_config.base_url,
        timeout=30.0,
    ) as client:
        yield client


@pytest.fixture(scope="session")
def async_http_client(stack_config: StackConfig) -> Generator[httpx.AsyncClient, None, None]:
    """Async HTTP client configured for the test stack."""
    async with httpx.AsyncClient(
        base_url=stack_config.base_url,
        timeout=30.0,
    ) as client:
        yield client


@pytest.fixture
def wait_for_ready(stack_config: StackConfig, http_client: httpx.Client):
    """Helper that waits for the stack to be ready."""
    def _wait(timeout: float = 120.0, interval: float = 2.0) -> None:
        import time
        start = time.time()

        while time.time() - start < timeout:
            try:
                response = http_client.get("/health")
                if response.status_code == 200:
                    print("Stack is ready")
                    return
            except httpx.ConnectError:
                pass
            time.sleep(interval)

        raise RuntimeError(f"Stack not ready after {timeout}s")

    return _wait
