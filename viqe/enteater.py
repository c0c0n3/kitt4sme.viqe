"""
Eats NGSI entities for breakfast.

Endpoint to process VIQE inspection data.
"""

from fipy.ngsi.headers import FiwareContext
from fipy.ngsi.quantumleap import QuantumLeapClient
from typing import List

from viqe.ai import analyze
from viqe.config import Settings, to_uri
import viqe.log as log
from viqe.ngsy import ClientInspection, InspectionEntityBatch


class InspectionBatchHandler:

    def __init__(self, ctx: FiwareContext, cfg: Settings):
        self._ctx = ctx
        self._cfg = cfg

    def process(self, client_inspection_batch: List[ClientInspection]):
        """Analyse the inspection data the VIQE client collected and then
        update the time series DB with the output inspection report NGSI
        entities.

        Args:
            client_inspection_batch: a batch of inspection reports the VIQE
                client sent to the cloud after an inspection session where
                VIQE carried out a series of checks on raw materials and
                tweezers dimensions.
        """
        outcome = analyze(client_inspection_batch)
        self._update_time_series(outcome)

    def _update_time_series(self, outcome: InspectionEntityBatch):
        reports = outcome.raw_materials + outcome.tweezers

        log.updating_time_series_reports(self._ctx, reports)

        endpoint = to_uri(self._cfg.quantumleap_base_url)
        client = QuantumLeapClient(base_url=endpoint, ctx=self._ctx)
        client.insert_entities(reports)
