import os
import tempfile
from typing import Dict, List, Optional
from excel_exporter import ExcelExporter


class PDFExporter:
    def __init__(self):
        self.excel_exporter = ExcelExporter()
    
    def export(self, solution: dict, output_filename: str = "Final_Program.pdf", 
               all_class_levels: Optional[List[int]] = None) -> Optional[str]:
        excel_filename = output_filename.replace('.pdf', '.xlsx')
        excel_filename = output_filename.replace('.pdf', '.xlsx')
        excel_path = self.excel_exporter.export(solution, excel_filename, all_class_levels=all_class_levels)
        
        if not excel_path or not os.path.exists(excel_path):
            return None
        
        try:
            return self._convert_excel_to_pdf_windows(excel_path, output_filename)
        except Exception as e:
            raise Exception(f"PDF dönüştürme hatası: {str(e)}\n\nExcel dosyası oluşturuldu: {excel_path}\nLütfen Excel'de 'Farklı Kaydet > PDF' seçeneğini kullanarak manuel olarak PDF'e dönüştürebilirsiniz.")
    
    def _convert_excel_to_pdf_windows(self, excel_path: str, pdf_path: str) -> str:
        try:
            import win32com.client
        except ImportError:
            raise Exception("win32com kütüphanesi bulunamadı. Lütfen 'pip install pywin32' komutu ile yükleyin.")
        
        excel = None
        workbook = None
        
        try:
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            
            workbook = excel.Workbooks.Open(os.path.abspath(excel_path))
            worksheet = workbook.ActiveSheet
            
            try:
                page_setup = worksheet.PageSetup
                try:
                    page_setup.Zoom = False
                except:
                    pass
                
                page_setup.FitToPagesWide = 1
                page_setup.FitToPagesTall = 1
            except Exception as setup_error:
                pass
            
            workbook.ExportAsFixedFormat(0, os.path.abspath(pdf_path))
            
            return pdf_path
            
        except Exception as e:
            error_msg = str(e)
            if "Excel.Application" in error_msg or "COM" in error_msg:
                raise Exception("Microsoft Excel bulunamadı veya açılamadı. Lütfen Excel'in yüklü olduğundan emin olun.")
            else:
                raise Exception(f"PDF dönüştürme hatası: {error_msg}")
        finally:
            if workbook:
                try:
                    workbook.Close(SaveChanges=False)
                except:
                    pass
            if excel:
                try:
                    excel.Quit()
                except:
                    pass


def export_to_pdf(solution: dict, output_filename: str = "Final_Program.pdf", 
                  all_class_levels: Optional[List[int]] = None) -> Optional[str]:
    exporter = PDFExporter()
    return exporter.export(solution, output_filename, all_class_levels=all_class_levels)
