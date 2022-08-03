"""
VIQE client data representation and corresponding NGSI entities.
"""

from enum import Enum
from fipy.ngsi.entity import BaseEntity, BoolAttr, FloatAttr, TextAttr
from pydantic import BaseModel, confloat, constr
from typing import List, Optional


class InspectionType(str, Enum):
    """Enumerate the kind of inspections VIQE can do.
    """

    raw_material = 'raw_material'
    """The type of inspections done on raw materials.
    """
    tweezers = 'tweezers_measurement'
    """The type of inspections done on tweezers dimensions.
    """


class ClientInspection(BaseModel):
    """Report the on-prem VIQE client sends to the cloud.
    """

    type: InspectionType
    """The kind of inspection VIQE did.
    """
    inspected_item_id: constr(min_length=1)
    """A non-empty string to uniquely identify the item VIQE inspected.
    """
    spec: Optional[constr(min_length=1)]
    """A non-empty string to uniquely identify the spec against which
    VIQE checked the inspected item. There's only one spec for raw material
    inspections whereas there can be many for tweezers measurements.
    """
    inspection_result: bool
    """Does the inspected item conform to the spec?
    """
    inspection_result_normalized: confloat(ge=0, le=1)
    """A float in the [0, 1] closed interval to indicate the degree to
    which the inspected item conforms to the spec. Zero means no significant
    deviations from the spec, one means the item is probably to be scrapped.
    The spec determines a conformance threshold t in (0, 1) so items with a
    value less or equal to t conform to the spec whereas values greater than
    t do not.
    """

    # TODO shouldn't the threshold be part of the report? If available,
    # then we could plot it as a horizontal line on the report chart as
    # an additional visual aid?


class BaseInspectionEntity(BaseEntity):
    """Base class for NGSI entities built out of VIQE client inspection
    data.
    """

    okay: BoolAttr
    """This field corresponds to the ``inspection_result`` field in the
    client data.
    """
    conformance_indicator: FloatAttr
    """This field corresponds to the ``inspection_result_normalized``
    field in the client data.
    """


class RawMaterialInspectionEntity(BaseInspectionEntity):
    """NGSI entity to represent the outcome of a VIQE inspection on raw
    materials. Notice the ``inspected_item_id`` in the client data becomes
    the entity ID and there's no spec field since there's only one spec
    for raw material inspections, so it's pointless to track it.
    """

    type = InspectionType.raw_material

    def to_entity(data: ClientInspection) -> 'RawMaterialInspectionEntity':
        """Convert a VIQE client inspection on raw materials to an
        instance of this NGSI entity.

        Args:
            data: inspection data from the VIQE client.

        Returns:
            The corresponding NGSI entity.

        Raises:
            ValueError: if the inspection type isn't raw materials.
        """
        if data.type != InspectionType.raw_material:
            raise ValueError(f"not a raw material inspection: {data}")

        return RawMaterialInspectionEntity(
            id=data.inspected_item_id,
            okay=BoolAttr.new(data.inspection_result),
            conformance_indicator=FloatAttr.new(
                data.inspection_result_normalized)
        )


class TweezersInspectionEntity(BaseInspectionEntity):
    """NGSI entity to represent the outcome of a VIQE inspection on tweezers.
    Notice the ``inspected_item_id`` in the client data becomes the entity ID.
    """

    type = InspectionType.tweezers
    spec: TextAttr

    def to_entity(data: ClientInspection) -> 'TweezersInspectionEntity':
        """Convert a VIQE client inspection on tweezers to an instance of
        this NGSI entity.

        Args:
            data: inspection data from the VIQE client.

        Returns:
            The corresponding NGSI entity.

        Raises:
            ValueError: if the inspection type isn't tweezers.
        """
        if data.type != InspectionType.tweezers:
            raise ValueError(f"not a tweezers inspection: {data}")

        return TweezersInspectionEntity(
            id=data.inspected_item_id,
            okay=BoolAttr.new(data.inspection_result),
            conformance_indicator=FloatAttr.new(
                data.inspection_result_normalized),
            spec=TextAttr.new(data.spec)
        )


class InspectionEntityBatch(BaseModel):
    """Conversion of VIQE client inspection data to NGSI entities.

    The VIQE client sends a list of ``ClientInspection`` to the cloud at
    the end of an on-prem inspection session. This class converts each
    ``ClientInspection`` to either a ``RawMaterialInspectionEntity`` or
    a ``TweezersInspectionEntity``, according to the inspection's type.
    """

    raw_materials: List[RawMaterialInspectionEntity]
    tweezers: List[TweezersInspectionEntity]


    def to_entity_batch(ds: List[ClientInspection]) -> 'InspectionEntityBatch':
        """Create an ``InspectionEntityBatch`` from the input VIQE client
        inspection batch.

        Args:
            ds: data received from the VIQE client.

        Returns:
            A new ``InspectionEntityBatch`` with VIQE inspection data
            mapped to the corresponding NGSI entities.
        """
        batch = InspectionEntityBatch(raw_materials=[], tweezers=[])
        for d in ds:
            if d.type == InspectionType.raw_material:
                entity = RawMaterialInspectionEntity.to_entity(d)
                batch.raw_materials.append(entity)
            if d.type == InspectionType.tweezers:
                entity = TweezersInspectionEntity.to_entity(d)
                batch.tweezers.append(entity)

        return batch
