from database import DatabaseManager
from models import Hoca, Oda, Ders

DERSLER = [
    {"ders_id": 101, "ders_ad": "Bilgisayar Müh.Giriş", "kredi": 2, "şube": "Tek", "hoca_id": 11, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 103, "ders_ad": "Fizik I", "kredi": 4, "şube": "Tek", "hoca_id": 2, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 105, "ders_ad": "Kimya (Grup A)", "kredi": 4, "şube": "A", "hoca_id": 10, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 106, "ders_ad": "Kimya (Grup B)", "kredi": 4, "şube": "B", "hoca_id": 10, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 107, "ders_ad": "Matematik I", "kredi": 4, "şube": "Tek", "hoca_id": 1, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 109, "ders_ad": "A.İ.İ.T-I", "kredi": 2, "şube": "Tek", "hoca_id": 15, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 111, "ders_ad": "Türk Dili I", "kredi": 2, "şube": "Tek", "hoca_id": 13, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 113, "ders_ad": "Yabancı Dil I", "kredi": 2, "şube": "Tek", "hoca_id": 14, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 117, "ders_ad": "Kariyer Planlama", "kredi": 1, "şube": "Tek", "hoca_id": 16, "teorik_slot": 1, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 115, "ders_ad": "Mühendislik Etiği", "kredi": 3, "şube": "Tek", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    # 2. Sınıf
    {"ders_id": 201, "ders_ad": "Nesne Tabanlı Prog (A)", "kredi": 4, "şube": "A", "hoca_id": 12, "teorik_slot": 0, "lab_slot": 5, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 202, "ders_ad": "Nesne Tabanlı Prog (B)", "kredi": 4, "şube": "B", "hoca_id": 12, "teorik_slot": 0, "lab_slot": 5, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 203, "ders_ad": "Ayrık Matematik", "kredi": 3, "şube": "Tek", "hoca_id": 1, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 205, "ders_ad": "Veri Yapıları (A)", "kredi": 4, "şube": "A", "hoca_id": 7, "teorik_slot": 0, "lab_slot": 5, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 206, "ders_ad": "Veri Yapıları (B)", "kredi": 4, "şube": "B", "hoca_id": 7, "teorik_slot": 0, "lab_slot": 5, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 207, "ders_ad": "Mesleki İngilizce", "kredi": 3, "şube": "Tek", "hoca_id": 17, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 209, "ders_ad": "Diferansiyel Denklemler", "kredi": 4, "şube": "Tek", "hoca_id": 1, "teorik_slot": 4, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 211, "ders_ad": "Elektrik Devreleri (A)", "kredi": 4, "şube": "A", "hoca_id": 3, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 212, "ders_ad": "Elektrik Devreleri (B)", "kredi": 4, "şube": "B", "hoca_id": 3, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 1906002132015, "ders_ad": "Programlama Dilleri Temelleri", "kredi": 3, "akts": 4, "şube": "Tek", "hoca_id": 11, "teorik_slot": 0, "lab_slot": 3, "ue": False, "zorunlu": False, "sinif_seviyesi": 2},
    {"ders_id": 1906002152015, "ders_ad": "Mühendislik Ekonomisi", "kredi": 3, "akts": 4, "şube": "Tek", "hoca_id": 9, "teorik_slot": 3, "lab_slot": 0, "ue": False, "zorunlu": False, "sinif_seviyesi": 2},
    {"ders_id": 2906001032015, "ders_ad": "Web Programlama", "kredi": 3, "akts": 4, "şube": "Tek", "hoca_id": 8, "teorik_slot": 0, "lab_slot": 3, "ue": False, "zorunlu": False, "sinif_seviyesi": 2},
    # 3. Sınıf
    {"ders_id": 301, "ders_ad": "Mikroişlemciler (A)", "kredi": 4, "şube": "A", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 302, "ders_ad": "Mikroişlemciler (B)", "kredi": 4, "şube": "B", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 303, "ders_ad": "Algoritma Analizi (A)", "kredi": 4, "şube": "A", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 304, "ders_ad": "Algoritma Analizi (B)", "kredi": 4, "şube": "B", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 305, "ders_ad": "İşletim Sistemleri (A)", "kredi": 4, "şube": "A", "hoca_id": 8, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 306, "ders_ad": "İşletim Sistemleri (B)", "kredi": 4, "şube": "B", "hoca_id": 8, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 307, "ders_ad": "Bilgisayar Mimarisi (A)", "kredi": 3, "şube": "A", "hoca_id": 12, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 308, "ders_ad": "Bilgisayar Mimarisi (B)", "kredi": 3, "şube": "B", "hoca_id": 12, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 313, "ders_ad": "Doğal Dil İşleme", "kredi": 3, "şube": "Tek", "hoca_id": 11, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 315, "ders_ad": "Paralel Hesaplama", "kredi": 3, "şube": "Tek", "hoca_id": 8, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 317, "ders_ad": "Tasarım Desenleri", "kredi": 3, "şube": "Tek", "hoca_id": 8, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    # 4. Sınıf
    {"ders_id": 405, "ders_ad": "İleri Veri Tabanı", "kredi": 3, "şube": "Tek", "hoca_id": 9, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 411, "ders_ad": "Yapay Zeka", "kredi": 3, "şube": "Tek", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 413, "ders_ad": "Veri Madenciliği", "kredi": 3, "şube": "Tek", "hoca_id": 3, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 425, "ders_ad": "Nesnelerin İnterneti", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 4},
    {"ders_id": 421, "ders_ad": "Sensor Ağları", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 419, "ders_ad": "E Ticaret", "kredi": 3, "şube": "Tek", "hoca_id": 18, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 4},
    {"ders_id": 423, "ders_ad": "Bilişim Hukuku", "kredi": 3, "şube": "Tek", "hoca_id": 18, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 424, "ders_ad": "Robotik Sistemler", "kredi": 3, "şube": "Tek", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
]

ODALAR = [
    {"oda_id": "D100", "oda_ad": "227", "tip": "teorik"},
    {"oda_id": "D101", "oda_ad": "326", "tip": "teorik"},
    {"oda_id": "D102", "oda_ad": "327", "tip": "teorik"},
    {"oda_id": "D00", "oda_ad": "B.L", "tip": "lab"},
    {"oda_id": "D01", "oda_ad": "A.L", "tip": "lab"},
    {"oda_id": "D02", "oda_ad": "D.L", "tip": "lab"},
    {"oda_id": "ONLINE", "oda_ad": "U.E", "tip": "ue"}
]

HOCALAR = [
    {"hoca_id": 1, "hoca_ad": "Hünkar Kayhan", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]},
    {"hoca_id": 2, "hoca_ad": "Ferhat Demiray", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 3, "hoca_ad": "Ali Yılmaz", "musait_gunler": ["Pazartesi", "Salı", "Perşembe", "Cuma"]},
    {"hoca_id": 4, "hoca_ad": "Mustafa Alper Akkaş", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    {"hoca_id": 5, "hoca_ad": "Dinçer Erbaş", "musait_gunler": ["Salı", "Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 6, "hoca_ad": "Ali Çalım", "musait_gunler": ["Salı", "Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 7, "hoca_ad": "Mehmet Milli", "musait_gunler": ["Pazartesi", "Salı", "Perşembe"]},
    {"hoca_id": 8, "hoca_ad": "Önder Eyecioğlu", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Cuma"]},
    {"hoca_id": 9, "hoca_ad": "Abdulkadir Özdemir", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 10, "hoca_ad": "Berrin TOPUZ", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba"]},
    {"hoca_id": 11, "hoca_ad": "İsmail Hakkı Parlak", "musait_gunler": ["Salı", "Perşembe", "Cuma"]},
    {"hoca_id": 12, "hoca_ad": "Ümit Şentürk", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]},
    {"hoca_id": 13, "hoca_ad": "Cenk AÇIKGÖZ", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    {"hoca_id": 14, "hoca_ad": "Filiz KIRALİ", "musait_gunler": ["Salı", "Perşembe", "Cuma"]},
    {"hoca_id": 15, "hoca_ad": "Ahmet Ercivan", "musait_gunler": ["Pazartesi", "Salı", "Perşembe"]},
    {"hoca_id": 16, "hoca_ad": "Elif Çetin", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 17, "hoca_ad": "İsmihan Külcü", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    {"hoca_id": 18, "hoca_ad": "Murat BEKEN", "musait_gunler": ["Salı", "Çarşamba", "Perşembe"]}
]


def migrate():
    db = DatabaseManager()
    
    program_id = db.create_program("BAIBU", "ornek_veri_seti.py'den aktarılan veriler")
    
    print(f"Program oluşturuldu: ID={program_id}")
    for hoca_data in HOCALAR:
        hoca = Hoca(
            hoca_id=hoca_data["hoca_id"],
            hoca_ad=hoca_data["hoca_ad"],
            musait_gunler=hoca_data["musait_gunler"],
            program_id=program_id
        )
        db.add_teacher(hoca)
    print(f"{len(HOCALAR)} öğretmen eklendi.")
    for oda_data in ODALAR:
        oda = Oda(
            oda_id=oda_data["oda_id"],
            oda_ad=oda_data["oda_ad"],
            tip=oda_data["tip"],
            program_id=program_id
        )
        db.add_room(oda)
    print(f"{len(ODALAR)} oda eklendi.")
    for ders_data in DERSLER:
        ders = Ders(
            ders_id=ders_data["ders_id"],
            ders_ad=ders_data["ders_ad"],
            kredi=ders_data["kredi"],
            şube=ders_data["şube"],
            hoca_id=ders_data["hoca_id"],
            teorik_slot=ders_data.get("teorik_slot", 0),
            lab_slot=ders_data.get("lab_slot", 0),
            ue=ders_data.get("ue", False),
            sinif_seviyesi=ders_data["sinif_seviyesi"],
            program_id=program_id,
            akts=ders_data.get("akts"),
            zorunlu=ders_data.get("zorunlu")
        )
        db.add_lesson(ders)
    print(f"{len(DERSLER)} ders eklendi.")
    
    print("\nMigrasyon tamamlandı!")
    print(f"Program ID: {program_id}")
    print("Uygulamayı başlatıp bu programı seçebilirsiniz.")


if __name__ == "__main__":
    migrate()





