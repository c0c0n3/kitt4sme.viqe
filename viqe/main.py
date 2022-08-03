from fastapi import FastAPI
from fipy.ngsi.headers import FiwareContext
from typing import List
import uvicorn

from viqe import __version__
from viqe.config import viqe_config
from viqe.enteater import InspectionBatchHandler
import viqe.log as log
from viqe.ngsy import ClientInspection


log.init()
app = FastAPI()


@app.get('/')
def read_root():
    return {'viqe': __version__}


@app.get("/version")
def read_version():
    return read_root()


@app.post("/{tenant}/inspection")
async def post_inspections(tenant: str, batch: List[ClientInspection]):
    ctx = FiwareContext(service=tenant, service_path='/')
    cfg = viqe_config()

    log.received_inspection_batch(ctx, batch)

    handler = InspectionBatchHandler(ctx=ctx, cfg=cfg)
    handler.process(batch)


if __name__ == '__main__':
    uvicorn.run(app)
