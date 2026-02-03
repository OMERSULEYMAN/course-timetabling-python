from ortools.sat.python import cp_model
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# ==========================================
# 1. VERİ SETLERİ (AYNEN KORUNDU)
# ==========================================

DERSLER = [
    # 1. Sınıf
    {"ders_id": 101, "ders_ad": "Bilgisayar Müh.Giriş", "kredi": 2, "şube": "Tek", "hoca_id": 11, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 102, "ders_ad": "Fizik I", "kredi": 4, "şube": "Tek", "hoca_id": 2, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 103, "ders_ad": "Kimya (Grup A)", "kredi": 4, "şube": "A", "hoca_id": 10, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 104, "ders_ad": "Kimya (Grup B)", "kredi": 4, "şube": "B", "hoca_id": 10, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 105, "ders_ad": "Matematik I", "kredi": 4, "şube": "Tek", "hoca_id": 1, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 1},
    {"ders_id": 106, "ders_ad": "A.İ.İ.T-I", "kredi": 2, "şube": "Tek", "hoca_id": 15, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 107, "ders_ad": "Türk Dili I", "kredi": 2, "şube": "Tek", "hoca_id": 13, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 108, "ders_ad": "Yabancı Dil I", "kredi": 2, "şube": "Tek", "hoca_id": 14, "teorik_slot": 2, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 109, "ders_ad": "Kariyer Planlama", "kredi": 1, "şube": "Tek", "hoca_id": 16, "teorik_slot": 1, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},
    {"ders_id": 110, "ders_ad": "Mühendislik Etiği", "kredi": 3, "şube": "Tek", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 1},

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
    {"ders_id": 213,"ders_ad": "Programlama Dilleri Temelleri","kredi": 3,"akts": 4,"şube" : "Tek","hoca_id": 11,"teorik_slot": 0,"lab_slot": 3,"ue": False,"zorunlu": False,"sinif_seviyesi": 2},
    {"ders_id": 214,"ders_ad": "Mühendislik Ekonomisi","kredi": 3,"akts": 4,"şube" : "Tek","hoca_id": 9,"teorik_slot": 3,"lab_slot": 0,"ue": False,"zorunlu": False,"sinif_seviyesi": 2},
    {"ders_id": 215,"ders_ad": "Web Programlama","kredi": 3,"akts": 4,"şube" : "Tek","hoca_id": 8,"teorik_slot": 0,"lab_slot": 3,"ue": False,"zorunlu": False,"sinif_seviyesi": 2},
   
    # 3. Sınıf
    {"ders_id": 301, "ders_ad": "Mikroişlemciler (A)", "kredi": 4, "şube": "A", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 302, "ders_ad": "Mikroişlemciler (B)", "kredi": 4, "şube": "B", "hoca_id": 6, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 303, "ders_ad": "Algoritma Analizi (A)", "kredi": 4, "şube": "A", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 304, "ders_ad": "Algoritma Analizi (B)", "kredi": 4, "şube": "B", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 2, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 305, "ders_ad": "İşletim Sistemleri (A)", "kredi": 4, "şube": "A", "hoca_id": 8, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 306, "ders_ad": "İşletim Sistemleri (B)", "kredi": 4, "şube": "B", "hoca_id": 8, "teorik_slot": 5, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 307, "ders_ad": "Bilgisayar Mimarisi (A)", "kredi": 3, "şube": "A", "hoca_id": 12, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 308, "ders_ad": "Bilgisayar Mimarisi (B)", "kredi": 3, "şube": "B", "hoca_id": 12, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 309, "ders_ad": "Doğal Dil İşleme", "kredi": 3, "şube": "Tek", "hoca_id": 11, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 310, "ders_ad": "Paralel Hesaplama", "kredi": 3, "şube": "Tek", "hoca_id": 8, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 3},
    {"ders_id": 311, "ders_ad": "Tasarım Desenleri", "kredi": 3, "şube": "Tek", "hoca_id": 8, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 3},

    # 4. Sınıf
    {"ders_id": 401, "ders_ad": "İleri Veri Tabanı", "kredi": 3, "şube": "Tek", "hoca_id": 9, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 402, "ders_ad": "Yapay Zeka", "kredi": 3, "şube": "Tek", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 403, "ders_ad": "Veri Madenciliği", "kredi": 3, "şube": "Tek", "hoca_id": 3, "teorik_slot": 0, "lab_slot": 3, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 404, "ders_ad": "Nesnelerin İnterneti", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 4},
    {"ders_id": 405, "ders_ad": "Sensor Ağları", "kredi": 3, "şube": "Tek", "hoca_id": 4, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 406, "ders_ad": "E Ticaret", "kredi": 3, "şube": "Tek", "hoca_id": 18, "teorik_slot": 3, "lab_slot": 0, "ue": True, "sinif_seviyesi": 4},
    {"ders_id": 407, "ders_ad": "Bilişim Hukuku", "kredi": 3, "şube": "Tek", "hoca_id": 18, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4},
    {"ders_id": 408, "ders_ad": "Robotik Sistemler", "kredi": 3, "şube": "Tek", "hoca_id": 5, "teorik_slot": 3, "lab_slot": 0, "ue": False, "sinif_seviyesi": 4}, 
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
    # YÜKSEK YÜK (Mat I, Ayrık, Dif) -> 4 Gün
    {"hoca_id": 1, "hoca_ad": "Hünkar Kayhan", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]},
    
    # ORTA YÜK (Fizik I) -> 3 Gün
    {"hoca_id": 2, "hoca_ad": "Ferhat Demiray", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    
    # YÜKSEK YÜK (Elk Devreleri A/B + Veri Mad.) -> 4 Gün
    {"hoca_id": 3, "hoca_ad": "Ali Yılmaz", "musait_gunler": ["Pazartesi", "Salı", "Perşembe", "Cuma"]},
    
    # ORTA YÜK (IoT, Sensor) -> 3 Gün
    {"hoca_id": 4, "hoca_ad": "Mustafa Alper Akkaş", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    
    # ÇOK YÜKSEK YÜK (Algoritma A/B + Yapay Zeka) -> 4 Gün
    {"hoca_id": 5, "hoca_ad": "Dinçer Erbaş", "musait_gunler": ["Salı", "Çarşamba", "Perşembe", "Cuma"]},
    
    # YÜKSEK YÜK (Mikro A/B + Etik) -> 4 Gün (Pazartesi boş bıraktım senin eski listedeki gibi)
    {"hoca_id": 6, "hoca_ad": "Ali Çalım", "musait_gunler": ["Salı", "Çarşamba", "Perşembe", "Cuma"]},
    
    # ORTA YÜK (Veri Yapıları A/B) -> 3 Gün (Labları da olduğu için 3 gün ideal)
    {"hoca_id": 7, "hoca_ad": "Mehmet Milli", "musait_gunler": ["Pazartesi", "Salı", "Perşembe"]},
    
    # ÇOK YÜKSEK YÜK (İşletim A/B + Paralel + Tasarım) -> 4 Gün
    {"hoca_id": 8, "hoca_ad": "Önder Eyecioğlu", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Cuma"]},
    
    # HAFİF YÜK (İleri Veri Tabanı) -> 3 Gün
    {"hoca_id": 9, "hoca_ad": "Abdulkadir Özdemir", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    
    # ORTA YÜK (Kimya A/B) -> 3 Gün
    {"hoca_id": 10, "hoca_ad": "Berrin TOPUZ", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba"]},
    
    # ORTA YÜK (Giriş + NLP) -> 3 Gün
    {"hoca_id": 11, "hoca_ad": "İsmail Hakkı Parlak", "musait_gunler": ["Salı", "Perşembe", "Cuma"]},
    
    # ÇOK YÜKSEK YÜK (NTP A/B + Mimari A/B) -> 4 Gün (Hatta 5 bile ister ama 4'te zorlayalım)
    {"hoca_id": 12, "hoca_ad": "Ümit Şentürk", "musait_gunler": ["Pazartesi", "Salı", "Çarşamba", "Perşembe"]},
    
    # HAFİF YÜK (Türk Dili) -> 3 Gün
    {"hoca_id": 13, "hoca_ad": "Cenk AÇIKGÖZ", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    
    # HAFİF YÜK (Yabancı Dil) -> 3 Gün
    {"hoca_id": 14, "hoca_ad": "Filiz KIRALİ", "musait_gunler": ["Salı", "Perşembe", "Cuma"]},
    
    # HAFİF YÜK (AİİT) -> 3 Gün
    {"hoca_id": 15, "hoca_ad": "Ahmet Ercivan", "musait_gunler": ["Pazartesi", "Salı", "Perşembe"]},
    
    # ÇOK HAFİF YÜK (Kariyer - 1 Saat) -> 3 Gün
    {"hoca_id": 16, "hoca_ad": "Elif Çetin", "musait_gunler": ["Çarşamba", "Perşembe", "Cuma"]},
    
    # HAFİF YÜK (Mesleki İng) -> 3 Gün
    {"hoca_id": 17, "hoca_ad": "İsmihan Külcü", "musait_gunler": ["Pazartesi", "Çarşamba", "Cuma"]},
    
    # ORTA YÜK (E-Ticaret + Hukuk) -> 3 Gün
    {"hoca_id": 18, "hoca_ad": "Murat BEKEN", "musait_gunler": ["Salı", "Çarşamba", "Perşembe"]}
]

GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe","Cuma"]
SLOTLAR = ["08:30", "09:30", "10:30", "11:30", "12:30", "13:30", "14:30", "15:30", "16:30", "17:30"]
NUM_DAYS, NUM_SLOTS = len(GUNLER), len(SLOTLAR)
TOTAL_SLOTS = NUM_DAYS * NUM_SLOTS

# ==========================================
# 2. MODEL KURULUMU
# ==========================================

model = cp_model.CpModel()
all_tasks = {}
room_intervals = {i: [] for i in range(len(ODALAR))}
teacher_intervals = {h['hoca_id']: [] for h in HOCALAR}
student_group_intervals = {}

# CEZA PUANLARINI TOPLAYACAĞIMIZ LİSTE
optimization_penalties = []

# ---------------------------------------------------------
# A. DEĞİŞKENLERİ OLUŞTURMA
# ---------------------------------------------------------
task_id_counter = 0

for ders in DERSLER:
    components = []
    if ders.get('teorik_slot', 0) > 0:
        components.append({'type': 'teorik', 'duration': ders['teorik_slot'], 'room_type': 'ue' if ders['ue'] else 'teorik'})
    if ders.get('lab_slot', 0) > 0:
        components.append({'type': 'lab', 'duration': ders['lab_slot'], 'room_type': 'lab'})

    current_course_ids = [] 

    for comp in components:
        duration = comp['duration']
        req_type = comp['room_type']
        
        start_var = model.NewIntVar(0, TOTAL_SLOTS - duration, f'start_{task_id_counter}')
        end_var = model.NewIntVar(0, TOTAL_SLOTS, f'end_{task_id_counter}')
        interval_var = model.NewIntervalVar(start_var, duration, end_var, f'int_{task_id_counter}')
        
        # Gün Aşımı Kısıtı
        start_day_time = model.NewIntVar(0, NUM_SLOTS - 1, f'day_time_{task_id_counter}')
        model.AddModuloEquality(start_day_time, start_var, NUM_SLOTS)
        model.Add(start_day_time + duration <= NUM_SLOTS)

        # Oda Ataması
        possible_rooms = [i for i, r in enumerate(ODALAR) if r['tip'] == req_type]
        room_lits = []
        for r_idx in possible_rooms:
            lit = model.NewBoolVar(f't_{task_id_counter}_r_{r_idx}')
            room_lits.append(lit)
            room_intervals[r_idx].append(model.NewOptionalIntervalVar(start_var, duration, end_var, lit, f'opt_{task_id_counter}_{r_idx}'))
        
        model.Add(sum(room_lits) == 1)

        all_tasks[task_id_counter] = {
            'info': ders, 'type': comp['type'],
            'start': start_var, 'end': end_var, 'interval': interval_var,
            'room_literals': dict(zip(possible_rooms, room_lits)),
            'start_day_time': start_day_time # Bunu ilerde kullanacağız
        }
        
        teacher_intervals[ders['hoca_id']].append(interval_var)
        
        seviye, sube = ders['sinif_seviyesi'], ders['şube']
        groups = [f"{seviye}-A", f"{seviye}-B"] if sube == "Tek" else [f"{seviye}-{sube}"]
        for g in groups:
            student_group_intervals.setdefault(g, []).append(interval_var)

        # ==========================================
        # OPTİMİZASYON KURALI 1: BÜYÜK DERSLER SABAHA (Big Rocks)
        # ==========================================
        # Eğer ders süresi 4 saat veya fazlaysa, tercihen 08:30 (slot index 0) başlamalı.
        if duration >= 4:
            is_0830 = model.NewBoolVar(f'is_0830_{task_id_counter}')
            # start_day_time == 0 ise is_0830 = True
            model.Add(start_day_time == 0).OnlyEnforceIf(is_0830)
            model.Add(start_day_time != 0).OnlyEnforceIf(is_0830.Not())
            
            # Eğer 08:30 değilse ceza puanı ekle (Örn: 50 Puan)
            penalty_var = model.NewIntVar(0, 50, f'pen_0830_{task_id_counter}')
            model.Add(penalty_var == 50).OnlyEnforceIf(is_0830.Not())
            model.Add(penalty_var == 0).OnlyEnforceIf(is_0830)
            optimization_penalties.append(penalty_var)

        # ==========================================
        # OPTİMİZASYON KURALI 2: ÖĞLE ARASI (12:30) KORUMASI
        # ==========================================
        # 12:30 (4. index) slotuna ders gelirse ceza yazalım.
        # Dersin aralığı: [start_day_time, start_day_time + duration)
        # Eğer bu aralık 4'ü (12:30) kapsıyorsa ceza ver.
        # Kapsama mantığı: (start <= 4) VE (end > 4)
        
        covers_lunch = model.NewBoolVar(f'lunch_{task_id_counter}')
        
        # Mantık: Start <= 4
        s_le_4 = model.NewBoolVar(f's_le_4_{task_id_counter}')
        model.Add(start_day_time <= 4).OnlyEnforceIf(s_le_4)
        model.Add(start_day_time > 4).OnlyEnforceIf(s_le_4.Not())
        
        # Mantık: End > 4 (yani start + duration > 4)
        e_gt_4 = model.NewBoolVar(f'e_gt_4_{task_id_counter}')
        model.Add(start_day_time + duration > 4).OnlyEnforceIf(e_gt_4)
        model.Add(start_day_time + duration <= 4).OnlyEnforceIf(e_gt_4.Not())
        
        # İkisi de doğruysa öğle arasını yiyordur
        model.AddBoolAnd([s_le_4, e_gt_4]).OnlyEnforceIf(covers_lunch)
        model.AddBoolOr([s_le_4.Not(), e_gt_4.Not()]).OnlyEnforceIf(covers_lunch.Not())
        
        # Ceza (Örn: 20 Puan)
        lunch_pen = model.NewIntVar(0, 20, f'pen_lunch_{task_id_counter}')
        model.Add(lunch_pen == 20).OnlyEnforceIf(covers_lunch)
        model.Add(lunch_pen == 0).OnlyEnforceIf(covers_lunch.Not())
        optimization_penalties.append(lunch_pen)

        current_course_ids.append(task_id_counter)
        task_id_counter += 1

    # --- HİBRİT DERS (Teorik + Lab) KISITLARI (Değişmedi) ---
    if len(current_course_ids) == 2:
        task1 = all_tasks[current_course_ids[0]]
        task2 = all_tasks[current_course_ids[1]]
        teorik_task = task1 if task1['type'] == 'teorik' else task2
        lab_task = task1 if task1['type'] == 'lab' else task2
        
        model.Add(teorik_task['end'] == lab_task['start'])
        
        day_teorik = model.NewIntVar(0, NUM_DAYS - 1, f'day_chk_t_{current_course_ids[0]}')
        day_lab = model.NewIntVar(0, NUM_DAYS - 1, f'day_chk_l_{current_course_ids[1]}')
        model.AddDivisionEquality(day_teorik, teorik_task['start'], NUM_SLOTS)
        model.AddDivisionEquality(day_lab, lab_task['start'], NUM_SLOTS)
        model.Add(day_teorik == day_lab)

# ---------------------------------------------------------
# B. STANDART KISITLAR (Aynen Korundu)
# ---------------------------------------------------------
for t_ints in teacher_intervals.values():
    if len(t_ints) > 1: model.AddNoOverlap(t_ints)

for r_idx, r_ints in room_intervals.items():
    if ODALAR[r_idx]['oda_id'] != "ONLINE" and len(r_ints) > 1:
        model.AddNoOverlap(r_ints)

for g_ints in student_group_intervals.values():
    if len(g_ints) > 1: model.AddNoOverlap(g_ints)

# Hoca Günleri ve Sınıf Seviyesi Kısıtları (Önceki kodun aynısı)
gun_map = {g: i for i, g in enumerate(GUNLER)}
for hoca in HOCALAR:
    if 'musait_gunler' not in hoca: continue
    allowed_days = [gun_map[g] for g in hoca['musait_gunler'] if g in gun_map]
    if not allowed_days: continue
    forbidden = []
    for d in range(NUM_DAYS):
        if d not in allowed_days:
            forbidden.extend(range(d * NUM_SLOTS, (d + 1) * NUM_SLOTS))
    for t in all_tasks.values():
        if t['info']['hoca_id'] == hoca['hoca_id']:
            for f_slot in forbidden:
                model.Add(t['start'] != f_slot)

tasks_by_level = {}
for t in all_tasks.values():
    tasks_by_level.setdefault(t['info']['sinif_seviyesi'], []).append(t)
for tasks in tasks_by_level.values():
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            t1, t2 = tasks[i], tasks[j]
            s1, s2 = t1['info']['şube'], t2['info']['şube']
            if "Tek" in (s1, s2) or s1 == s2:
                model.AddNoOverlap([t1['interval'], t2['interval']])

# ==========================================
# EK KISIT 6 GÜNCELLENDİ: SOFT CONSTRAINT (CEZA PUANI)
# GÜNLÜK KREDİ LİMİTİ ARTIK YASAKLAMIYOR, CEZA YAZIYOR
# ==========================================


SOFT_LIMIT = 6   # 6'yı geçersen ceza başlar
HARD_LIMIT = 10  # 10 fiziksel sınır (asla geçemez)

# 1. Day index değişkenlerini hazırla
for t_id, task in all_tasks.items():
    day_idx_var = model.NewIntVar(0, NUM_DAYS - 1, f'day_idx_{t_id}')
    model.AddDivisionEquality(day_idx_var, task['start'], NUM_SLOTS)
    task['day_idx_var'] = day_idx_var

# 2. Grupları hazırla
grup_dersleri = {}
for t_id, task in all_tasks.items():
    info = task['info']
    seviye = info['sinif_seviyesi']
    sube = info['şube']
    kredi_degeri = info['kredi']
    if task['type'] == 'lab' and info.get('teorik_slot', 0) > 0:
        kredi_degeri = 0 
    
    etkilenen_gruplar = []
    if sube == "Tek":
        etkilenen_gruplar = [f"{seviye}-A", f"{seviye}-B"]
    else:
        etkilenen_gruplar = [f"{seviye}-{sube}"]
        
    for grp in etkilenen_gruplar:
        if grp not in grup_dersleri: grup_dersleri[grp] = []
        grup_dersleri[grp].append({'day_var': task['day_idx_var'], 'credit': kredi_degeri})

# 3. Yük Hesapla ve Ceza Yaz
for grp, tasks in grup_dersleri.items():
    for d in range(NUM_DAYS):
        gunluk_toplam_vars = []
        
        for item in tasks:
            credit = item['credit']
            if credit == 0: continue
            
            # Bu ders bu gün var mı? (1 veya 0)
            is_on_day = model.NewBoolVar(f'load_{grp}_d{d}_t{item["day_var"].Name()}')
            model.Add(item['day_var'] == d).OnlyEnforceIf(is_on_day)
            model.Add(item['day_var'] != d).OnlyEnforceIf(is_on_day.Not())
            
            gunluk_toplam_vars.append(is_on_day * credit)
        
        if gunluk_toplam_vars:
            # O günkü toplam kredi
            total_daily_load = model.NewIntVar(0, 20, f'total_load_{grp}_{d}')
            model.Add(total_daily_load == sum(gunluk_toplam_vars))
            
            # HARD LIMIT (Yasak - Fiziksel sınır)
            model.Add(total_daily_load <= HARD_LIMIT)
            
            # SOFT LIMIT (Ceza - Tercih)
            # Eğer 6'yı geçerse, (Total - 6) kadar ceza puanı ekle
            # Örn: 8 kredi -> 2 birim ceza. Her birim 10 puan olsun.
            excess_var = model.NewIntVar(0, 10, f'excess_{grp}_{d}')
            # excess >= total - 6  ve excess >= 0
            # Bu mantığı max(0, total-6) olarak kuruyoruz
            model.AddMaxEquality(excess_var, [0, total_daily_load - SOFT_LIMIT])
            
            # Cezayı listeye ekle (Her 1 fazla kredi için 10 ceza puanı)
            weight = 10
            # Puan = excess * 10
            # Çarpma işlemi için NewIntVar gerekebilir ama katsayıyı direct minimize'a verebiliriz.
            # Ancak listeye eklemek için ara değişken yapalım.
            cost_for_day = model.NewIntVar(0, 100, f'cost_{grp}_{d}')
            model.Add(cost_for_day == excess_var * weight)
            optimization_penalties.append(cost_for_day)

# ==========================================
# 3. ÇÖZÜM VE MINIMIZE (HEDEF FONKSİYONU)
# ==========================================
# Amacımız: Toplam ceza puanını SIFIRA yaklaştırmak
model.Minimize(sum(optimization_penalties))

solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = 20.0 # Süreyi biraz artırdım, optimizasyon düşünsün
"""status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Çözüm Bulundu: {solver.StatusName(status)}")
    
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "Program"
    
    # Stiller
    fill_header = PatternFill("solid", fgColor="4F81BD")
    fill_sub = PatternFill("solid", fgColor="DCE6F1")
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    border = Border(left=Side('thin'), right=Side('thin'), top=Side('thin'), bottom=Side('thin'))
    
    # Başlıklar
    ws.merge_cells("A1:A2"); ws['A1'] = "GÜN"; ws['A1'].fill = fill_header
    ws.merge_cells("B1:B2"); ws['B1'] = "SAAT"; ws['B1'].fill = fill_header
    
    col_map = {}
    curr_col = 3
    for sinif in sorted(list(set(d['sinif_seviyesi'] for d in DERSLER))):
        ws.merge_cells(start_row=1, start_column=curr_col, end_row=1, end_column=curr_col+5)
        cell = ws.cell(1, curr_col, f"{sinif}. SINIF"); cell.fill = fill_header; cell.alignment = align_center
        
        for offset, grp in enumerate(["A", "B"]):
            base = curr_col + (offset * 3)
            col_map[(sinif, grp)] = base
            ws.cell(2, base, "Ders").fill = fill_sub
            ws.cell(2, base+1, "Hoca").fill = fill_sub
            ws.cell(2, base+2, "Yer").fill = fill_sub
        curr_col += 6

    row_map = {}
    r = 3
    for d_idx, gun in enumerate(GUNLER):
        ws.merge_cells(start_row=r, start_column=1, end_row=r+NUM_SLOTS-1, end_column=1)
        ws.cell(r, 1, gun).alignment = Alignment(text_rotation=90, horizontal="center", vertical="center")
        for s_idx, slot in enumerate(SLOTLAR):
            ws.cell(r, 2, slot)
            row_map[(d_idx, s_idx)] = r
            r += 1

    for t in all_tasks.values():
        start = solver.Value(t['start'])
        dur = t['info']['teorik_slot'] if t['type'] == 'teorik' else t['info']['lab_slot']
        
        r = row_map[(start // NUM_SLOTS, start % NUM_SLOTS)]
        c = col_map[(t['info']['sinif_seviyesi'], "B" if t['info']['şube'] == "B" else "A")]
        
        hoca_ad = next((h['hoca_ad'] for h in HOCALAR if h['hoca_id'] == t['info']['hoca_id']), "?")
        oda_ad = "?"
        for r_idx, lit in t['room_literals'].items():
            if solver.BooleanValue(lit): oda_ad = ODALAR[r_idx]['oda_ad']; break
            
        for offset, val in enumerate([t['info']['ders_ad'], hoca_ad, oda_ad]):
            ws.merge_cells(start_row=r, start_column=c+offset, end_row=r+dur-1, end_column=c+offset)
            cell = ws.cell(r, c+offset, val)
            cell.alignment = align_center
            cell.border = border
            if offset == 2: cell.font = Font(bold=True, color="FF0000")

    wb.save("Program.xlsx")
else:
    print("Çözüm Bulunamadı! (Hard Kısıtlar hala çok sıkı olabilir)")"""


import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# ... (Solver çözümü ve model.Minimize kısmı yukarıda aynı kalıyor) ...

# ÇÖZÜMÜ BAŞLAT
status = solver.Solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"Çözüm Bulundu: {solver.StatusName(status)}")
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ders Programi"

    # ==========================================
    # 1. AYARLAR VE STİLLER
    # ==========================================
    COLOR_HEADER_BG = "4F81BD"  
    COLOR_SUB_BG = "DCE6F1"     
    COLOR_BORDER = "000000"     

    # Font Ayarları (İçerik fontunu küçülttüm: Size 8)
    font_main_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_sub_header = Font(name="Calibri", size=9, bold=True, color="000000")
    font_day = Font(name="Calibri", size=11, bold=True, color="000000")
    font_slot = Font(name="Calibri", size=9, bold=False, color="000000")
    font_content = Font(name="Calibri", size=8, bold=False, color="000000") 

    # Alignment Ayarları (Shrink to Fit: Sığacak şekilde küçült)
    align_header = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    # İÇERİK İÇİN: Wrap text FALSE, Shrink to Fit TRUE
    align_content = Alignment(horizontal="center", vertical="center", wrap_text=False, shrink_to_fit=True)
    
    align_vertical = Alignment(horizontal="center", vertical="center", text_rotation=90, wrap_text=True)

    # Kenarlıklar (Standart İnce)
    thin = Side(border_style="thin", color=COLOR_BORDER)
    medium = Side(border_style="medium", color=COLOR_BORDER) # Gün ayrımları için kalın
    
    border_all = Border(left=thin, right=thin, top=thin, bottom=thin)
    border_thick_bottom = Border(left=thin, right=thin, top=thin, bottom=medium) # Gün bitimi için

    # Listeler
    sorted_siniflar = sorted(list(set(d['sinif_seviyesi'] for d in DERSLER)))
    
    col_map = {} 
    row_map = {} 

    # ==========================================
    # 2. BAŞLIK YAPISI (HEADER)
    # ==========================================

    # A1:A2 -> GÜN
    ws.merge_cells("A1:A2"); ws["A1"] = "GÜN"
    ws["A1"].fill = PatternFill("solid", fgColor=COLOR_HEADER_BG)
    ws["A1"].font = font_main_header
    ws["A1"].alignment = align_header
    ws["A1"].border = border_all
    ws["A2"].border = border_all

    # B1:B2 -> SAAT
    ws.merge_cells("B1:B2"); ws["B1"] = "SAAT"
    ws["B1"].fill = PatternFill("solid", fgColor=COLOR_HEADER_BG)
    ws["B1"].font = font_main_header
    ws["B1"].alignment = align_header
    ws["B1"].border = border_all
    ws["B2"].border = border_all

    current_col = 3 
    class_columns = [] 

    for i, sinif in enumerate(sorted_siniflar):
        start_char = get_column_letter(current_col)
        end_char = get_column_letter(current_col + 5)
        
        ws.merge_cells(f"{start_char}1:{end_char}1")
        cell = ws.cell(1, current_col, f"{sinif}. SINIF")
        cell.fill = PatternFill("solid", fgColor=COLOR_HEADER_BG)
        cell.font = font_main_header
        cell.alignment = align_header
        cell.border = border_all
        
        col_map[(sinif, "A")] = current_col
        col_map[(sinif, "B")] = current_col + 3

        for c in range(current_col, current_col + 6):
            ws.cell(1, c).border = border_all
            class_columns.append(c) # Border çizilecek sütunlar listesi

        sub_headers = ["Dersin Adı", "Öğr. Elemanı", "Yer"] * 2 
        
        for k, header_text in enumerate(sub_headers):
            c_idx = current_col + k
            cell = ws.cell(2, c_idx, header_text)
            cell.fill = PatternFill("solid", fgColor=COLOR_SUB_BG)
            cell.font = font_sub_header
            cell.alignment = align_header
            cell.border = border_all
            
            # SÜTUN GENİŞLİKLERİ (Biraz daha artırdım sığsın diye)
            col_let = get_column_letter(c_idx)
            if "Yer" in header_text:
                ws.column_dimensions[col_let].width = 6 
            elif "Ders" in header_text:
                ws.column_dimensions[col_let].width = 22 # Ders adı uzun olabilir
            else:
                ws.column_dimensions[col_let].width = 16 # Hoca adı

        current_col += 6 

        if i < len(sorted_siniflar) - 1:
            gap_col_letter = get_column_letter(current_col)
            ws.column_dimensions[gap_col_letter].width = 2
            current_col += 1 

    # ==========================================
    # 3. SATIR YAPISI VE IZGARA ÇİZİMİ
    # ==========================================
    
    row_num = 3 
    
    for d_idx, gun in enumerate(GUNLER):
        start_row = row_num
        
        for s_idx, slot in enumerate(SLOTLAR):
            row_map[(d_idx, s_idx)] = row_num

            # Saat Hücresi
            cell_slot = ws.cell(row_num, 2, slot)
            cell_slot.font = font_slot
            cell_slot.alignment = align_header
            
            # Bu günün son slotu mu?
            is_last_slot_of_day = (s_idx == len(SLOTLAR) - 1)
            
            # Kenarlık Tipi Belirle (Günün sonuysa altı kalın olsun)
            current_border = border_thick_bottom if is_last_slot_of_day else border_all
            
            cell_slot.border = current_border
            
            # --- TÜM DERS HÜCRELERİNE BOŞ KENARLIK ÇİZ ---
            # Bu döngü sayesinde çizgilerdeki "biri kalın biri ince" hatası düzelir.
            # Her hücreye standart ince çizgi çekiyoruz.
            for c in class_columns:
                cell_grid = ws.cell(row_num, c)
                cell_grid.border = current_border
            
            row_num += 1
        
        # Gün İsmi
        end_row = row_num - 1
        ws.merge_cells(start_row=start_row, start_column=1, end_row=end_row, end_column=1)
        cell_day = ws.cell(start_row, 1, gun)
        cell_day.font = font_day
        cell_day.alignment = align_vertical
        
        # Gün hücresinin tüm kenarlarına border verelim
        # Merge olduğu için sol üst köşeye vermemiz yeterli ama stili düzeltmek gerekebilir
        cell_day.border = border_all # Varsayılan ince
        
        # Günler arası boşluk (Görsel temizliği için)
        if gun != GUNLER[-1]:
             row_num += 1 

    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 13

    # ==========================================
    # 4. VERİLERİ YERLEŞTİRME
    # ==========================================
   

    for t_key, t_val in all_tasks.items():
        start_val = solver.Value(t_val['start'])
        duration = t_val['info']['teorik_slot'] if t_val['type'] == 'teorik' else t_val['info']['lab_slot']
        
        ders_ad = t_val['info']['ders_ad']
        hoca_ad = next((h['hoca_ad'] for h in HOCALAR if h['hoca_id'] == t_val['info']['hoca_id']), "?")
        
        oda_ad = "?"
        for r_idx, lit in t_val['room_literals'].items():
            if solver.BooleanValue(lit):
                oda_ad = ODALAR[r_idx]['oda_ad']
                break

        sinif_level = t_val['info']['sinif_seviyesi']
        sube = t_val['info']['şube']
        target_sube = "B" if sube == "B" else "A"
        
        if (sinif_level, target_sube) not in col_map: continue
            
        base_col = col_map[(sinif_level, target_sube)]

        for i in range(duration):
            current_abs_slot = start_val + i
            day_idx = current_abs_slot // NUM_SLOTS 
            slot_idx = current_abs_slot % NUM_SLOTS
            
            if (day_idx, slot_idx) in row_map:
                r = row_map[(day_idx, slot_idx)]
                
                # O satırın border stilini korumak için mevcut border'ı alabiliriz
                # ama zaten yukarıda hepsine border_all veya border_thick_bottom verdik.
                # Tekrar border tanımlamaya gerek yok, sadece içeriği ve alignment'ı basacağız.
                # Ancak openpyxl bazen stil üzerine yazınca border'ı sıfırlayabilir,
                # o yüzden border'ı tekrar set etmek garanti olur.
                
                is_last_slot = (slot_idx == NUM_SLOTS - 1)
                curr_border = border_thick_bottom if is_last_slot else border_all

                # 1. Ders Adı
                c1 = ws.cell(r, base_col, ders_ad)
                c1.alignment = align_content # Shrink to Fit BURADA
                c1.font = font_content
                c1.border = curr_border
                
                # 2. Hoca Adı
                c2 = ws.cell(r, base_col + 1, hoca_ad)
                c2.alignment = align_content # Shrink to Fit BURADA
                c2.font = font_content
                c2.border = curr_border
                
                # 3. Yer
                c3 = ws.cell(r, base_col + 2, oda_ad)
                c3.alignment = align_content 
                c3.font = Font(name="Calibri", size=8, bold=True, color="FF0000")
                c3.border = curr_border

    # Dosyayı Kaydet
    output_filename = "Final_Program.xlsx"
    wb.save(output_filename)
    