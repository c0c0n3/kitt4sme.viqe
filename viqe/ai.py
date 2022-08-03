"""
VIQE deep learning.

NOTE. This module is just a placeholder for now.
"""

from typing import List

from viqe.ngsy import ClientInspection, InspectionEntityBatch


def analyze(client_batch: List[ClientInspection]) -> InspectionEntityBatch:
    """Analyse the inspection data the VIQE client collected.

    Args:
        client_batch: the inspection data.

    Returns:
        InspectionEntityBatch: Raw materials and tweezers inspection reports
            to sum up analysis outcome.
    """
    return InspectionEntityBatch.to_entity_batch(client_batch)

    # NOTE. This function is just a placeholder.
    # Deep learning happens client-side at the moment and will eventually
    # be migrated here. We attempted an initial migration but then realised
    # it would take too long, so we decided to keep the AI functionality at
    # the edge for now---i.e. the AI component runs on prem along w/ the
    # VIQE client.
    #
    # Bottom line: each ClientInspection already contains the analysis
    # results and all we need to do here is convert them to NGSI format.
