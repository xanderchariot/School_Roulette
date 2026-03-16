import sys
import json
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class StudentCard(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)
        self.setMinimumWidth(520)
        self.setStyleSheet("""
        QLabel{
        font-size:32px;
        font-weight:bold;
        padding:40px;
        border-radius:14px;
        background:qlineargradient(
            x1:0,y1:0,x2:1,y2:1,
            stop:0 #3b82f6,
            stop:1 #9333ea
        );
        color:white;
        }
        """)
        self.opacity = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity)
        self.anim = QPropertyAnimation(self.opacity, b"opacity")
        self.anim.setDuration(300)
    def show_text(self, text, list_mode=False):
        if list_mode:
            self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.setStyleSheet("""
            QLabel{
            font-size:22px;
            font-weight:bold;
            padding:40px;
            border-radius:14px;
            background:qlineargradient(
                x1:0,y1:0,x2:1,y2:1,
                stop:0 #3b82f6,
                stop:1 #9333ea
            );
            color:white;
            }
            """)
        else:
            self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        self.anim.stop()
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
    def show_text(self, text):
        self.setText(text)
        self.anim.stop()
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
class StudentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.uczniowie = []
        self.obecni = []
        self.index = 0
        self.draw_timer = QTimer()
        self.draw_timer.timeout.connect(self.show_next_draw)
        self.selected_students = []
        self.current_draw_index = 0
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle("🎓 Classroom Randomizer")
        self.resize(900,550)
        main_layout = QHBoxLayout()
        left = QVBoxLayout()
        center = QVBoxLayout()
        title = QLabel("Classroom Randomizer")
        title.setStyleSheet("font-size:26px;font-weight:bold;")
        left.addWidget(title)
        self.class_input = QLineEdit()
        self.class_input.setPlaceholderText("Podaj klasę np. 1A")
        left.addWidget(self.class_input)
        load_btn = QPushButton("Wczytaj klasę")
        load_btn.clicked.connect(self.load_class)
        left.addWidget(load_btn)
        left.addWidget(QLabel("Lista obecnych"))
        self.present_list = QListWidget()
        left.addWidget(self.present_list)
        left.addWidget(QLabel("Ilu uczniów odpowiada"))
        self.answer_spin = QSpinBox()
        self.answer_spin.setMinimum(1)
        left.addWidget(self.answer_spin)
        answer_btn = QPushButton("Losuj do odpowiedzi")
        answer_btn.clicked.connect(self.draw_answers)
        left.addWidget(answer_btn)
        main_layout.addLayout(left)
        self.card = StudentCard()
        center.addWidget(self.card)
        self.button_layout = QHBoxLayout()
        self.present_btn = QPushButton("✔ Obecny")
        self.present_btn.clicked.connect(self.mark_present)
        self.absent_btn = QPushButton("✖ Nieobecny")
        self.absent_btn.clicked.connect(self.mark_absent)
        self.button_layout.addWidget(self.present_btn)
        self.button_layout.addWidget(self.absent_btn)
        center.addLayout(self.button_layout)
        main_layout.addLayout(center)
        self.setLayout(main_layout)
        self.setStyleSheet("""
        QWidget{
        background:#0f172a;
        color:white;
        font-family:Segoe UI;
        font-size:14px;
        }
        QPushButton{
        background:#3b82f6;
        border:none;
        padding:10px;
        border-radius:8px;
        }
        QPushButton:hover{
        background:#2563eb;
        }
        QListWidget,QLineEdit{
        background:#1e293b;
        border-radius:8px;
        padding:6px;
        }
        """)
    def load_class(self):
        try:
            with open(self.class_input.text()+".json","r",encoding="utf-8") as f:
                data = json.load(f)
            self.uczniowie = list(data.values())
            self.index = 0
            self.obecni = []
            self.present_list.clear()
            self.present_btn.show()
            self.absent_btn.show()
            self.next_student()
        except:
            QMessageBox.warning(self,"Błąd","Nie znaleziono pliku")
    def next_student(self):
        if self.index >= len(self.uczniowie):
            self.card.show_text("Czekamy na szczęśliwców...")
            self.present_btn.hide()
            self.absent_btn.hide()
            return
        s = self.uczniowie[self.index]
        name = f"{s['imie']} {s['nazwisko']}"
        self.card.show_text(name)
    def mark_present(self):
        s = self.uczniowie[self.index]
        self.obecni.append(s)
        self.present_list.addItem(
            f"{s['imie']} {s['nazwisko']}"
        )
        self.index += 1
        self.next_student()
    def mark_absent(self):
        self.index += 1
        self.next_student()
    def draw_answers(self):
        n = self.answer_spin.value()
        if n > len(self.obecni):
            QMessageBox.warning(self,"Błąd","Za dużo uczniów")
            return
        self.selected_students = random.sample(self.obecni,n)
        self.current_draw_index = 0
        self.card.show_text("Wybrani uczniowie:\n")
        self.draw_timer.start(700)
    def show_next_draw(self):
        if self.current_draw_index >= len(self.selected_students):
            self.draw_timer.stop()
            return
        s = self.selected_students[self.current_draw_index]
        current_text = self.card.text()
        current_text += f"\n{s['imie']} {s['nazwisko']}"
        self.card.show_text(current_text)
        self.current_draw_index += 1
app = QApplication(sys.argv)
window = StudentApp()
window.show()
sys.exit(app.exec_())