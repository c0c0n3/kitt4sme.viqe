from fastapi.testclient import TestClient
from fipy.docker import DockerCompose
from fipy.ngsi.quantumleap import QuantumLeapClient
import os
import pytest

from viqe.main import app
from tests.util.fiware import quantumleap_client, wait_on_quantumleap, \
    QUANTUMLEAP_EXTERNAL_BASE_URL


docker = DockerCompose(__file__)


@pytest.fixture(scope='package', autouse=True)
def run_services():
    docker.start()
    wait_on_quantumleap()
    os.environ['QUANTUMLEAP_BASE_URL'] = QUANTUMLEAP_EXTERNAL_BASE_URL
    yield
    docker.stop()


@pytest.fixture(scope="module")
def quantumleap() -> QuantumLeapClient:
    return quantumleap_client()


@pytest.fixture(scope="module")
def fastapi() -> TestClient:
    return TestClient(app)
