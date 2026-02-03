import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from typing import Dict, List, Optional


class ExcelExporter:
    def __init__(self):
        self.GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        self.SLOTLAR = ["08:30", "09:30", "10:30", "11:30", "12:30", "13:30", "14:30", "15:30", "16:30", "17:30"]
        self.NUM_DAYS = len(self.GUNLER)
        self.NUM_SLOTS = len(self.SLOTLAR)
    
    def export(self, solution: Dict, output_filename: str = "Final_Program.xlsx", 
               all_class_levels: Optional[List[int]] = None):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Ders Programi"
        
        COLOR_HEADER_BG = "4F81BD"
        COLOR_SUB_BG = "DCE6F1"
        COLOR_BORDER = "000000"
        
        font_main_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        font_sub_header = Font(name="Calibri", size=9, bold=True, color="000000")
        font_day = Font(name="Calibri", size=11, bold=True, color="000000")
        font_slot = Font(name="Calibri", size=9, bold=False, color="000000")
        font_content = Font(name="Calibri", size=8, bold=False, color="000000")
        
        align_header = Alignment(horizontal="center", vertical="center", wrap_text=True)
        align_content = Alignment(horizontal="center", vertical="center", wrap_text=False, shrink_to_fit=True)
        align_vertical = Alignment(horizontal="center", vertical="center", text_rotation=90, wrap_text=True)
        
        thin = Side(border_style="thin", color=COLOR_BORDER)
        medium = Side(border_style="medium", color=COLOR_BORDER)
        
        border_all = Border(left=thin, right=thin, top=thin, bottom=thin)
        border_thick_bottom = Border(left=thin, right=thin, top=thin, bottom=medium)
        
        if all_class_levels is not None:
            sinif_seviyeleri = sorted(all_class_levels)
        else:
            sinif_seviyeleri = sorted(list(set(task['sinif_seviyesi'] for task in solution['tasks'])))
        
        col_map = {}
        row_map = {}
        ws.merge_cells("A1:A2")
        ws["A1"] = "GÜN"
        ws["A1"].fill = PatternFill("solid", fgColor=COLOR_HEADER_BG)
        ws["A1"].font = font_main_header
        ws["A1"].alignment = align_header
        ws["A1"].border = border_all
        ws["A2"].border = border_all
        
        ws.merge_cells("B1:B2")
        ws["B1"] = "SAAT"
        ws["B1"].fill = PatternFill("solid", fgColor=COLOR_HEADER_BG)
        ws["B1"].font = font_main_header
        ws["B1"].alignment = align_header
        ws["B1"].border = border_all
        ws["B2"].border = border_all
        
        current_col = 3
        class_columns = []
        
        for i, sinif in enumerate(sinif_seviyeleri):
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
                class_columns.append(c)
            
            sub_headers = ["Dersin Adı", "Öğr. Elemanı", "Yer"] * 2
            
            for k, header_text in enumerate(sub_headers):
                c_idx = current_col + k
                cell = ws.cell(2, c_idx, header_text)
                cell.fill = PatternFill("solid", fgColor=COLOR_SUB_BG)
                cell.font = font_sub_header
                cell.alignment = align_header
                cell.border = border_all
                
                col_let = get_column_letter(c_idx)
                if "Yer" in header_text:
                    ws.column_dimensions[col_let].width = 6
                elif "Ders" in header_text:
                    ws.column_dimensions[col_let].width = 22
                else:
                    ws.column_dimensions[col_let].width = 16
            
            current_col += 6
            
            if i < len(sinif_seviyeleri) - 1:
                gap_col_letter = get_column_letter(current_col)
                ws.column_dimensions[gap_col_letter].width = 2
                current_col += 1
        
        row_num = 3
        
        for d_idx, gun in enumerate(self.GUNLER):
            start_row = row_num
            
            for s_idx, slot in enumerate(self.SLOTLAR):
                row_map[(d_idx, s_idx)] = row_num
                
                cell_slot = ws.cell(row_num, 2, slot)
                cell_slot.font = font_slot
                cell_slot.alignment = align_header
                
                is_last_slot_of_day = (s_idx == len(self.SLOTLAR) - 1)
                current_border = border_thick_bottom if is_last_slot_of_day else border_all
                
                cell_slot.border = current_border
                
                for c in class_columns:
                    cell_grid = ws.cell(row_num, c)
                    cell_grid.border = current_border
                
                row_num += 1
            
            end_row = row_num - 1
            
            is_last_day = (gun == self.GUNLER[-1])
            for r in range(start_row, end_row + 1):
                day_cell = ws.cell(r, 1)
                if r == start_row:
                    if is_last_day:
                        day_cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
                    else:
                        day_cell.border = border_all
                elif r == end_row:
                    if is_last_day:
                        day_cell.border = Border(left=thin, right=thin, top=thin, bottom=medium)
                    else:
                        day_cell.border = border_all
                else:
                    day_cell.border = Border(left=thin, right=thin, top=None, bottom=None)
            
            ws.merge_cells(start_row=start_row, start_column=1, end_row=end_row, end_column=1)
            
            cell_day = ws.cell(start_row, 1, gun)
            cell_day.font = font_day
            cell_day.alignment = align_vertical
            
            if is_last_day:
                cell_day.border = Border(left=thin, right=thin, top=thin, bottom=medium)
            else:
                cell_day.border = border_all
            
            for r in range(start_row, end_row + 1):
                day_cell = ws.cell(r, 1)
                if r == start_row:
                    if is_last_day:
                        day_cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
                    else:
                        day_cell.border = border_all
                elif r == end_row:
                    if is_last_day:
                        day_cell.border = Border(left=thin, right=thin, top=thin, bottom=medium)
                    else:
                        day_cell.border = border_all
                else:
                    day_cell.border = Border(left=thin, right=thin, top=None, bottom=None)
            
            if gun != self.GUNLER[-1]:
                row_num += 1
        
        ws.column_dimensions['A'].width = 5
        ws.column_dimensions['B'].width = 13
        
        for task in solution['tasks']:
            start_val = task['start_slot']
            duration = task['duration']
            
            ders_ad = task['ders_ad']
            hoca_ad = task['hoca_ad']
            oda_ad = task['oda_ad']
            
            sinif_level = task['sinif_seviyesi']
            sube = task['şube']
            target_sube = "B" if sube == "B" else "A"
            
            if (sinif_level, target_sube) not in col_map:
                continue
            
            base_col = col_map[(sinif_level, target_sube)]
            
            for i in range(duration):
                current_abs_slot = start_val + i
                day_idx = current_abs_slot // self.NUM_SLOTS
                slot_idx = current_abs_slot % self.NUM_SLOTS
                
                if (day_idx, slot_idx) in row_map:
                    r = row_map[(day_idx, slot_idx)]
                    
                    is_last_slot = (slot_idx == self.NUM_SLOTS - 1)
                    curr_border = border_thick_bottom if is_last_slot else border_all
                    
                    c1 = ws.cell(r, base_col, ders_ad)
                    c1.alignment = align_content
                    c1.font = font_content
                    c1.border = curr_border
                    
                    c2 = ws.cell(r, base_col + 1, hoca_ad)
                    c2.alignment = align_content
                    c2.font = font_content
                    c2.border = curr_border
                    
                    c3 = ws.cell(r, base_col + 2, oda_ad)
                    c3.alignment = align_content
                    c3.font = Font(name="Calibri", size=8, bold=True, color="FF0000")
                    c3.border = curr_border
        
        wb.save(output_filename)
        return output_filename

