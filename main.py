from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import v1
from vt import vt



@asynccontextmanager
async def yasam_dongusu(app: FastAPI):
    # uygulama başlarken çalışacak olan kod bloğu
    await vt.connect("postgresql+asyncpg://yunus:1259@localhost:5432/yunus1")
    yield
    await vt.disconnect()

    # uygulama kapatılırken çalışacak kod bloğu

app = FastAPI(lifespan=yasam_dongusu)

app.include_router(v1)

#app.include_router(ogr_api_router)
#app.include_router(fakulte_api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

