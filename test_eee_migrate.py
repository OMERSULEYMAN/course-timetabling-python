from database import DatabaseManager
from models import Hoca, Oda, Ders

HOCALAR = [
    {"hoca_id": 1, "hoca_ad": "Prof. Dr. Robert Chen", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]},
    {"hoca_id": 2, "hoca_ad": "Prof. Dr. Sarah Mitchell", "musait_gunler": ["Salı", "Çarşamba", "Perşembe"]},
    {"hoca_id": 3, "hoca_ad": "Assoc. Prof. Dr. James Anderson", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    {"hoca_id": 4, "hoca_ad": "Assoc. Prof. Dr. Emily Rodriguez", "musait_gunler": ["Salı", "Perşembe", "Cuma"]},
    {"hoca_id": 5, "hoca_ad": "Prof. Dr. Michael Thompson", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]},
    {"hoca_id": 6, "hoca_ad": "Dr. David Kim", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 7, "hoca_ad": "Assoc. Prof. Dr. Lisa Wang", "musait_gunler": ["Pazartesi", "Salı", "Cuma"]},
    {"hoca_id": 8, "hoca_ad": "Prof. Dr. Christopher Brown", "musait_gunler": ["Pazartesi", "Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 9, "hoca_ad": "Dr. Jennifer Martinez", "musait_gunler": ["Salı", "Çarşamba", "Perşembe"]},
    {"hoca_id": 10, "hoca_ad": "Assoc. Prof. Dr. Daniel Lee", "musait_gunler": ["Pazartesi", "Salı", "Perşembe"]},
    {"hoca_id": 11, "hoca_ad": "Prof. Dr. Amanda White", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    {"hoca_id": 12, "hoca_ad": "Dr. Kevin Johnson", "musait_gunler": ["Salı", "Perşembe", "Cuma"]},
]

ODALAR = [
    {"oda_id": "E201", "oda_ad": "LH201", "tip": "teorik"},  # Lecture Hall 201
    {"oda_id": "E202", "oda_ad": "LH202", "tip": "teorik"},  # Lecture Hall 202
    {"oda_id": "E301", "oda_ad": "SR301", "tip": "teorik"},  # Seminar Room 301
    {"oda_id": "E302", "oda_ad": "SR302", "tip": "teorik"},  # Seminar Room 302
    {"oda_id": "EL101", "oda_ad": "EL101", "tip": "lab"},    # Electronics Lab 1
    {"oda_id": "EL102", "oda_ad": "EL102", "tip": "lab"},    # Electronics Lab 2
    {"oda_id": "EL201", "oda_ad": "PSL", "tip": "lab"},      # Power Systems Lab
    {"oda_id": "ONLINE", "oda_ad": "ONLINE", "tip": "ue"},
]

DERSLER = [
    {"ders_id": 101, "ders_ad": "Introduction to Electrical Engineering", "kredi": 2, "şube": "Tek", "hoca_id": 11, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 102, "ders_ad": "Calculus II", "kredi": 4, "şube": "Tek", "hoca_id": 1, "teorik_slot": 4, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 103, "ders_ad": "Physics II", "kredi": 4, "şube": "Tek", "hoca_id": 2, "teorik_slot": 4, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 104, "ders_ad": "Linear Algebra", "kredi": 3, "şube": "Tek", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 105, "ders_ad": "DC Circuit Analysis (A)", "kredi": 4, "şube": "A", "hoca_id": 3, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 106, "ders_ad": "DC Circuit Analysis (B)", "kredi": 4, "şube": "B", "hoca_id": 3, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 107, "ders_ad": "History of Turkish Republic I", "kredi": 2, "şube": "Tek", "hoca_id": 9, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 108, "ders_ad": "Turkish Language I", "kredi": 2, "şube": "Tek", "hoca_id": 10, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 109, "ders_ad": "English I", "kredi": 2, "şube": "Tek", "hoca_id": 12, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    
    # 2ND YEAR
    {"ders_id": 201, "ders_ad": "AC Circuit Analysis (A)", "kredi": 4, "şube": "A", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 202, "ders_ad": "AC Circuit Analysis (B)", "kredi": 4, "şube": "B", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 203, "ders_ad": "Electrical Machines I (A)", "kredi": 4, "şube": "A", "hoca_id": 8, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 204, "ders_ad": "Electrical Machines I (B)", "kredi": 4, "şube": "B", "hoca_id": 8, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 205, "ders_ad": "Electromagnetic Field Theory", "kredi": 4, "şube": "Tek", "hoca_id": 4, "teorik_slot": 4, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 206, "ders_ad": "Semiconductor Devices (A)", "kredi": 4, "şube": "A", "hoca_id": 7, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 207, "ders_ad": "Semiconductor Devices (B)", "kredi": 4, "şube": "B", "hoca_id": 7, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 208, "ders_ad": "Differential Equations", "kredi": 3, "şube": "Tek", "hoca_id": 1, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 209, "ders_ad": "Probability and Random Processes", "kredi": 3, "şube": "Tek", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 210, "ders_ad": "Technical English", "kredi": 3, "şube": "Tek", "hoca_id": 12, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 211, "ders_ad": "Engineering Ethics", "kredi": 2, "şube": "Tek", "hoca_id": 9, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 2},
    {"ders_id": 301, "ders_ad": "Automatic Control Systems (A)", "kredi": 4, "şube": "A", "hoca_id": 8, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 302, "ders_ad": "Automatic Control Systems (B)", "kredi": 4, "şube": "B", "hoca_id": 8, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 303, "ders_ad": "Power System Analysis", "kredi": 4, "şube": "Tek", "hoca_id": 4, "teorik_slot": 4, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 304, "ders_ad": "Analog Electronics (A)", "kredi": 4, "şube": "A", "hoca_id": 7, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 305, "ders_ad": "Analog Electronics (B)", "kredi": 4, "şube": "B", "hoca_id": 7, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 306, "ders_ad": "Electromagnetic Waves", "kredi": 3, "şube": "Tek", "hoca_id": 2, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 307, "ders_ad": "Power Electronics and Drives", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 2, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 308, "ders_ad": "Electrical Measurements (A)", "kredi": 3, "şube": "A", "hoca_id": 2, "teorik_slot": 2, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 309, "ders_ad": "Engineering Project Management", "kredi": 2, "şube": "Tek", "hoca_id": 9, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 3},
    {"ders_id": 401, "ders_ad": "High Voltage Engineering", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 402, "ders_ad": "Antenna Theory and Design", "kredi": 3, "şube": "Tek", "hoca_id": 2, "teorik_slot": 2, "lab_slot": 2, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 403, "ders_ad": "Electrical Machine Design", "kredi": 3, "şube": "Tek", "hoca_id": 7, "teorik_slot": 2, "lab_slot": 2, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 404, "ders_ad": "Renewable Energy Technologies", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 4},
    {"ders_id": 405, "ders_ad": "Industrial Control Systems", "kredi": 3, "şube": "Tek", "hoca_id": 6, "teorik_slot": 2, "lab_slot": 2, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 406, "ders_ad": "Senior Design Project I", "kredi": 3, "şube": "Tek", "hoca_id": 11, "teorik_slot": 0, "lab_slot": 4, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 407, "ders_ad": "Professional Practice", "kredi": 2, "şube": "Tek", "hoca_id": 9, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 4},
]


def migrate():
    """EEE test verilerini veritabanına aktar"""
    db = DatabaseManager()
    
    # Program oluştur
    program_id = db.create_program(
        "Electrical and Electronics Engineering - Spring 2024",
        "Electrical and Electronics Engineering Department Spring 2024 Test Data Set"
    )
    
    print(f"Program oluşturuldu: ID={program_id}")
    
    # Öğretmenleri ekle
    print("\nÖğretmenler ekleniyor...")
    for hoca_data in HOCALAR:
        hoca = Hoca(
            hoca_id=hoca_data["hoca_id"],
            hoca_ad=hoca_data["hoca_ad"],
            musait_gunler=hoca_data["musait_gunler"],
            program_id=program_id
        )
        db.add_teacher(hoca, auto_id=False)
        print(f"  ✓ {hoca.hoca_ad}")
    
    print("\nOdalar ekleniyor...")
    for oda_data in ODALAR:
        oda = Oda(
            oda_id=oda_data["oda_id"],
            oda_ad=oda_data["oda_ad"],
            tip=oda_data["tip"],
            program_id=program_id
        )
        db.add_room(oda, auto_id=False)
        print(f"  ✓ {oda.oda_ad} ({oda.tip})")
    
    print("\nDersler ekleniyor...")
    for ders_data in DERSLER:
        ders = Ders(
            ders_id=ders_data["ders_id"],
            ders_ad=ders_data["ders_ad"],
            kredi=ders_data["kredi"],
            şube=ders_data["şube"],
            hoca_id=ders_data["hoca_id"],
            teorik_slot=ders_data["teorik_slot"],
            lab_slot=ders_data["lab_slot"],
            ue=ders_data["ue"],
            sinif_seviyesi=ders_data["sinif_seviyesi"],
            program_id=program_id
        )
        db.add_lesson(ders, auto_id=False)
        print(f"  ✓ {ders.ders_ad} ({ders.sinif_seviyesi}. Sınıf)")
    
    print("\n" + "="*70)
    print("EEE Test Veri Seti başarıyla veritabanına aktarıldı!")
    print(f"Program ID: {program_id}")
    print("Program Adı: Electrical and Electronics Engineering - Spring 2024")
    print("\nİstatistikler:")
    print(f"  - Toplam Öğretmen: {len(HOCALAR)}")
    print(f"  - Toplam Oda: {len(ODALAR)}")
    print(f"  - Toplam Ders: {len(DERSLER)}")
    print("="*70)
    print("\nUygulamayı başlatıp bu programı seçebilirsiniz.")


if __name__ == "__main__":
    migrate()
