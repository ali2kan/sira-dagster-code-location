from time import sleep

import docker
import pytest


@pytest.fixture(scope="session")
def docker_client():
    return docker.from_env()


@pytest.fixture(scope="session")
def dagster_container(docker_client):
    container = docker_client.containers.run(
        "dagster-code-location-base:test", detach=True, ports={"4000/tcp": 4000}, environment={"DAGSTER_HOME": "/opt/dagster/dagster_home"}
    )
    sleep(5)  # Wait for container to start
    yield container
    container.stop()
    container.remove()


def test_uv_availability(dagster_container):
    """Test if uv is installed and accessible."""
    exit_code, output = dagster_container.exec_run("which uv")
    assert exit_code == 0
    assert "/bin/uv" in output.decode()


def test_dagster_version(dagster_container):
    """Test if Dagster is installed and accessible."""
    exit_code, output = dagster_container.exec_run("dagster --version")
    assert exit_code == 0
    assert "dagster" in output.decode()
