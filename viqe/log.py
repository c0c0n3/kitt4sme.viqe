from fipy.ngsi.headers import FiwareContext
import logging
from typing import Any, List

from viqe.ngsy import BaseInspectionEntity, ClientInspection


FORMAT = '%(levelname)s: %(asctime)s - %(message)s'
ROOT_LEVEL = logging.DEBUG


def init():
    logging.basicConfig(format=FORMAT, level=ROOT_LEVEL)


def _format_mgs(lines: List[Any]) -> str:
    ls = [f"{line}\n" for line in lines]
    return ''.join(ls)


def received_inspection_batch(ctx: FiwareContext,
                              batch: List[ClientInspection]):
    header = f"got inspection batch for {ctx}:"
    msg = _format_mgs([header] + batch)
    logging.info(msg)


def updating_time_series_reports(ctx: FiwareContext,
                                 reports: List[BaseInspectionEntity]):
    header = f"updating time series reports for {ctx}:"
    msg = _format_mgs([header] + reports)
    logging.info(msg)
