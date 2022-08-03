import pytest

from viqe.ngsy import *


client_inspection_data_supply = [
    {
        'type': 'raw_material',
        'inspected_item_id': 'steel-slab:1',
        'inspection_result': True,
        'inspection_result_normalized': 0.2
    },
    {
        'type': 'raw_material',
        'inspected_item_id': 'steel-slab:2',
        'inspection_result': False,
        'inspection_result_normalized': 1
    },
    {
        'type': 'raw_material',
        'inspected_item_id': 'steel-slab:3',
        'inspection_result': True,
        'inspection_result_normalized': 0
    },
    {
        'type': 'tweezers_measurement',
        'spec': 'spec:1',
        'inspected_item_id': 'tweezers:1',
        'inspection_result': True,
        'inspection_result_normalized': 0.2
    },
    {
        'type': 'tweezers_measurement',
        'spec': 'spec:1',
        'inspected_item_id': 'tweezers:2',
        'inspection_result': False,
        'inspection_result_normalized': 1
    },
    {
        'type': 'tweezers_measurement',
        'spec': 'spec:2',
        'inspected_item_id': 'tweezers:3',
        'inspection_result': True,
        'inspection_result_normalized': 0
    },
]

@pytest.mark.parametrize('data', client_inspection_data_supply)
def test_client_inspection_from_dict(data):
    inspection = ClientInspection(**data)

    assert inspection.type == data['type']
    assert inspection.inspected_item_id == data['inspected_item_id']
    assert inspection.inspection_result == data['inspection_result']
    assert inspection.inspection_result_normalized == \
        data['inspection_result_normalized']

    spec = data.get('spec', None)
    if spec is not None:
        assert inspection.spec == spec


def test_make_entity_batch_from_client_inspection_batch():
    client_batch = [ClientInspection(**d)
                    for d in client_inspection_data_supply]
    entity_batch = InspectionEntityBatch.to_entity_batch(client_batch)

    assert len(entity_batch.raw_materials) == 3
    assert len(entity_batch.tweezers) == 3

    entities = entity_batch.raw_materials + entity_batch.tweezers
    for k in range(6):
        entity = entities[k]
        client_data = client_batch[k]

        assert entity.id == client_data.inspected_item_id
        assert entity.type == client_data.type
        assert entity.okay.value == client_data.inspection_result
        assert entity.conformance_indicator.value == \
            client_data.inspection_result_normalized

    want_specs = ['spec:1', 'spec:1', 'spec:2']
    got_specs = [e.spec.value for e in entity_batch.tweezers]
    assert want_specs == got_specs
