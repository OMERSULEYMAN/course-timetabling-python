from ortools.sat.python import cp_model
from typing import List, Dict, Tuple, Optional
from database import DatabaseManager
from models import Hoca, Oda, Ders

GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
SLOTLAR = ["08:30", "09:30", "10:30", "11:30", "12:30", "13:30", "14:30", "15:30", "16:30", "17:30"]
NUM_DAYS, NUM_SLOTS = len(GUNLER), len(SLOTLAR)
TOTAL_SLOTS = NUM_DAYS * NUM_SLOTS

SOFT_LIMIT = 6
HARD_LIMIT = 10


class SchedulerEngine:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        self.model = None
        self.solver = None
        self.all_tasks = {}
        self.room_intervals = {}
        self.teacher_intervals = {}
        self.student_group_intervals = {}
        self.optimization_penalties = []
    
    def load_data(self, program_id: int) -> Tuple[List[Ders], List[Oda], List[Hoca]]:
        dersler = self.db.get_lessons(program_id)
        odalar = self.db.get_rooms(program_id)
        hocalar = self.db.get_teachers(program_id)
        return dersler, odalar, hocalar
    
    def solve(self, program_id: int, max_time_seconds: float = 20.0) -> Tuple[str, Optional[Dict]]:
        dersler, odalar, hocalar = self.load_data(program_id)
        
        if not dersler or not odalar or not hocalar:
            return "INFEASIBLE", None
        
        DERSLER = [d.to_dict() for d in dersler]
        ODALAR = [o.to_dict() for o in odalar]
        HOCALAR = [h.to_dict() for h in hocalar]
        
        self._build_model(DERSLER, ODALAR, HOCALAR)
        
        self.solver = cp_model.CpSolver()
        self.solver.parameters.max_time_in_seconds = max_time_seconds
        
        status = self.solver.Solve(self.model)
        status_name = self.solver.StatusName(status)
        
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            solution = self._extract_solution(DERSLER, ODALAR, HOCALAR)
            total_penalty = self.solver.ObjectiveValue()
            penalty_details = self._analyze_penalties()
            solution['total_penalty'] = int(total_penalty)
            solution['penalty_details'] = penalty_details
            return status_name, solution
        else:
            return status_name, None
    
    def _build_model(self, DERSLER: List[Dict], ODALAR: List[Dict], HOCALAR: List[Dict]):
        """CP-SAT modelini kur (Mevcut mantık korunmuştur)"""
        self.model = cp_model.CpModel()
        self.all_tasks = {}
        self.room_intervals = {i: [] for i in range(len(ODALAR))}
        self.teacher_intervals = {h['hoca_id']: [] for h in HOCALAR}
        self.student_group_intervals = {}
        self.optimization_penalties = []
        
        task_id_counter = 0
        
        for ders in DERSLER:
            components = []
            if ders.get('teorik_slot', 0) > 0:
                components.append({
                    'type': 'teorik',
                    'duration': ders['teorik_slot'],
                    'room_type': 'ue' if ders['ue'] else 'teorik'
                })
            if ders.get('lab_slot', 0) > 0:
                components.append({
                    'type': 'lab',
                    'duration': ders['lab_slot'],
                    'room_type': 'lab'
                })
            
            current_course_ids = []
            
            for comp in components:
                duration = comp['duration']
                req_type = comp['room_type']
                
                start_var = self.model.NewIntVar(0, TOTAL_SLOTS - duration, f'start_{task_id_counter}')
                end_var = self.model.NewIntVar(0, TOTAL_SLOTS, f'end_{task_id_counter}')
                interval_var = self.model.NewIntervalVar(start_var, duration, end_var, f'int_{task_id_counter}')
                
                start_day_time = self.model.NewIntVar(0, NUM_SLOTS - 1, f'day_time_{task_id_counter}')
                self.model.AddModuloEquality(start_day_time, start_var, NUM_SLOTS)
                self.model.Add(start_day_time + duration <= NUM_SLOTS)
                
                possible_rooms = [i for i, r in enumerate(ODALAR) if r['tip'] == req_type]
                room_lits = []
                for r_idx in possible_rooms:
                    lit = self.model.NewBoolVar(f't_{task_id_counter}_r_{r_idx}')
                    room_lits.append(lit)
                    self.room_intervals[r_idx].append(
                        self.model.NewOptionalIntervalVar(start_var, duration, end_var, lit, f'opt_{task_id_counter}_{r_idx}')
                    )
                
                self.model.Add(sum(room_lits) == 1)
                
                self.all_tasks[task_id_counter] = {
                    'info': ders,
                    'type': comp['type'],
                    'start': start_var,
                    'end': end_var,
                    'interval': interval_var,
                    'room_literals': dict(zip(possible_rooms, room_lits)),
                    'start_day_time': start_day_time
                }
                
                self.teacher_intervals[ders['hoca_id']].append(interval_var)
                
                seviye, sube = ders['sinif_seviyesi'], ders['şube']
                groups = [f"{seviye}-A", f"{seviye}-B"] if sube == "Tek" else [f"{seviye}-{sube}"]
                for g in groups:
                    self.student_group_intervals.setdefault(g, []).append(interval_var)
                
                if duration >= 4:
                    is_0830 = self.model.NewBoolVar(f'is_0830_{task_id_counter}')
                    self.model.Add(start_day_time == 0).OnlyEnforceIf(is_0830)
                    self.model.Add(start_day_time != 0).OnlyEnforceIf(is_0830.Not())
                    
                    penalty_var = self.model.NewIntVar(0, 50, f'pen_0830_{task_id_counter}')
                    self.model.Add(penalty_var == 50).OnlyEnforceIf(is_0830.Not())
                    self.model.Add(penalty_var == 0).OnlyEnforceIf(is_0830)
                    self.optimization_penalties.append(penalty_var)
                
                # OPTİMİZASYON KURALI 2: ÖĞLE ARASI KORUMASI
                covers_lunch = self.model.NewBoolVar(f'lunch_{task_id_counter}')
                
                s_le_4 = self.model.NewBoolVar(f's_le_4_{task_id_counter}')
                self.model.Add(start_day_time <= 4).OnlyEnforceIf(s_le_4)
                self.model.Add(start_day_time > 4).OnlyEnforceIf(s_le_4.Not())
                
                e_gt_4 = self.model.NewBoolVar(f'e_gt_4_{task_id_counter}')
                self.model.Add(start_day_time + duration > 4).OnlyEnforceIf(e_gt_4)
                self.model.Add(start_day_time + duration <= 4).OnlyEnforceIf(e_gt_4.Not())
                
                self.model.AddBoolAnd([s_le_4, e_gt_4]).OnlyEnforceIf(covers_lunch)
                self.model.AddBoolOr([s_le_4.Not(), e_gt_4.Not()]).OnlyEnforceIf(covers_lunch.Not())
                
                lunch_pen = self.model.NewIntVar(0, 20, f'pen_lunch_{task_id_counter}')
                self.model.Add(lunch_pen == 20).OnlyEnforceIf(covers_lunch)
                self.model.Add(lunch_pen == 0).OnlyEnforceIf(covers_lunch.Not())
                self.optimization_penalties.append(lunch_pen)
                
                current_course_ids.append(task_id_counter)
                task_id_counter += 1
            
            if len(current_course_ids) == 2:
                task1 = self.all_tasks[current_course_ids[0]]
                task2 = self.all_tasks[current_course_ids[1]]
                teorik_task = task1 if task1['type'] == 'teorik' else task2
                lab_task = task1 if task1['type'] == 'lab' else task2
                
                self.model.Add(teorik_task['end'] == lab_task['start'])
                
                day_teorik = self.model.NewIntVar(0, NUM_DAYS - 1, f'day_chk_t_{current_course_ids[0]}')
                day_lab = self.model.NewIntVar(0, NUM_DAYS - 1, f'day_chk_l_{current_course_ids[1]}')
                self.model.AddDivisionEquality(day_teorik, teorik_task['start'], NUM_SLOTS)
                self.model.AddDivisionEquality(day_lab, lab_task['start'], NUM_SLOTS)
                self.model.Add(day_teorik == day_lab)
        
        for t_ints in self.teacher_intervals.values():
            if len(t_ints) > 1:
                self.model.AddNoOverlap(t_ints)
        
        for r_idx, r_ints in self.room_intervals.items():
            if ODALAR[r_idx]['oda_id'] != "ONLINE" and len(r_ints) > 1:
                self.model.AddNoOverlap(r_ints)
        
        for g_ints in self.student_group_intervals.values():
            if len(g_ints) > 1:
                self.model.AddNoOverlap(g_ints)
        
        gun_map = {g: i for i, g in enumerate(GUNLER)}
        for hoca in HOCALAR:
            if 'musait_gunler' not in hoca:
                continue
            allowed_days = [gun_map[g] for g in hoca['musait_gunler'] if g in gun_map]
            if not allowed_days:
                continue
            forbidden = []
            for d in range(NUM_DAYS):
                if d not in allowed_days:
                    forbidden.extend(range(d * NUM_SLOTS, (d + 1) * NUM_SLOTS))
            for t in self.all_tasks.values():
                if t['info']['hoca_id'] == hoca['hoca_id']:
                    for f_slot in forbidden:
                        self.model.Add(t['start'] != f_slot)
        
        # Sınıf Seviyesi Kısıtları
        tasks_by_level = {}
        for t in self.all_tasks.values():
            tasks_by_level.setdefault(t['info']['sinif_seviyesi'], []).append(t)
        for tasks in tasks_by_level.values():
            for i in range(len(tasks)):
                for j in range(i + 1, len(tasks)):
                    t1, t2 = tasks[i], tasks[j]
                    s1, s2 = t1['info']['şube'], t2['info']['şube']
                    if "Tek" in (s1, s2) or s1 == s2:
                        self.model.AddNoOverlap([t1['interval'], t2['interval']])
        
        for t_id, task in self.all_tasks.items():
            day_idx_var = self.model.NewIntVar(0, NUM_DAYS - 1, f'day_idx_{t_id}')
            self.model.AddDivisionEquality(day_idx_var, task['start'], NUM_SLOTS)
            task['day_idx_var'] = day_idx_var
        
        grup_dersleri = {}
        for t_id, task in self.all_tasks.items():
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
                if grp not in grup_dersleri:
                    grup_dersleri[grp] = []
                grup_dersleri[grp].append({'day_var': task['day_idx_var'], 'credit': kredi_degeri})
        
        for grp, tasks in grup_dersleri.items():
            for d in range(NUM_DAYS):
                gunluk_toplam_vars = []
                
                for item in tasks:
                    credit = item['credit']
                    if credit == 0:
                        continue
                    
                    is_on_day = self.model.NewBoolVar(f'load_{grp}_d{d}_t{item["day_var"].Name()}')
                    self.model.Add(item['day_var'] == d).OnlyEnforceIf(is_on_day)
                    self.model.Add(item['day_var'] != d).OnlyEnforceIf(is_on_day.Not())
                    
                    gunluk_toplam_vars.append(is_on_day * credit)
                
                if gunluk_toplam_vars:
                    total_daily_load = self.model.NewIntVar(0, 20, f'total_load_{grp}_{d}')
                    self.model.Add(total_daily_load == sum(gunluk_toplam_vars))
                    
                    # HARD LIMIT
                    self.model.Add(total_daily_load <= HARD_LIMIT)
                    
                    # SOFT LIMIT
                    excess_var = self.model.NewIntVar(0, 10, f'excess_{grp}_{d}')
                    self.model.AddMaxEquality(excess_var, [0, total_daily_load - SOFT_LIMIT])
                    
                    weight = 10
                    cost_for_day = self.model.NewIntVar(0, 100, f'cost_{grp}_{d}')
                    self.model.Add(cost_for_day == excess_var * weight)
                    self.optimization_penalties.append(cost_for_day)
        
        self.model.Minimize(sum(self.optimization_penalties))
    
    def _extract_solution(self, DERSLER: List[Dict], ODALAR: List[Dict], HOCALAR: List[Dict]) -> Dict:
        all_class_levels = sorted(list(set(d['sinif_seviyesi'] for d in DERSLER)))
        
        solution = {
            'tasks': [],
            'gunler': GUNLER,
            'slotlar': SLOTLAR,
            'all_class_levels': all_class_levels  # Excel exporter için
        }
        
        hoca_map = {h['hoca_id']: h['hoca_ad'] for h in HOCALAR}
        
        for t_id, task in self.all_tasks.items():
            start_val = self.solver.Value(task['start'])
            duration = task['info']['teorik_slot'] if task['type'] == 'teorik' else task['info']['lab_slot']
            
            # Oda bul
            oda_ad = "?"
            for r_idx, lit in task['room_literals'].items():
                if self.solver.BooleanValue(lit):
                    oda_ad = ODALAR[r_idx]['oda_ad']
                    break
            
            day_idx = start_val // NUM_SLOTS
            slot_idx = start_val % NUM_SLOTS
            
            solution['tasks'].append({
                'task_id': t_id,
                'ders_id': task['info']['ders_id'],
                'ders_ad': task['info']['ders_ad'],
                'hoca_id': task['info']['hoca_id'],
                'hoca_ad': hoca_map.get(task['info']['hoca_id'], "?"),
                'oda_ad': oda_ad,
                'type': task['type'],
                'sinif_seviyesi': task['info']['sinif_seviyesi'],
                'şube': task['info']['şube'],
                'day_idx': day_idx,
                'slot_idx': slot_idx,
                'duration': duration,
                'start_slot': start_val
            })
        
        return solution
    
    def _analyze_penalties(self) -> Dict:
        details = {
            'big_course_penalty': 0,
            'lunch_penalty': 0,
            'daily_load_penalty': 0,
            'big_course_list': [],
            'lunch_violations': [],
            'daily_load_violations': []
        }
        
        for t_id, task in self.all_tasks.items():
            duration = task['info']['teorik_slot'] if task['type'] == 'teorik' else task['info']['lab_slot']
            if duration >= 4:
                start_day_time = self.solver.Value(task['start_day_time'])
                if start_day_time != 0:
                    details['big_course_penalty'] += 50
                    day_idx = self.solver.Value(task['day_idx_var'])
                    details['big_course_list'].append({
                        'ders_ad': task['info']['ders_ad'],
                        'sinif_seviyesi': task['info']['sinif_seviyesi'],
                        'gun': GUNLER[day_idx],
                        'şube': task['info']['şube']
                    })
        
        # Öğle arası koruması (C11) - 20 puan ceza
        for t_id, task in self.all_tasks.items():
            duration = task['info']['teorik_slot'] if task['type'] == 'teorik' else task['info']['lab_slot']
            start_day_time = self.solver.Value(task['start_day_time'])
            # Ders öğle arasını kapsıyor mu? (start <= 4 ve start + duration > 4)
            if start_day_time <= 4 and start_day_time + duration > 4:
                details['lunch_penalty'] += 20
                day_idx = self.solver.Value(task['day_idx_var'])
                details['lunch_violations'].append({
                    'ders_ad': task['info']['ders_ad'],
                    'sinif_seviyesi': task['info']['sinif_seviyesi'],
                    'gun': GUNLER[day_idx],
                    'şube': task['info']['şube']
                })
        
        daily_load_penalty = 0
        grup_dersleri = {}
        task_day_map = {}  # Her task için hangi gün ve hangi grup
        
        for t_id, task in self.all_tasks.items():
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
            
            day_idx = self.solver.Value(task['day_idx_var'])
            for grp in etkilenen_gruplar:
                if grp not in grup_dersleri:
                    grup_dersleri[grp] = {d: [] for d in range(NUM_DAYS)}  # Her gün için ders listesi
                if kredi_degeri > 0:
                    grup_dersleri[grp][day_idx].append({
                        'ders_ad': info['ders_ad'],
                        'kredi': kredi_degeri,
                        'şube': sube
                    })
                    task_day_map[(t_id, grp, day_idx)] = {
                        'ders_ad': info['ders_ad'],
                        'kredi': kredi_degeri,
                        'sinif_seviyesi': seviye,
                        'şube': sube
                    }
        
        for grp, daily_credits in grup_dersleri.items():
            sinif_seviyesi = int(grp.split('-')[0])
            for day, ders_listesi in daily_credits.items():
                total_credits = sum(d['kredi'] for d in ders_listesi)
                if total_credits > SOFT_LIMIT:
                    excess = total_credits - SOFT_LIMIT
                    daily_load_penalty += excess * 10
                    details['daily_load_violations'].append({
                        'sinif_seviyesi': sinif_seviyesi,
                        'gun': GUNLER[day],
                        'toplam_kredi': total_credits,
                        'fazla_kredi': excess,
                        'dersler': ders_listesi
                    })
        
        details['daily_load_penalty'] = daily_load_penalty
        
        return details

