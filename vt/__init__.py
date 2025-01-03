from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import scoped_session


class VeriTabani:
    def __init__(self):
        self.__session = None
        self.__engine = None

    async def connect(self, db_url: str = None):
        self.__engine = create_async_engine(db_url)

        self.__session = async_sessionmaker(
            bind=self.__engine,
            autocommit=False,
        )

    async def disconnect(self):
        await self.__engine.dispose()

    async def get_db(self):
        async with self.__session() as session:
            yield session




vt = VeriTabani()



VTBagimliligi = Annotated[AsyncSession, Depends(vt.get_db)]