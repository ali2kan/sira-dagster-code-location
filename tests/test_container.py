from time import sleep

import docker
import pytest
import requests


@pytest.fixture(scope="session")
def docker_client():
    return docker.from_env()


@pytest.fixture(scope="session")
def dagster_container(docker_client):
    container = docker_client.containers.run(
        "dagster-core:latest", detach=True, ports={"3000/tcp": 3000}, environment={"DAGSTER_HOME": "/opt/dagster/dagster_home"}
    )
    sleep(5)  # Wait for container to start
    yield container
    container.stop()
    container.remove()


def test_dagster_webserver_health(dagster_container):
    """Test if the Dagster webserver is responding."""
    response = requests.get("http://localhost:3000/health")
    assert response.status_code == 200


def test_dagster_version(dagster_container):
    """Test if Dagster is installed and accessible."""
    exit_code, output = dagster_container.exec_run("dagster version")
    assert exit_code == 0
    assert "dagster" in output.decode()
