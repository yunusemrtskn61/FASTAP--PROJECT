import re
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query
from sqlalchemy import select, inspect

from semalar.semalar import TemelSorguSemasi
from vt import VTBagimliligi


def genel_api_olusturucu(adres: str, etiketler: list[str],schema:type,model: type):
    router = APIRouter(prefix=adres, tags=etiketler)
    async def sorgu_hazirla(sorgu_parametreleri):
        sorgu = select(model)
        model_bilgileri = inspect(model)
        model_sutunlari = set([c.name for c in model_bilgileri.columns])
        if len(sorgu_parametreleri.filtre) > 0:
            for filtre in sorgu_parametreleri.filtre:
                filtre_elemanlari = re.findall("(\W+)([><~;=]*)(.*)", filtre)[0]
                alan_adi = filtre_elemanlari[0]
                operator = filtre_elemanlari[1]
                deger = filtre_elemanlari[2]
                if alan_adi in model_sutunlari:

                    vt_sutunu = getattr(model, alan_adi)
                    match operator:
                        case ">":
                            sorgu = sorgu.where(vt_sutunu > deger)
                        case "<":
                            sorgu = sorgu.where(vt_sutunu < deger)
                        case ">=":
                            sorgu = sorgu.where(vt_sutunu >= deger)
                        case "<=":
                            sorgu = sorgu.where(vt_sutunu <= deger)
                        case "~":
                            sorgu = sorgu.where(vt_sutunu.ilike(f"{deger}"))
                        case ";":
                            gecici = deger.split(",")
                            baslangic =datetime.date.fromisoformat(gecici[0])
                            bitis = datetime.date.fromisoformat(gecici[1])
                            sorgu = sorgu.where(vt_sutunu.between(baslangic, bitis))





        if len(sorgu_parametreleri.siralama) > 0:

            for siralama_sutunu in sorgu_parametreleri.siralama:
                yon = siralama_sutunu[0]
                sutun = siralama_sutunu[1:]
                if sutun in model_sutunlari:
                    vt_sutunu = getattr(model, sutun)
                    if yon == "<":
                        sorgu = sorgu.order_by(vt_sutunu.desc())
                    elif yon == ">":
                        sorgu = sorgu.order_by(vt_sutunu.asc())
        sorgu = sorgu.limit(sorgu_parametreleri.kayit_sayisi)
        sorgu = sorgu.offset(sorgu_parametreleri.kayit_sayisi * sorgu_parametreleri.sayfa)
        return sorgu




    @router.get("/")
    async def tum_veri(db: VTBagimliligi,sorgu_parametreleri:Annotated[TemelSorguSemasi, Query()]) -> list[schema]:
        sorgu = await sorgu_hazirla(sorgu_parametreleri)
        sorgu_sonucu = await db.execute(sorgu)
        return sorgu_sonucu.scalars().all()



    @router.post("/")
    async def veri_ekle(db: VTBagimliligi, fakulte: schema) -> schema:
        data = fakulte.model_dump(mode="python")
        vt_obj = model(**data)
        db.add(vt_obj)
        await db.commit()
        await db.refresh(vt_obj)
        return vt_obj

    @router.get("/{id}")
    async def veri(db: VTBagimliligi, id: UUID) -> schema:
        sorgu_sonucu = await db.execute(select(model).where(model.id == id))
        return sorgu_sonucu.scalars().first()

    @router.put("/{id}")
    async def guncelle(db: VTBagimliligi, id: UUID, fakulte: schema ) -> schema:
        data = fakulte.model_dump(mode="python")
        sorgu_sonucu = await db.execute(select(model).where(model.id == id))
        vt_obj = sorgu_sonucu.scalars().first()
        for field in data:
            if data[field] is not None:
                setattr(vt_obj, field, data[field])
        await db.commit()
        await db.refresh(vt_obj)
        return vt_obj

    @router.delete("/{id}")
    async def sil(db: VTBagimliligi, id: UUID) -> dict[str, bool]:
        sorgu_sonucu = await db.execute(select(model).where(model.id == id))
        vt_obj = sorgu_sonucu.scalars().first()
        await db.delete(vt_obj)
        await db.commit()
        return {"silindi": True}
    return router