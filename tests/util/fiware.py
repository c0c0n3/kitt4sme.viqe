from fipy.ngsi.headers import FiwareContext
from fipy.ngsi.quantumleap import QuantumLeapClient
from fipy.wait import wait_for_quantumleap
from uri import URI


TENANT = 'rovi'
QUANTUMLEAP_EXTERNAL_BASE_URL = 'http://localhost:8668'


def quantumleap_client() -> QuantumLeapClient:
    base_url = URI(QUANTUMLEAP_EXTERNAL_BASE_URL)
    ctx = FiwareContext(service=TENANT, service_path='/')
    return QuantumLeapClient(base_url, ctx)


def wait_on_quantumleap():
    wait_for_quantumleap(quantumleap_client())
