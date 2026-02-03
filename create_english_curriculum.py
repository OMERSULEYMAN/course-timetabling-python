from database import DatabaseManager
from models import Hoca, Oda, Ders

DERSLER = [
    {"ders_id": 101, "ders_ad": "Introduction to Computer Engineering", "kredi": 2, "şube": "Tek", "hoca_id": 11, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 102, "ders_ad": "Physics I", "kredi": 4, "şube": "Tek", "hoca_id": 2, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 103, "ders_ad": "Chemistry (Group A)", "kredi": 4, "şube": "A", "hoca_id": 10, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 104, "ders_ad": "Chemistry (Group B)", "kredi": 4, "şube": "B", "hoca_id": 10, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 105, "ders_ad": "Calculus I", "kredi": 4, "şube": "Tek", "hoca_id": 1, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 106, "ders_ad": "History of Ataturk I", "kredi": 2, "şube": "Tek", "hoca_id": 15, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 107, "ders_ad": "Turkish Language I", "kredi": 2, "şube": "Tek", "hoca_id": 13, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 108, "ders_ad": "Foreign Language I", "kredi": 2, "şube": "Tek", "hoca_id": 14, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 109, "ders_ad": "Career Planning", "kredi": 1, "şube": "Tek", "hoca_id": 16, "teorik_slot": 1, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 110, "ders_ad": "Engineering Ethics", "kredi": 3, "şube": "Tek", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 201, "ders_ad": "Object-Oriented Programming (A)", "kredi": 4, "şube": "A", "hoca_id": 12, "teorik_slot": 0, "lab_slot": 5, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 202, "ders_ad": "Object-Oriented Programming (B)", "kredi": 4, "şube": "B", "hoca_id": 12, "teorik_slot": 0, "lab_slot": 5, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 203, "ders_ad": "Discrete Mathematics", "kredi": 3, "şube": "Tek", "hoca_id": 1, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 205, "ders_ad": "Data Structures (A)", "kredi": 4, "şube": "A", "hoca_id": 7, "teorik_slot": 0, "lab_slot": 5, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 206, "ders_ad": "Data Structures (B)", "kredi": 4, "şube": "B", "hoca_id": 7, "teorik_slot": 0, "lab_slot": 5, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 207, "ders_ad": "Technical English", "kredi": 3, "şube": "Tek", "hoca_id": 17, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 209, "ders_ad": "Differential Equations", "kredi": 4, "şube": "Tek", "hoca_id": 1, "teorik_slot": 4, "lab_slot": 0, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 211, "ders_ad": "Electrical Circuits (A)", "kredi": 4, "şube": "A", "hoca_id": 3, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 212, "ders_ad": "Electrical Circuits (B)", "kredi": 4, "şube": "B", "hoca_id": 3, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 2},
    {"ders_id": 213, "ders_ad": "Programming Languages Fundamentals", "kredi": 3, "akts": 4, "şube": "Tek", "hoca_id": 11, "teorik_slot": 0, "lab_slot": 3, "ue": False, "zorunlu": False, "sinif_seviyesi": 2},
    {"ders_id": 214, "ders_ad": "Engineering Economics", "kredi": 3, "akts": 4, "şube": "Tek", "hoca_id": 9, "teorik_slot": 3, "lab_slot": 0, "ue": False, "zorunlu": False, "sinif_seviyesi": 2},
    {"ders_id": 215, "ders_ad": "Web Programming", "kredi": 3, "akts": 4, "şube": "Tek", "hoca_id": 8, "teorik_slot": 0, "lab_slot": 3, "ue": False, "zorunlu": False, "sinif_seviyesi": 2},
    {"ders_id": 301, "ders_ad": "Microprocessors (A)", "kredi": 4, "şube": "A", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 302, "ders_ad": "Microprocessors (B)", "kredi": 4, "şube": "B", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 303, "ders_ad": "Algorithm Analysis (A)", "kredi": 4, "şube": "A", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 304, "ders_ad": "Algorithm Analysis (B)", "kredi": 4, "şube": "B", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 305, "ders_ad": "Operating Systems (A)", "kredi": 4, "şube": "A", "hoca_id": 8, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 306, "ders_ad": "Operating Systems (B)", "kredi": 4, "şube": "B", "hoca_id": 8, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 307, "ders_ad": "Computer Architecture (A)", "kredi": 3, "şube": "A", "hoca_id": 12, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 308, "ders_ad": "Computer Architecture (B)", "kredi": 3, "şube": "B", "hoca_id": 12, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 309, "ders_ad": "Natural Language Processing", "kredi": 3, "şube": "Tek", "hoca_id": 11, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 310, "ders_ad": "Parallel Computing", "kredi": 3, "şube": "Tek", "hoca_id": 8, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 311, "ders_ad": "Design Patterns", "kredi": 3, "şube": "Tek", "hoca_id": 8, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 401, "ders_ad": "Advanced Database Systems", "kredi": 3, "şube": "Tek", "hoca_id": 9, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 402, "ders_ad": "Artificial Intelligence", "kredi": 3, "şube": "Tek", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 403, "ders_ad": "Data Mining", "kredi": 3, "şube": "Tek", "hoca_id": 3, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 404, "ders_ad": "Internet of Things", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 4},
    {"ders_id": 405, "ders_ad": "Sensor Networks", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 406, "ders_ad": "E-Commerce", "kredi": 3, "şube": "Tek", "hoca_id": 18, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 4},
    {"ders_id": 407, "ders_ad": "IT Law", "kredi": 3, "şube": "Tek", "hoca_id": 18, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 408, "ders_ad": "Robotic Systems", "kredi": 3, "şube": "Tek", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
]

# English Room Names
ODALAR = [
    {"oda_id": "R100", "oda_ad": "227", "tip": "teorik"},
    {"oda_id": "R101", "oda_ad": "326", "tip": "teorik"},
    {"oda_id": "R102", "oda_ad": "327", "tip": "teorik"},
    {"oda_id": "L00", "oda_ad": "B.Lab", "tip": "lab"},
    {"oda_id": "L01", "oda_ad": "A.Lab", "tip": "lab"},
    {"oda_id": "L02", "oda_ad": "D.Lab", "tip": "lab"},
    {"oda_id": "ONLINE", "oda_ad": "Online", "tip": "ue"}
]

HOCALAR = [
    {"hoca_id": 1, "hoca_ad": "Michael Johnson", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]},
    {"hoca_id": 2, "hoca_ad": "David Williams", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 3, "hoca_ad": "Robert Anderson", "musait_gunler": ["Pazartesi", "Salı", "Perşembe", "Cuma"]},
    {"hoca_id": 4, "hoca_ad": "James Martinez", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    {"hoca_id": 5, "hoca_ad": "Christopher Taylor", "musait_gunler": ["Salı", "Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 6, "hoca_ad": "Daniel Brown", "musait_gunler": ["Salı", "Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 7, "hoca_ad": "Matthew Davis", "musait_gunler": ["Pazartesi", "Salı", "Perşembe"]},
    {"hoca_id": 8, "hoca_ad": "Andrew Wilson", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Cuma"]},
    {"hoca_id": 9, "hoca_ad": "Joseph Moore", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 10, "hoca_ad": "Thomas Jackson", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba"]},
    {"hoca_id": 11, "hoca_ad": "Richard White", "musait_gunler": ["Salı", "Perşembe", "Cuma"]},
    {"hoca_id": 12, "hoca_ad": "Charles Harris", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]},
    {"hoca_id": 13, "hoca_ad": "Edward Martin", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    {"hoca_id": 14, "hoca_ad": "Steven Thompson", "musait_gunler": ["Salı", "Perşembe", "Cuma"]},
    {"hoca_id": 15, "hoca_ad": "Kenneth Garcia", "musait_gunler": ["Pazartesi", "Salı", "Perşembe"]},
    {"hoca_id": 16, "hoca_ad": "Brian Rodriguez", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    {"hoca_id": 17, "hoca_ad": "Kevin Lewis", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    {"hoca_id": 18, "hoca_ad": "Mark Walker", "musait_gunler": ["Salı", "Çarşamba", "Perşembe"]}
]


def create_english_curriculum():
    db = DatabaseManager()
    
    program_id = db.create_program("Computer Engineering", "English curriculum for presentation purposes")
    
    print(f"Program created: ID={program_id}")
    for hoca_data in HOCALAR:
        hoca = Hoca(
            hoca_id=hoca_data["hoca_id"],
            hoca_ad=hoca_data["hoca_ad"],
            musait_gunler=hoca_data["musait_gunler"],
            program_id=program_id
        )
        db.add_teacher(hoca)
    print(f"{len(HOCALAR)} teachers added.")
    
    # Add rooms
    for oda_data in ODALAR:
        oda = Oda(
            oda_id=oda_data["oda_id"],
            oda_ad=oda_data["oda_ad"],
            tip=oda_data["tip"],
            program_id=program_id
        )
        db.add_room(oda)
    print(f"{len(ODALAR)} rooms added.")
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
    print(f"{len(DERSLER)} courses added.")
    
    print("\nEnglish curriculum migration completed!")
    print(f"Program ID: {program_id}")
    print("Program Name: Computer Engineering")
    print("You can now select this program in the application for testing.")


if __name__ == "__main__":
    create_english_curriculum()
