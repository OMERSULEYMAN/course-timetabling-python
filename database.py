import sqlite3
import json
from typing import List, Optional
from datetime import datetime
from models import Hoca, Oda, Ders, Program


class DatabaseManager:
    def __init__(self, db_path: str = "scheduler.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS programs (
                program_id INTEGER PRIMARY KEY AUTOINCREMENT,
                program_adi TEXT NOT NULL,
                aciklama TEXT,
                olusturma_tarihi TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Teachers tablosu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                hoca_id INTEGER NOT NULL,
                hoca_ad TEXT NOT NULL,
                musait_gunler TEXT NOT NULL,
                program_id INTEGER NOT NULL,
                FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
                UNIQUE(program_id, hoca_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                oda_id TEXT NOT NULL,
                oda_ad TEXT NOT NULL,
                tip TEXT NOT NULL,
                program_id INTEGER NOT NULL,
                FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
                UNIQUE(program_id, oda_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ders_id INTEGER NOT NULL,
                ders_ad TEXT NOT NULL,
                kredi INTEGER NOT NULL,
                şube TEXT NOT NULL,
                hoca_id INTEGER NOT NULL,
                teorik_slot INTEGER DEFAULT 0,
                lab_slot INTEGER DEFAULT 0,
                ue INTEGER DEFAULT 0,
                sinif_seviyesi INTEGER NOT NULL,
                akts INTEGER,
                zorunlu INTEGER,
                program_id INTEGER NOT NULL,
                FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
                FOREIGN KEY (hoca_id) REFERENCES teachers(hoca_id),
                UNIQUE(program_id, ders_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_program(self, program_adi: str, aciklama: Optional[str] = None) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO programs (program_adi, aciklama, olusturma_tarihi)
            VALUES (?, ?, ?)
        """, (program_adi, aciklama, datetime.now().isoformat()))
        program_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return program_id
    
    def get_all_programs(self) -> List[Program]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM programs ORDER BY olusturma_tarihi DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [Program(
            program_id=row['program_id'],
            program_adi=row['program_adi'],
            aciklama=row['aciklama'],
            olusturma_tarihi=row['olusturma_tarihi']
        ) for row in rows]
    
    def get_program(self, program_id: int) -> Optional[Program]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM programs WHERE program_id = ?", (program_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Program(
                program_id=row['program_id'],
                program_adi=row['program_adi'],
                aciklama=row['aciklama'],
                olusturma_tarihi=row['olusturma_tarihi']
            )
        return None
    
    def delete_program(self, program_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM programs WHERE program_id = ?", (program_id,))
        conn.commit()
        conn.close()
    
    def get_next_teacher_id(self, program_id: int) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(MAX(hoca_id), 0) + 1 as next_id
            FROM teachers
            WHERE program_id = ?
        """, (program_id,))
        row = cursor.fetchone()
        conn.close()
        return row['next_id'] if row else 1
    
    def add_teacher(self, hoca: Hoca, auto_id: bool = True):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if auto_id and (hoca.hoca_id is None or hoca.hoca_id == 0):
            hoca.hoca_id = self.get_next_teacher_id(hoca.program_id)
        
        cursor.execute("""
            INSERT OR REPLACE INTO teachers (hoca_id, hoca_ad, musait_gunler, program_id)
            VALUES (?, ?, ?, ?)
        """, (hoca.hoca_id, hoca.hoca_ad, json.dumps(hoca.musait_gunler), hoca.program_id))
        conn.commit()
        conn.close()
    
    def get_teachers(self, program_id: int) -> List[Hoca]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers WHERE program_id = ?", (program_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Hoca(
            hoca_id=row['hoca_id'],
            hoca_ad=row['hoca_ad'],
            musait_gunler=json.loads(row['musait_gunler']),
            program_id=row['program_id']
        ) for row in rows]
    
    def delete_teacher(self, program_id: int, hoca_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM teachers WHERE program_id = ? AND hoca_id = ?", 
                      (program_id, hoca_id))
        conn.commit()
        conn.close()
    
    def get_next_room_id(self, program_id: int) -> str:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT oda_id FROM rooms
            WHERE program_id = ?
        """, (program_id,))
        rows = cursor.fetchall()
        conn.close()
        
        max_num = 0
        for row in rows:
            oda_id = row['oda_id']
            try:
                if oda_id.startswith('D') and len(oda_id) > 1:
                    num = int(oda_id[1:])
                    max_num = max(max_num, num)
            except:
                pass
        
        return f"D{max_num + 1:03d}"
    
    def add_room(self, oda: Oda, auto_id: bool = True):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if auto_id and (not oda.oda_id or oda.oda_id.strip() == ""):
            oda.oda_id = self.get_next_room_id(oda.program_id)
        
        cursor.execute("""
            INSERT OR REPLACE INTO rooms (oda_id, oda_ad, tip, program_id)
            VALUES (?, ?, ?, ?)
        """, (oda.oda_id, oda.oda_ad, oda.tip, oda.program_id))
        conn.commit()
        conn.close()
    
    def get_rooms(self, program_id: int) -> List[Oda]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE program_id = ?", (program_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [Oda(
            oda_id=row['oda_id'],
            oda_ad=row['oda_ad'],
            tip=row['tip'],
            program_id=row['program_id']
        ) for row in rows]
    
    def delete_room(self, program_id: int, oda_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rooms WHERE program_id = ? AND oda_id = ?", 
                      (program_id, oda_id))
        conn.commit()
        conn.close()
    
    def get_next_lesson_id(self, program_id: int) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(MAX(ders_id), 0) + 1 as next_id
            FROM lessons
            WHERE program_id = ?
        """, (program_id,))
        row = cursor.fetchone()
        conn.close()
        return row['next_id'] if row else 1
    
    def add_lesson(self, ders: Ders, auto_id: bool = True):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if auto_id and (ders.ders_id is None or ders.ders_id == 0):
            ders.ders_id = self.get_next_lesson_id(ders.program_id)
        
        cursor.execute("""
            INSERT OR REPLACE INTO lessons (
                ders_id, ders_ad, kredi, şube, hoca_id, teorik_slot, lab_slot,
                ue, sinif_seviyesi, akts, zorunlu, program_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ders.ders_id, ders.ders_ad, ders.kredi, ders.şube, ders.hoca_id,
            ders.teorik_slot, ders.lab_slot, 1 if ders.ue else 0,
            ders.sinif_seviyesi, ders.akts, 1 if ders.zorunlu else 0 if ders.zorunlu is not None else None,
            ders.program_id
        ))
        conn.commit()
        conn.close()
    
    def get_lessons(self, program_id: int) -> List[Ders]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lessons WHERE program_id = ?", (program_id,))
        rows = cursor.fetchall()
        conn.close()
        
        lessons = []
        for row in rows:
            lessons.append(Ders(
                ders_id=row['ders_id'],
                ders_ad=row['ders_ad'],
                kredi=row['kredi'],
                şube=row['şube'],
                hoca_id=row['hoca_id'],
                teorik_slot=row['teorik_slot'],
                lab_slot=row['lab_slot'],
                ue=bool(row['ue']),
                sinif_seviyesi=row['sinif_seviyesi'],
                program_id=row['program_id'],
                akts=row['akts'],
                zorunlu=bool(row['zorunlu']) if row['zorunlu'] is not None else None
            ))
        return lessons
    
    def delete_lesson(self, program_id: int, ders_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lessons WHERE program_id = ? AND ders_id = ?", 
                      (program_id, ders_id))
        conn.commit()
        conn.close()

