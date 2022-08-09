from typing import List

import tests.util.viqe_client as viqe_client


def client_inspection_batch() -> List[dict]:
    return [
        {
            "type": "raw_material",
            "inspected_item_id": "steel-slab:1",
            "inspection_result": True,
            "inspection_result_normalized": 0.2
        },
        {
            "type": "raw_material",
            "inspected_item_id": "steel-slab:2",
            "inspection_result": False,
            "inspection_result_normalized": 1
        },
        {
            "type": "raw_material",
            "inspected_item_id": "steel-slab:3",
            "inspection_result": True,
            "inspection_result_normalized": 0
        },
        {
            "type": "raw_material",
            "inspected_item_id": "steel-slab:4",
            "inspection_result": True,
            "inspection_result_normalized": 0.3
        },
        {
            "type": "raw_material",
            "inspected_item_id": "steel-slab:5",
            "inspection_result": True,
            "inspection_result_normalized": 0.4
        },
        {
            "type": "raw_material",
            "inspected_item_id": "steel-slab:6",
            "inspection_result": False,
            "inspection_result_normalized": 0.6
        },
        {
            "type": "tweezers_measurement",
            "spec": "spec:1",
            "inspected_item_id": "tweezers:1",
            "inspection_result": True,
            "inspection_result_normalized": 0.2
        },
        {
            "type": "tweezers_measurement",
            "spec": "spec:1",
            "inspected_item_id": "tweezers:2",
            "inspection_result": False,
            "inspection_result_normalized": 1
        },
        {
            "type": "tweezers_measurement",
            "spec": "spec:2",
            "inspected_item_id": "tweezers:3",
            "inspection_result": True,
            "inspection_result_normalized": 0.4
        },
        {
            "type": "tweezers_measurement",
            "spec": "spec:1",
            "inspected_item_id": "tweezers:4",
            "inspection_result": True,
            "inspection_result_normalized": 0.2
        },
        {
            "type": "tweezers_measurement",
            "spec": "spec:1",
            "inspected_item_id": "tweezers:5",
            "inspection_result": False,
            "inspection_result_normalized": 0.6
        },
        {
            "type": "tweezers_measurement",
            "spec": "spec:2",
            "inspected_item_id": "tweezers:6",
            "inspection_result": True,
            "inspection_result_normalized": 0.3
        }
    ]


def post_inspection_batch() -> bool:
    response = viqe_client.post_inspection_batch(
        client_inspection_batch()
    )
    return response.status_code == 200
