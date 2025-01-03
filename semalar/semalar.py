
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TemelSorguSemasi(BaseModel):
    sayfa: int = Field(default=0, ge=0)
    kayit_sayisi:int = Field(default=10, ge=5, le=100)
    siralama: list[str] = Field(default_factory=list)

    filtre: list[str] = Field(default_factory=list)




class TemelSchema(BaseModel):
    model_config =ConfigDict(from_attributes=True)

    id: UUID | None = None
    olusturma_zamani: datetime | None = None
    guncelleme_zamani: datetime | None = None


class FakulteSchema(TemelSchema):
    adi: str
    adres: str
    telefon: str


class FakulteWithBolumSchema(FakulteSchema):
    bolumler: list['BolumSchemaSchema'] | None = Field(default_factory=list)




class BolumSchema(TemelSchema):
    adi: str
    adres: str
    telefon: str
    fakulte_id: UUID




class BolumWithBolumSchema(BolumSchema):
    ogrenciler: Optional[list['OgrenciSchema']] = [Field(default_factory=list)]


class BolumSchemaWithDersler(BolumSchema):
    dersler: Optional[list['DerslerSchema']] = [Field(default_factory=list)]


class DersSchema(TemelSchema):
    adi: str
    kodu: str
    bolum_id: UUID


class OgrenciSchema(TemelSchema):
    tckimlik_no: str
    adi: str
    soyadi: str
    numara: str
    cinsiyet: str
    dogumyeriplakasi: int
    dogumTarihi: datetime
    bolum_id: UUID





