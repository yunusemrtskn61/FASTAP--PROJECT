from datetime import datetime
from enum import StrEnum
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from vt.temel import Temel


class Cinsiyet(StrEnum):
    Erkek = "E"
    Kadin = "K"



class Fakulte(Temel):
    __tablename__ = "fakulte"
    adi: Mapped[str]= mapped_column(String(255), nullable=False, default='',index=True)
    adres: Mapped[str]= mapped_column(String(255), nullable=False, default='',index=True)
    telefon: Mapped[str]= mapped_column(String(255), nullable=False, default='',index=True)
    bolumler: Mapped[list['Bolum']] = relationship(back_populates='fakulte', lazy = 'selectin')



class Bolum(Temel):
    __tablename__ = "bolum"
    adi: Mapped[str]= mapped_column(String(255), nullable=False, default='',index=True)
    adres: Mapped[str]= mapped_column(String(255), nullable=False, default='',index=True)
    telefon: Mapped[str]= mapped_column(String(255), nullable=False, default='',index=True)
    fakulte_id: Mapped[UUID] = mapped_column(ForeignKey('fakulte.id'))
    fakulte: Mapped[Fakulte] = relationship(back_populates = 'bolumler')
    ogrenciler: Mapped[list['Ogrenci']] = relationship(back_populates='bolum', lazy = 'selectin')
    dersler: Mapped[list['Ders']] = relationship(back_populates='bolum', lazy = 'selectin')


class Ders(Temel):
    __tablename__ = "ders"
    adi: Mapped[str]= mapped_column(String(255), nullable=False, default='',index=True)
    kodu: Mapped[str]= mapped_column(String(255), nullable=False, default='',index=True)
    bolum_id: Mapped[UUID] = mapped_column(ForeignKey('bolum.id'))
    bolum: Mapped[Bolum] = relationship(back_populates = 'dersler', lazy = 'selectin')



class Ogrenci(Temel):
    __tablename__ = "ogrenci"
    tckimlik_no: Mapped[str]= mapped_column(String(11), nullable=False, default='', index=True)
    adi: Mapped[str]= mapped_column(String(255), nullable=False, default='', index=True)
    soyadi: Mapped[str]= mapped_column(String(255), nullable=False, default='', index=True)
    numara: Mapped[str]= mapped_column(String(255), nullable=False, default='', index=True)
    cinsiyet: Mapped[Cinsiyet]= mapped_column(String(1), nullable=False, default='', index=True)
    dogumyeriplakasi: Mapped[int] = mapped_column()
    bolum_id: Mapped[UUID] = mapped_column(ForeignKey('bolum.id'))
    dogumTarihi: Mapped[datetime] = mapped_column()
    bolum: Mapped[Bolum] = relationship(back_populates = 'ogrenciler', lazy = 'selectin')

    def __repr__(self):
        return f"öğrenci {self.adi} {self.soyadi} Plaka:{self.dogumyeriplakasi}"


