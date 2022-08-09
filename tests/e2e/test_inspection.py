from typing import List

from viqe.ngsy import InspectionType
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
            "inspection_result_normalized": 0
        }
    ]


def post_inspection_batch():
    response = viqe_client.post_inspection_batch(
        client_inspection_batch()
    )
    assert response.status_code == 200


def test_inspection(quantumleap):
    post_inspection_batch()

    raw_material_entities = quantumleap.list_entities(
        entity_type=InspectionType.raw_material
    )
    got_ids = {e.id for e in raw_material_entities}
    want_ids = {'steel-slab:1', 'steel-slab:2', 'steel-slab:3'}
    assert want_ids == got_ids

    tweezers_entities = quantumleap.list_entities(
        entity_type=InspectionType.tweezers
    )
    got_ids = {e.id for e in tweezers_entities}
    want_ids = {'tweezers:1', 'tweezers:2', 'tweezers:3'}
    assert want_ids == got_ids
