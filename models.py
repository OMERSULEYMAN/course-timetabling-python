from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Hoca:
    hoca_id: Optional[int] = None
    hoca_ad: str = ""
    musait_gunler: List[str] = None
    program_id: int = 0
    
    def __post_init__(self):
        if self.musait_gunler is None:
            self.musait_gunler = []
    
    def to_dict(self) -> dict:
        if self.hoca_id is None:
            raise ValueError("Hoca ID boş olamaz! Önce veritabanına kaydedin.")
        return {
            "hoca_id": self.hoca_id,
            "hoca_ad": self.hoca_ad,
            "musait_gunler": self.musait_gunler
        }


@dataclass
class Oda:
    oda_id: str = ""
    oda_ad: str = ""
    tip: str = "teorik"
    program_id: int = 0
    
    def to_dict(self) -> dict:
        return {
            "oda_id": self.oda_id,
            "oda_ad": self.oda_ad,
            "tip": self.tip
        }


@dataclass
class Ders:
    ders_id: Optional[int] = None
    ders_ad: str = ""
    kredi: int = 0
    şube: str = "Tek"
    hoca_id: int = 0
    teorik_slot: int = 0
    lab_slot: int = 0
    ue: bool = False
    sinif_seviyesi: int = 1
    program_id: int = 0
    akts: Optional[int] = None
    zorunlu: Optional[bool] = None
    
    def to_dict(self) -> dict:
        if self.ders_id is None:
            raise ValueError("Ders ID boş olamaz! Önce veritabanına kaydedin.")
        result = {
            "ders_id": self.ders_id,
            "ders_ad": self.ders_ad,
            "kredi": self.kredi,
            "şube": self.şube,
            "hoca_id": self.hoca_id,
            "teorik_slot": self.teorik_slot,
            "lab_slot": self.lab_slot,
            "ue": self.ue,
            "sinif_seviyesi": self.sinif_seviyesi
        }
        if self.akts is not None:
            result["akts"] = self.akts
        if self.zorunlu is not None:
            result["zorunlu"] = self.zorunlu
        return result


@dataclass
class Program:
    program_id: int
    program_adi: str
    aciklama: Optional[str] = None
    olusturma_tarihi: Optional[str] = None

