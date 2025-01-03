from fastapi import APIRouter

from api.genel_api import genel_api_olusturucu
from semalar.semalar import FakulteSchema, BolumSchema, DersSchema, OgrenciSchema
from vt.modeller import Fakulte, Bolum, Ders, Ogrenci

v1 = APIRouter(prefix="/v1",tags=["Sürüm 1.0"])
v1.include_router(genel_api_olusturucu("/fakulte",["Fakülte"],FakulteSchema,Fakulte))
v1.include_router(genel_api_olusturucu("/bolum",["Bölüm"],BolumSchema,Bolum))
v1.include_router(genel_api_olusturucu("/ders",["Dersler"],DersSchema,Ders))
v1.include_router(genel_api_olusturucu("/ogrenci",["Öğrenciler"],OgrenciSchema,Ogrenci))