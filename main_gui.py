import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QLineEdit, QComboBox, QSpinBox, QCheckBox, QMessageBox, QFileDialog,
    QListWidget, QListWidgetItem, QGroupBox, QFormLayout, QDialog,
    QDialogButtonBox, QTextEdit, QProgressBar, QHeaderView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette
from typing import Optional, List
from database import DatabaseManager
from models import Hoca, Oda, Ders, Program
from scheduler_engine import SchedulerEngine
from excel_exporter import ExcelExporter
from pdf_exporter import PDFExporter


class SolveThread(QThread):
    finished = pyqtSignal(str, object)
    error = pyqtSignal(str)
    
    def __init__(self, engine: SchedulerEngine, program_id: int):
        super().__init__()
        self.engine = engine
        self.program_id = program_id
    
    def run(self):
        try:
            status, solution = self.engine.solve(self.program_id)
            self.finished.emit(status, solution)
        except Exception as e:
            self.error.emit(str(e))


class ProgramDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Program Oluştur")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        form = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Örn: 2024-2025 Güz Dönemi")
        form.addRow("Program Adı:", self.name_input)
        
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setPlaceholderText("Açıklama (opsiyonel)")
        form.addRow("Açıklama:", self.desc_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_data(self) -> tuple:
        """Dialog verilerini döndür"""
        return (
            self.name_input.text().strip(),
            self.desc_input.toPlainText().strip() or None
        )


class TeacherDialog(QDialog):
    def __init__(self, parent=None, hoca: Optional[Hoca] = None):
        super().__init__(parent)
        self.hoca = hoca
        self.setWindowTitle("Öğretmen Ekle" if not hoca else "Öğretmen Düzenle")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        # ID sadece düzenleme modunda gösterilir (değiştirilemez)
        if hoca:
            self.id_label = QLabel(f"Hoca ID: {hoca.hoca_id}")
            self.id_label.setEnabled(False)
            form.addRow("", self.id_label)
        
        self.name_input = QLineEdit()
        if hoca:
            self.name_input.setText(hoca.hoca_ad)
        form.addRow("Hoca Adı:", self.name_input)
        
        days_group = QGroupBox("Müsait Günler")
        days_layout = QVBoxLayout()
        
        self.day_checkboxes = {}
        gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
        for gun in gunler:
            checkbox = QCheckBox(gun)
            if hoca and gun in hoca.musait_gunler:
                checkbox.setChecked(True)
            self.day_checkboxes[gun] = checkbox
            days_layout.addWidget(checkbox)
        
        days_group.setLayout(days_layout)
        form.addRow("", days_group)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_data(self) -> tuple:
        """Dialog verilerini döndür"""
        # Checkbox'lardan seçili günleri al
        selected_days = [gun for gun, checkbox in self.day_checkboxes.items() if checkbox.isChecked()]
        # ID sadece düzenleme modunda kullanılır, yeni eklemede None döner (otomatik üretilecek)
        hoca_id = self.hoca.hoca_id if self.hoca else None
        return (
            hoca_id,
            self.name_input.text().strip(),
            selected_days
        )


class RoomDialog(QDialog):
    def __init__(self, parent=None, oda: Optional[Oda] = None):
        super().__init__(parent)
        self.oda = oda
        self.setWindowTitle("Oda Ekle" if not oda else "Oda Düzenle")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        # ID sadece düzenleme modunda gösterilir (değiştirilemez)
        if oda:
            self.id_label = QLabel(f"Oda ID: {oda.oda_id}")
            self.id_label.setEnabled(False)
            form.addRow("", self.id_label)
        
        self.name_input = QLineEdit()
        if oda:
            self.name_input.setText(oda.oda_ad)
        form.addRow("Oda Adı:", self.name_input)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["teorik", "lab", "ue"])
        if oda:
            index = self.type_combo.findText(oda.tip)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
        form.addRow("Tip:", self.type_combo)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_data(self) -> tuple:
        oda_id = self.oda.oda_id if self.oda else ""
        return (
            oda_id,
            self.name_input.text().strip(),
            self.type_combo.currentText()
        )


class LessonDialog(QDialog):
    """Ders ekleme/düzenleme dialog'u"""
    
    def __init__(self, parent=None, ders: Optional[Ders] = None, hocalar: List[Hoca] = None):
        super().__init__(parent)
        self.ders = ders
        self.hocalar = hocalar or []
        self.setWindowTitle("Ders Ekle" if not ders else "Ders Düzenle")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        form = QFormLayout()
        
        if ders:
            self.id_label = QLabel(f"Ders ID: {ders.ders_id}")
            self.id_label.setEnabled(False)
            form.addRow("", self.id_label)
        
        self.name_input = QLineEdit()
        if ders:
            self.name_input.setText(ders.ders_ad)
        form.addRow("Ders Adı:", self.name_input)
        
        self.kredi_input = QSpinBox()
        self.kredi_input.setMinimum(1)
        self.kredi_input.setMaximum(10)
        if ders:
            self.kredi_input.setValue(ders.kredi)
        form.addRow("Kredi:", self.kredi_input)
        
        self.sube_combo = QComboBox()
        self.sube_combo.addItems(["Tek", "A", "B"])
        if ders:
            index = self.sube_combo.findText(ders.şube)
            if index >= 0:
                self.sube_combo.setCurrentIndex(index)
        form.addRow("Şube:", self.sube_combo)
        
        self.hoca_combo = QComboBox()
        for hoca in self.hocalar:
            self.hoca_combo.addItem(hoca.hoca_ad, hoca.hoca_id)
        
        if ders:
            index = self.hoca_combo.findData(ders.hoca_id)
            if index >= 0:
                self.hoca_combo.setCurrentIndex(index)
        form.addRow("Hoca:", self.hoca_combo)
        
        self.teorik_input = QSpinBox()
        self.teorik_input.setMinimum(0)
        self.teorik_input.setMaximum(10)
        if ders:
            self.teorik_input.setValue(ders.teorik_slot)
        form.addRow("Teorik Slot:", self.teorik_input)
        
        self.lab_input = QSpinBox()
        self.lab_input.setMinimum(0)
        self.lab_input.setMaximum(10)
        if ders:
            self.lab_input.setValue(ders.lab_slot)
        form.addRow("Lab Slot:", self.lab_input)
        
        self.ue_check = QCheckBox()
        if ders:
            self.ue_check.setChecked(ders.ue)
        form.addRow("Uzaktan Eğitim:", self.ue_check)
        
        self.sinif_input = QSpinBox()
        self.sinif_input.setMinimum(1)
        self.sinif_input.setMaximum(4)
        if ders:
            self.sinif_input.setValue(ders.sinif_seviyesi)
        form.addRow("Sınıf Seviyesi:", self.sinif_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_data(self) -> dict:
        """Dialog verilerini döndür"""
        # ID sadece düzenleme modunda kullanılır, yeni eklemede None döner (otomatik üretilecek)
        ders_id = self.ders.ders_id if self.ders else None
        # Hoca ID'sini combo'dan al (currentData ile)
        hoca_id = self.hoca_combo.currentData()
        if hoca_id is None or hoca_id == 0:
            hoca_id = 0  # Varsayılan
        
        return {
            'ders_id': ders_id,
            'ders_ad': self.name_input.text().strip(),
            'kredi': self.kredi_input.value(),
            'şube': self.sube_combo.currentText(),
            'hoca_id': hoca_id,
            'teorik_slot': self.teorik_input.value(),
            'lab_slot': self.lab_input.value(),
            'ue': self.ue_check.isChecked(),
            'sinif_seviyesi': self.sinif_input.value()
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.engine = SchedulerEngine(self.db)
        self.current_program_id: Optional[int] = None
        self.solve_thread: Optional[SolveThread] = None
        self.current_solution = None
        
        self.setWindowTitle("Ders Programı Optimizasyon Sistemi")
        self.setMinimumSize(1200, 800)
        self.showMaximized()
        
        self.apply_modern_style()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_widget.setLayout(main_layout)
        
        program_group = QGroupBox("Program Yönetimi")
        program_layout = QHBoxLayout()
        program_layout.setSpacing(15)
        program_layout.setContentsMargins(20, 15, 20, 15)
        
        program_layout.addWidget(QLabel("Aktif Program:"))
        self.program_combo = QComboBox()
        self.program_combo.currentIndexChanged.connect(self.on_program_changed)
        program_layout.addWidget(self.program_combo, 1)
        
        btn_new_program = QPushButton("Yeni Program")
        btn_new_program.clicked.connect(self.create_program)
        program_layout.addWidget(btn_new_program)
        
        btn_delete_program = QPushButton("Programı Sil")
        btn_delete_program.clicked.connect(self.delete_program)
        btn_delete_program.setStyleSheet("QPushButton { background-color: #ef4444; } QPushButton:hover { background-color: #dc2626; }")
        program_layout.addWidget(btn_delete_program)
        
        program_group.setLayout(program_layout)
        main_layout.addWidget(program_group)
        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        self.teacher_tab = self.create_teacher_tab()
        self.tabs.addTab(self.teacher_tab, "Öğretmenler")
        
        self.room_tab = self.create_room_tab()
        self.tabs.addTab(self.room_tab, "Odalar")
        
        self.lesson_tab = self.create_lesson_tab()
        self.tabs.addTab(self.lesson_tab, "Dersler")
        
        self.solve_tab = self.create_solve_tab()
        self.tabs.addTab(self.solve_tab, "Motor ve Çıktı")
        
        self.refresh_programs()
    
    def apply_modern_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #d1d9e6;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: #4a5568;
            }
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10pt;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
            QPushButton:pressed {
                background-color: #4c5bc4;
            }
            QTabWidget::pane {
                border: 1px solid #d1d9e6;
                border-radius: 8px;
                background-color: #ffffff;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #e2e8f0;
                color: #4a5568;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 10pt;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #667eea;
                border-bottom: 2px solid #667eea;
            }
            QTabBar::tab:hover {
                background-color: #f1f5f9;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #e2e8f0;
                selection-background-color: #e0e7ff;
                selection-color: #1e293b;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #e0e7ff;
            }
            QHeaderView::section {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 10pt;
            }
            QComboBox {
                background-color: #ffffff;
                border: 2px solid #d1d9e6;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
                min-width: 200px;
            }
            QComboBox:hover {
                border-color: #667eea;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #4a5568;
                margin-right: 10px;
            }
            QLabel {
                color: #4a5568;
                font-size: 10pt;
            }
        """)
    
    def create_teacher_tab(self) -> QWidget:
        """Öğretmenler tab'ını oluştur"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)
        
        # Butonlar - ortalanmış
        btn_container = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_add = QPushButton("Öğretmen Ekle")
        btn_add.clicked.connect(self.add_teacher)
        btn_edit = QPushButton("Düzenle")
        btn_edit.clicked.connect(self.edit_teacher)
        btn_delete = QPushButton("Sil")
        btn_delete.clicked.connect(self.delete_teacher)
        btn_delete.setStyleSheet("QPushButton { background-color: #ef4444; } QPushButton:hover { background-color: #dc2626; }")
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()
        
        btn_container.setLayout(btn_layout)
        main_layout.addWidget(btn_container)
        
        # Tablo container - ortalanmış ve boyutlandırılmış
        table_container = QWidget()
        table_layout = QHBoxLayout()
        table_layout.addStretch()
        
        self.teacher_table = QTableWidget()
        self.teacher_table.setColumnCount(3)
        self.teacher_table.setHorizontalHeaderLabels(["Hoca ID", "Hoca Adı", "Müsait Günler"])
        self.teacher_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.teacher_table.verticalHeader().setVisible(False)
        
        # Tablo boyutlarını ayarla
        self.teacher_table.setMinimumWidth(800)
        self.teacher_table.setMaximumWidth(1200)
        self.teacher_table.setMinimumHeight(400)
        
        # Sütun genişliklerini ayarla
        self.teacher_table.setColumnWidth(0, 100)
        self.teacher_table.setColumnWidth(1, 250)
        self.teacher_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        table_layout.addWidget(self.teacher_table)
        table_layout.addStretch()
        table_container.setLayout(table_layout)
        main_layout.addWidget(table_container, 1)  # Stretch factor
        
        widget.setLayout(main_layout)
        return widget
    
    def create_room_tab(self) -> QWidget:
        """Odalar tab'ını oluştur"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)
        
        # Butonlar - ortalanmış
        btn_container = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_add = QPushButton("Oda Ekle")
        btn_add.clicked.connect(self.add_room)
        btn_edit = QPushButton("Düzenle")
        btn_edit.clicked.connect(self.edit_room)
        btn_delete = QPushButton("Sil")
        btn_delete.clicked.connect(self.delete_room)
        btn_delete.setStyleSheet("QPushButton { background-color: #ef4444; } QPushButton:hover { background-color: #dc2626; }")
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()
        
        btn_container.setLayout(btn_layout)
        main_layout.addWidget(btn_container)
        
        # Tablo container - ortalanmış ve boyutlandırılmış
        table_container = QWidget()
        table_layout = QHBoxLayout()
        table_layout.addStretch()
        
        self.room_table = QTableWidget()
        self.room_table.setColumnCount(3)
        self.room_table.setHorizontalHeaderLabels(["Oda ID", "Oda Adı", "Tip"])
        self.room_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.room_table.verticalHeader().setVisible(False)
        
        # Tablo boyutlarını ayarla
        self.room_table.setMinimumWidth(600)
        self.room_table.setMaximumWidth(900)
        self.room_table.setMinimumHeight(400)
        
        # Sütun genişliklerini ayarla
        self.room_table.setColumnWidth(0, 150)
        self.room_table.setColumnWidth(1, 300)
        self.room_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        table_layout.addWidget(self.room_table)
        table_layout.addStretch()
        table_container.setLayout(table_layout)
        main_layout.addWidget(table_container, 1)  # Stretch factor
        
        widget.setLayout(main_layout)
        return widget
    
    def create_lesson_tab(self) -> QWidget:
        """Dersler tab'ını oluştur"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)
        
        # Butonlar - ortalanmış
        btn_container = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_add = QPushButton("Ders Ekle")
        btn_add.clicked.connect(self.add_lesson)
        btn_edit = QPushButton("Düzenle")
        btn_edit.clicked.connect(self.edit_lesson)
        btn_delete = QPushButton("Sil")
        btn_delete.clicked.connect(self.delete_lesson)
        btn_delete.setStyleSheet("QPushButton { background-color: #ef4444; } QPushButton:hover { background-color: #dc2626; }")
        
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.addStretch()
        
        btn_container.setLayout(btn_layout)
        main_layout.addWidget(btn_container)
        
        # Tablo container - ortalanmış ve boyutlandırılmış
        table_container = QWidget()
        table_layout = QHBoxLayout()
        table_layout.addStretch()
        
        self.lesson_table = QTableWidget()
        self.lesson_table.setColumnCount(8)
        self.lesson_table.setHorizontalHeaderLabels([
            "Ders ID", "Ders Adı", "Kredi", "Şube", "Hoca ID", "Teorik", "Lab", "Sınıf"
        ])
        self.lesson_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.lesson_table.verticalHeader().setVisible(False)
        
        # Tablo boyutlarını ayarla
        self.lesson_table.setMinimumWidth(1000)
        self.lesson_table.setMaximumWidth(1400)
        self.lesson_table.setMinimumHeight(500)
        
        # Sütun genişliklerini ayarla
        self.lesson_table.setColumnWidth(0, 80)
        self.lesson_table.setColumnWidth(1, 300)
        self.lesson_table.setColumnWidth(2, 80)
        self.lesson_table.setColumnWidth(3, 80)
        self.lesson_table.setColumnWidth(4, 100)
        self.lesson_table.setColumnWidth(5, 80)
        self.lesson_table.setColumnWidth(6, 80)
        self.lesson_table.setColumnWidth(7, 80)
        
        table_layout.addWidget(self.lesson_table)
        table_layout.addStretch()
        table_container.setLayout(table_layout)
        main_layout.addWidget(table_container, 1)  # Stretch factor
        
        widget.setLayout(main_layout)
        return widget
    
    def create_solve_tab(self) -> QWidget:
        """Motor ve çıktı tab'ını oluştur"""
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(25)
        
        # Durum - ortalanmış
        status_container = QWidget()
        status_layout = QVBoxLayout()
        status_layout.addStretch()
        
        status_group = QGroupBox("Durum")
        status_group_layout = QVBoxLayout()
        status_group_layout.setSpacing(15)
        status_group_layout.setContentsMargins(20, 20, 20, 20)
        
        self.status_label = QLabel("Hazır")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #10b981; padding: 10px; font-weight: bold;")
        status_group_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #d1d9e6;
                border-radius: 8px;
                text-align: center;
                height: 25px;
                background-color: #f1f5f9;
            }
            QProgressBar::chunk {
                background-color: #667eea;
                border-radius: 6px;
            }
        """)
        status_group_layout.addWidget(self.progress_bar)
        
        status_group.setLayout(status_group_layout)
        status_layout.addWidget(status_group)
        status_layout.addStretch()
        status_container.setLayout(status_layout)
        main_layout.addWidget(status_container)
        
        # Motor butonu - ortalanmış ve büyük
        btn_container = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        btn_solve = QPushButton("Ders Programı Oluştur")
        btn_solve.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        btn_solve.setMinimumHeight(60)
        btn_solve.setMinimumWidth(300)
        btn_solve.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                font-size: 14pt;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        btn_solve.clicked.connect(self.run_solver)
        btn_layout.addWidget(btn_solve)
        btn_layout.addStretch()
        
        btn_container.setLayout(btn_layout)
        main_layout.addWidget(btn_container)
        
        # Çıktı butonları - ortalanmış
        output_container = QWidget()
        output_layout = QVBoxLayout()
        output_layout.addStretch()
        
        output_group = QGroupBox("Çıktı Formatları")
        output_group_layout = QVBoxLayout()
        output_group_layout.setSpacing(15)
        output_group_layout.setContentsMargins(20, 20, 20, 20)
        
        btn_excel = QPushButton("Excel Olarak Kaydet")
        btn_excel.setMinimumHeight(50)
        btn_excel.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)
        btn_excel.clicked.connect(self.export_excel)
        output_group_layout.addWidget(btn_excel)
        
        btn_pdf = QPushButton("PDF Olarak Kaydet")
        btn_pdf.setMinimumHeight(50)
        btn_pdf.setStyleSheet("""
            QPushButton {
                background-color: #f59e0b;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #d97706;
            }
        """)
        btn_pdf.clicked.connect(self.export_pdf)
        output_group_layout.addWidget(btn_pdf)
        
        output_group.setLayout(output_group_layout)
        output_layout.addWidget(output_group)
        output_layout.addStretch()
        output_container.setLayout(output_layout)
        main_layout.addWidget(output_container)
        
        main_layout.addStretch()
        widget.setLayout(main_layout)
        return widget
    
    def refresh_programs(self):
        """Program listesini yenile"""
        self.program_combo.clear()
        programs = self.db.get_all_programs()
        for prog in programs:
            self.program_combo.addItem(prog.program_adi, prog.program_id)
        
        if programs:
            self.current_program_id = programs[0].program_id
            self.refresh_all_tabs()
    
    def on_program_changed(self, index: int):
        """Program değiştiğinde"""
        if index >= 0:
            self.current_program_id = self.program_combo.currentData()
            self.refresh_all_tabs()
    
    def refresh_all_tabs(self):
        """Tüm tab'ları yenile"""
        if not self.current_program_id:
            return
        
        self.refresh_teachers()
        self.refresh_rooms()
        self.refresh_lessons()
        self.reset_solver_tab()
    
    def reset_solver_tab(self):
        if hasattr(self, 'current_solution'):
            self.current_solution = None
        
        self.status_label.setText("Hazır")
        self.status_label.setStyleSheet("color: #10b981; padding: 10px; font-weight: bold;")
        
        # Progress bar'ı gizle
        self.progress_bar.setVisible(False)
    
    def refresh_teachers(self):
        if not self.current_program_id:
            return
        
        self.teacher_table.setRowCount(0)
        
        hocalar = self.db.get_teachers(self.current_program_id)
        self.teacher_table.setRowCount(len(hocalar) + 1)
        
        for i, hoca in enumerate(hocalar):
            self.teacher_table.setItem(i, 0, QTableWidgetItem(str(hoca.hoca_id)))
            self.teacher_table.setItem(i, 1, QTableWidgetItem(hoca.hoca_ad))
            self.teacher_table.setItem(i, 2, QTableWidgetItem(", ".join(hoca.musait_gunler)))
        
        count_row = len(hocalar)
        for col in range(3):
            self.teacher_table.setItem(count_row, col, QTableWidgetItem(""))
        
        count_item = QTableWidgetItem(f"Toplam: {len(hocalar)} öğretmen")
        count_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.teacher_table.setItem(count_row, 0, count_item)
        self.teacher_table.setSpan(count_row, 0, 1, 3)
    
    def refresh_rooms(self):
        if not self.current_program_id:
            return
        
        self.room_table.setRowCount(0)
        
        odalar = self.db.get_rooms(self.current_program_id)
        self.room_table.setRowCount(len(odalar) + 1)
        
        for i, oda in enumerate(odalar):
            self.room_table.setItem(i, 0, QTableWidgetItem(oda.oda_id))
            self.room_table.setItem(i, 1, QTableWidgetItem(oda.oda_ad))
            self.room_table.setItem(i, 2, QTableWidgetItem(oda.tip))
        
        count_row = len(odalar)
        for col in range(3):
            self.room_table.setItem(count_row, col, QTableWidgetItem(""))
        
        count_item = QTableWidgetItem(f"Toplam: {len(odalar)} oda")
        count_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.room_table.setItem(count_row, 0, count_item)
        self.room_table.setSpan(count_row, 0, 1, 3)
    
    def refresh_lessons(self):
        if not self.current_program_id:
            return
        
        self.lesson_table.setRowCount(0)
        
        dersler = self.db.get_lessons(self.current_program_id)
        
        dersler_by_level = {1: [], 2: [], 3: [], 4: []}
        for ders in dersler:
            if ders.sinif_seviyesi in dersler_by_level:
                dersler_by_level[ders.sinif_seviyesi].append(ders)
        
        total_data_rows = 0
        for level_dersler in dersler_by_level.values():
            if len(level_dersler) > 0:
                total_data_rows += 1  # Başlık satırı
                total_data_rows += len(level_dersler)
        
        total_rows = total_data_rows + 1
        self.lesson_table.setRowCount(total_rows)
        
        current_row = 0
        
        for sinif_level in [1, 2, 3, 4]:
            level_dersler = dersler_by_level[sinif_level]
            
            if len(level_dersler) == 0:
                continue
            
            header_item = QTableWidgetItem(f"{sinif_level}. SINIF DERSLERİ")
            header_item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            header_item.setBackground(QColor(211, 211, 211))
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            
            for col in range(8):
                self.lesson_table.setItem(current_row, col, QTableWidgetItem(""))
            
            self.lesson_table.setItem(current_row, 0, header_item)
            self.lesson_table.setSpan(current_row, 0, 1, 8)
            current_row += 1
            
            for ders in level_dersler:
                self.lesson_table.setItem(current_row, 0, QTableWidgetItem(str(ders.ders_id)))
                self.lesson_table.setItem(current_row, 1, QTableWidgetItem(ders.ders_ad))
                self.lesson_table.setItem(current_row, 2, QTableWidgetItem(str(ders.kredi)))
                self.lesson_table.setItem(current_row, 3, QTableWidgetItem(ders.şube))
                self.lesson_table.setItem(current_row, 4, QTableWidgetItem(str(ders.hoca_id)))
                self.lesson_table.setItem(current_row, 5, QTableWidgetItem(str(ders.teorik_slot)))
                self.lesson_table.setItem(current_row, 6, QTableWidgetItem(str(ders.lab_slot)))
                self.lesson_table.setItem(current_row, 7, QTableWidgetItem(str(ders.sinif_seviyesi)))
                current_row += 1
        
        count_row = current_row
        
        for col in range(8):
            self.lesson_table.setItem(count_row, col, QTableWidgetItem(""))
        
        count_item = QTableWidgetItem(f"Toplam: {len(dersler)} ders")
        count_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        count_item.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        count_item.setBackground(QColor(240, 240, 240))  # Açık gri arka plan
        
        # Toplam item'ı ekle ve merge et
        self.lesson_table.setItem(count_row, 0, count_item)
        self.lesson_table.setSpan(count_row, 0, 1, 8)  # 1 satır, 8 sütun merge
    
    # Program işlemleri
    def create_program(self):
        """Yeni program oluştur"""
        dialog = ProgramDialog(self)
        if dialog.exec():
            name, desc = dialog.get_data()
            if name:
                program_id = self.db.create_program(name, desc)
                self.refresh_programs()
                index = self.program_combo.findData(program_id)
                if index >= 0:
                    self.program_combo.setCurrentIndex(index)
            else:
                QMessageBox.warning(self, "Hata", "Program adı boş olamaz!")
    
    def delete_program(self):
        """Programı sil"""
        if not self.current_program_id:
            return
        
        reply = QMessageBox.question(
            self, "Onay",
            "Bu programı ve tüm verilerini silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_program(self.current_program_id)
            self.current_program_id = None
            self.refresh_programs()
    
    def add_teacher(self):
        if not self.current_program_id:
            QMessageBox.warning(self, "Hata", "Lütfen önce bir program seçin!")
            return
        
        dialog = TeacherDialog(self)
        if dialog.exec():
            hoca_id, hoca_ad, musait_gunler = dialog.get_data()
            if hoca_ad and musait_gunler:
                hoca = Hoca(hoca_id=hoca_id, hoca_ad=hoca_ad, musait_gunler=musait_gunler, program_id=self.current_program_id)
                self.db.add_teacher(hoca, auto_id=True)
                self.refresh_teachers()
            else:
                QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")
    
    def edit_teacher(self):
        if not self.current_program_id:
            return
        
        row = self.teacher_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Lütfen bir öğretmen seçin!")
            return
        
        hoca_id = int(self.teacher_table.item(row, 0).text())
        hocalar = self.db.get_teachers(self.current_program_id)
        hoca = next((h for h in hocalar if h.hoca_id == hoca_id), None)
        
        if hoca:
            dialog = TeacherDialog(self, hoca)
            if dialog.exec():
                hoca_id, hoca_ad, musait_gunler = dialog.get_data()
                if hoca_ad and musait_gunler:
                    hoca.hoca_ad = hoca_ad
                    hoca.musait_gunler = musait_gunler
                    self.db.add_teacher(hoca, auto_id=False)  # Düzenlemede ID değişmez
                    self.refresh_teachers()
    
    def delete_teacher(self):
        """Öğretmen sil"""
        if not self.current_program_id:
            return
        
        row = self.teacher_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Lütfen bir öğretmen seçin!")
            return
        
        hoca_id = int(self.teacher_table.item(row, 0).text())
        self.db.delete_teacher(self.current_program_id, hoca_id)
        self.refresh_teachers()
    
    def add_room(self):
        if not self.current_program_id:
            QMessageBox.warning(self, "Hata", "Lütfen önce bir program seçin!")
            return
        
        dialog = RoomDialog(self)
        if dialog.exec():
            oda_id, oda_ad, tip = dialog.get_data()
            if oda_ad:  # ID otomatik üretilecek, sadece ad kontrolü yeterli
                oda = Oda(oda_id=oda_id, oda_ad=oda_ad, tip=tip, program_id=self.current_program_id)
                self.db.add_room(oda, auto_id=True)  # Otomatik ID üret
                self.refresh_rooms()
            else:
                QMessageBox.warning(self, "Hata", "Oda adı boş olamaz!")
    
    def edit_room(self):
        """Oda düzenle"""
        if not self.current_program_id:
            return
        
        row = self.room_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Lütfen bir oda seçin!")
            return
        
        oda_id = self.room_table.item(row, 0).text()
        odalar = self.db.get_rooms(self.current_program_id)
        oda = next((o for o in odalar if o.oda_id == oda_id), None)
        
        if oda:
            dialog = RoomDialog(self, oda)
            if dialog.exec():
                oda_id, oda_ad, tip = dialog.get_data()
                if oda_ad:
                    oda.oda_ad = oda_ad
                    oda.tip = tip
                    self.db.add_room(oda, auto_id=False)  # Düzenlemede ID değişmez
                    self.refresh_rooms()
    
    def delete_room(self):
        """Oda sil"""
        if not self.current_program_id:
            return
        
        row = self.room_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Lütfen bir oda seçin!")
            return
        
        oda_id = self.room_table.item(row, 0).text()
        self.db.delete_room(self.current_program_id, oda_id)
        self.refresh_rooms()
    
    # Ders işlemleri
    def add_lesson(self):
        """Ders ekle"""
        if not self.current_program_id:
            QMessageBox.warning(self, "Hata", "Lütfen önce bir program seçin!")
            return
        
        hocalar = self.db.get_teachers(self.current_program_id)
        
        if not hocalar:
            QMessageBox.warning(self, "Hata", "Önce öğretmen eklemelisiniz!")
            return
        
        dialog = LessonDialog(self, None, hocalar)
        if dialog.exec():
            data = dialog.get_data()
            if data['ders_ad']:
                ders = Ders(
                    ders_id=data['ders_id'],
                    ders_ad=data['ders_ad'],
                    kredi=data['kredi'],
                    şube=data['şube'],
                    hoca_id=data['hoca_id'],
                    teorik_slot=data['teorik_slot'],
                    lab_slot=data['lab_slot'],
                    ue=data['ue'],
                    sinif_seviyesi=data['sinif_seviyesi'],
                    program_id=self.current_program_id
                )
                self.db.add_lesson(ders, auto_id=True)  # Otomatik ID üret
                self.refresh_lessons()
    
    def edit_lesson(self):
        """Ders düzenle"""
        if not self.current_program_id:
            return
        
        row = self.lesson_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Lütfen bir ders seçin!")
            return
        
        ders_id = int(self.lesson_table.item(row, 0).text())
        dersler = self.db.get_lessons(self.current_program_id)
        ders = next((d for d in dersler if d.ders_id == ders_id), None)
        
        if ders:
            hocalar = self.db.get_teachers(self.current_program_id)
            dialog = LessonDialog(self, ders, hocalar)
            if dialog.exec():
                data = dialog.get_data()
                if data['ders_ad']:
                    ders.ders_ad = data['ders_ad']
                    ders.kredi = data['kredi']
                    ders.şube = data['şube']
                    ders.hoca_id = data['hoca_id']
                    ders.teorik_slot = data['teorik_slot']
                    ders.lab_slot = data['lab_slot']
                    ders.ue = data['ue']
                    ders.sinif_seviyesi = data['sinif_seviyesi']
                    self.db.add_lesson(ders, auto_id=False)  # Düzenlemede ID değişmez
                    self.refresh_lessons()
    
    def delete_lesson(self):
        """Ders sil"""
        if not self.current_program_id:
            return
        
        row = self.lesson_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Lütfen bir ders seçin!")
            return
        
        ders_id = int(self.lesson_table.item(row, 0).text())
        self.db.delete_lesson(self.current_program_id, ders_id)
        self.refresh_lessons()
    
    def run_solver(self):
        if not self.current_program_id:
            QMessageBox.warning(self, "Hata", "Lütfen önce bir program seçin!")
            return
        
        # Veri kontrolü
        dersler = self.db.get_lessons(self.current_program_id)
        odalar = self.db.get_rooms(self.current_program_id)
        hocalar = self.db.get_teachers(self.current_program_id)
        
        if not dersler:
            QMessageBox.warning(self, "Hata", "En az bir ders eklemelisiniz!")
            return
        if not odalar:
            QMessageBox.warning(self, "Hata", "En az bir oda eklemelisiniz!")
            return
        if not hocalar:
            QMessageBox.warning(self, "Hata", "En az bir öğretmen eklemelisiniz!")
            return
        
        # Thread başlat
        self.status_label.setText("Motor çalışıyor...")
        self.status_label.setStyleSheet("color: #f59e0b; padding: 10px; font-weight: bold;")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        self.solve_thread = SolveThread(self.engine, self.current_program_id)
        self.solve_thread.finished.connect(self.on_solve_finished)
        self.solve_thread.error.connect(self.on_solve_error)
        self.solve_thread.start()
    
    def on_solve_finished(self, status: str, solution):
        """Motor tamamlandığında"""
        self.progress_bar.setVisible(False)
        
        if solution:
            self.current_solution = solution
            
            # Ceza puanı bilgisi
            total_penalty = solution.get('total_penalty', 0)
            penalty_details = solution.get('penalty_details', {})
            
            # Durum mesajı oluştur (kısa versiyon)
            if status == "OPTIMAL":
                if total_penalty == 0:
                    status_text = f"Çözüm bulundu: {status}\nCeza Puanı: 0"
                else:
                    status_text = f"Çözüm bulundu: {status}\nCeza Puanı: {total_penalty}"
            else:  # FEASIBLE
                status_text = f"Çözüm bulundu: {status}\nCeza Puanı: {total_penalty}"
            
            self.status_label.setText(status_text)
            self.status_label.setStyleSheet("color: #10b981; padding: 10px; font-weight: bold;")
            
            # Detaylı mesaj
            detail_msg = f"Çözüm bulundu!\n\n"
            
            # Durum açıklaması
            if status == "OPTIMAL":
                if total_penalty == 0:
                    detail_msg += "Durum: OPTIMAL\nCeza Puanı: 0\n\n"
                    detail_msg += "Tüm katı kısıtlar (C1-C9) ve esnek kısıtlar (C10-C12) sağlandı!\n"
                    detail_msg += "Bu, mümkün olan en iyi çözümdür."
                else:
                    detail_msg += "Durum: OPTIMAL\nToplam Ceza Puanı: {}\n\n".format(total_penalty)
                    detail_msg += "Tüm katı kısıtlar (C1-C9) sağlandı.\n"
                    detail_msg += "Bazı esnek kısıtlar ihlal edildi, ancak bu en iyi mümkün çözümdür:\n\n"
                    
                    # C10 - Büyük dersler sabaha
                    if penalty_details.get('big_course_penalty', 0) > 0:
                        big_list = penalty_details.get('big_course_list', [])
                        detail_msg += "C10 - Büyük dersler sabaha: {} puan\n".format(penalty_details['big_course_penalty'])
                        for item in big_list:
                            sube_text = f" ({item['şube']})" if item['şube'] != "Tek" else ""
                            detail_msg += "  - {} ders, {}. sınıf{}, {}\n".format(
                                item['ders_ad'], item['sinif_seviyesi'], sube_text, item['gun'])
                        detail_msg += "\n"
                    
                    # C11 - Öğle arası koruması
                    if penalty_details.get('lunch_penalty', 0) > 0:
                        lunch_list = penalty_details.get('lunch_violations', [])
                        detail_msg += "C11 - Öğle arası koruması: {} puan\n".format(penalty_details['lunch_penalty'])
                        for item in lunch_list:
                            sube_text = f" ({item['şube']})" if item['şube'] != "Tek" else ""
                            detail_msg += "  - {} ders, {}. sınıf{}, {}\n".format(
                                item['ders_ad'], item['sinif_seviyesi'], sube_text, item['gun'])
                        detail_msg += "\n"
                    
                    # C12 - Günlük kredi limiti
                    if penalty_details.get('daily_load_penalty', 0) > 0:
                        load_list = penalty_details.get('daily_load_violations', [])
                        detail_msg += "C12 - Günlük kredi limiti: {} puan\n".format(penalty_details['daily_load_penalty'])
                        for item in load_list:
                            detail_msg += "  - {}. sınıf, {}: {} kredi (limit: 6, fazla: {} kredi)\n".format(
                                item['sinif_seviyesi'], item['gun'], item['toplam_kredi'], item['fazla_kredi'])
                            detail_msg += "    Dersler: "
                            ders_adlari = []
                            for ders in item['dersler']:
                                sube_text = f" ({ders['şube']})" if ders['şube'] != "Tek" else ""
                                ders_adlari.append(f"{ders['ders_ad']}{sube_text} [{ders['kredi']} kr]")
                            detail_msg += ", ".join(ders_adlari) + "\n"
                        detail_msg += "\n"
            else:  # FEASIBLE
                detail_msg += "Durum: FEASIBLE\nToplam Ceza Puanı: {}\n\n".format(total_penalty)
                detail_msg += "Tüm katı kısıtlar (C1-C9) sağlandı.\n"
                detail_msg += "Bazı esnek kısıtlar ihlal edildi (daha iyi bir çözüm bulunamadı):\n\n"
                
                # C10 - Büyük dersler sabaha
                if penalty_details.get('big_course_penalty', 0) > 0:
                    big_list = penalty_details.get('big_course_list', [])
                    detail_msg += "C10 - Büyük dersler sabaha: {} puan\n".format(penalty_details['big_course_penalty'])
                    for item in big_list:
                        sube_text = f" ({item['şube']})" if item['şube'] != "Tek" else ""
                        detail_msg += "  - {} ders, {}. sınıf{}, {}\n".format(
                            item['ders_ad'], item['sinif_seviyesi'], sube_text, item['gun'])
                    detail_msg += "\n"
                
                # C11 - Öğle arası koruması
                if penalty_details.get('lunch_penalty', 0) > 0:
                    lunch_list = penalty_details.get('lunch_violations', [])
                    detail_msg += "C11 - Öğle arası koruması: {} puan\n".format(penalty_details['lunch_penalty'])
                    for item in lunch_list:
                        sube_text = f" ({item['şube']})" if item['şube'] != "Tek" else ""
                        detail_msg += "  - {} ders, {}. sınıf{}, {}\n".format(
                            item['ders_ad'], item['sinif_seviyesi'], sube_text, item['gun'])
                    detail_msg += "\n"
                
                # C12 - Günlük kredi limiti
                if penalty_details.get('daily_load_penalty', 0) > 0:
                    load_list = penalty_details.get('daily_load_violations', [])
                    detail_msg += "C12 - Günlük kredi limiti: {} puan\n".format(penalty_details['daily_load_penalty'])
                    for item in load_list:
                        detail_msg += "  - {}. sınıf, {}: {} kredi (limit: 6, fazla: {} kredi)\n".format(
                            item['sinif_seviyesi'], item['gun'], item['toplam_kredi'], item['fazla_kredi'])
                        detail_msg += "    Dersler: "
                        ders_adlari = []
                        for ders in item['dersler']:
                            sube_text = f" ({ders['şube']})" if ders['şube'] != "Tek" else ""
                            ders_adlari.append(f"{ders['ders_ad']}{sube_text} [{ders['kredi']} kr]")
                        detail_msg += ", ".join(ders_adlari) + "\n"
                    detail_msg += "\n"
            
            QMessageBox.information(self, "Başarılı", detail_msg)
        else:
            self.status_label.setText(f"Çözüm bulunamadı: {status}")
            self.status_label.setStyleSheet("color: #ef4444; padding: 10px; font-weight: bold;")
            QMessageBox.warning(self, "Hata", f"Çözüm bulunamadı!\nDurum: {status}\n\nBu durum, katı kısıtların sağlanamadığı anlamına gelir.")
    
    def on_solve_error(self, error_msg: str):
        """Motor hatası"""
        self.progress_bar.setVisible(False)
        self.status_label.setText("Hata oluştu!")
        self.status_label.setStyleSheet("color: #ef4444; padding: 10px; font-weight: bold;")
        QMessageBox.critical(self, "Hata", f"Motor hatası:\n{error_msg}")
    
    def export_excel(self):
        if not hasattr(self, 'current_solution'):
            QMessageBox.warning(self, "Hata", "Önce motoru çalıştırın!")
            return
        
        default_filename = "Final_Program.xlsx"
        if self.current_program_id:
            program = self.db.get_program(self.current_program_id)
            if program and program.program_adi:
                safe_name = program.program_adi.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")
                default_filename = f"{safe_name}.xlsx"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Excel Dosyasını Kaydet", default_filename,
            "Excel Dosyaları (*.xlsx)"
        )
        
        if filename:
            try:
                exporter = ExcelExporter()
                all_class_levels = self.current_solution.get('all_class_levels')
                exporter.export(self.current_solution, filename, all_class_levels=all_class_levels)
                QMessageBox.information(self, "Başarılı", f"Dosya kaydedildi:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kayıt hatası:\n{str(e)}")
    
    def export_pdf(self):
        """PDF olarak kaydet"""
        if not hasattr(self, 'current_solution'):
            QMessageBox.warning(self, "Hata", "Önce motoru çalıştırın!")
            return
        
        # Aktif program adını al
        default_filename = "Final_Program.pdf"
        if self.current_program_id:
            program = self.db.get_program(self.current_program_id)
            if program and program.program_adi:
                # Dosya adı için güvenli karakterlere dönüştür
                safe_name = program.program_adi.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")
                default_filename = f"{safe_name}.pdf"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "PDF Dosyasını Kaydet", default_filename,
            "PDF Dosyaları (*.pdf)"
        )
        
        if filename:
            try:
                exporter = PDFExporter()
                # Tüm sınıf seviyelerini solution'dan al (Excel export ile aynı)
                all_class_levels = self.current_solution.get('all_class_levels')
                pdf_path = exporter.export(self.current_solution, filename, all_class_levels=all_class_levels)
                if pdf_path:
                    QMessageBox.information(self, "Başarılı", f"PDF dosyası kaydedildi:\n{pdf_path}")
                else:
                    QMessageBox.warning(
                        self, "Uyarı",
                        "PDF dönüştürme başarısız oldu.\n"
                        "Lütfen Excel dosyasını manuel olarak PDF'e dönüştürün."
                    )
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"PDF kayıt hatası:\n{str(e)}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

