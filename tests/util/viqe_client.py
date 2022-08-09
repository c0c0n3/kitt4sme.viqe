import json
import requests
from typing import List

from tests.util.fiware import TENANT


def inspection_endpoint_url() -> str:
    return f"http://localhost:8000/{TENANT}/inspection"


def post_inspection_batch(batch: List[dict]) -> requests.Response:
    """Send an inspection report batch to the VIQE service in the cloud.

    Args:
        batch: a list of reports. Each report collects the VIQE client
        inspection report fields in a dictionary and can either be a
        raw materials or tweezers report.

    Returns:
        The VIQE server's response.
    """
    headers = {
        'Content-Type': 'application/json'
    }
    body = json.dumps(batch)
    response = requests.post(
        inspection_endpoint_url(),
        headers=headers,
        data=body
    )
    return response
