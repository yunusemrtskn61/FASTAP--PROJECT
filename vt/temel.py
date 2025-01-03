import uuid
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Temel(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, nullable=False)
    olusturma_zamani: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    guncelleme_zamani: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
