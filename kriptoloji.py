from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

alphabet = "abcçdefgğhıijklmnoöprsştuüvyzABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("⚡ Cyber Crypto Tool")
        self.setWindowIcon(QIcon("icon.ico"))
        self.resize(900, 550)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Metin gir...")
        self.input_text.setTabChangesFocus(True)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Anahtar (sayı)")

        btn_layout = QHBoxLayout()

        self.encrypt_btn = QPushButton("Şifrele")
        self.decrypt_btn = QPushButton("Çöz")
        self.copy_btn = QPushButton("Kopyala")
        self.clear_btn = QPushButton("Temizle")

        for btn in [self.encrypt_btn, self.decrypt_btn, self.copy_btn, self.clear_btn]:
            btn.setFixedHeight(45)
            btn_layout.addWidget(btn)

        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText("Sonuç...")
        self.output_text.setReadOnly(True)

        main_layout.addWidget(self.input_text, 3)
        main_layout.addWidget(self.key_input, 1)
        main_layout.addLayout(btn_layout, 1)
        main_layout.addWidget(self.output_text, 3)

        self.setLayout(main_layout)

        self.encrypt_btn.clicked.connect(self.encrypt)
        self.decrypt_btn.clicked.connect(self.decrypt)
        self.copy_btn.clicked.connect(self.copy_text)
        self.clear_btn.clicked.connect(self.clear_all)

    def encrypt(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()

        if not key.isdigit():
            self.output_text.setText("Anahtar sayı olmalı!")
            return

        key = int(key)
        result = ""

        for char in text:
            if char in alphabet:
                i = alphabet.index(char)
                result += alphabet[(i + key) % len(alphabet)]
            else:
                result += char

        self.output_text.setText(result)

    def decrypt(self):
        text = self.input_text.toPlainText()
        key = self.key_input.text()

        if not key.isdigit():
            self.output_text.setText("Anahtar sayı olmalı!")
            return

        key = int(key)
        result = ""

        for char in text:
            if char in alphabet:
                i = alphabet.index(char)
                result += alphabet[(i - key) % len(alphabet)]
            else:
                result += char

        self.output_text.setText(result)

    def copy_text(self):
        QApplication.clipboard().setText(self.output_text.toPlainText())

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()
        self.key_input.clear()

app = QApplication(sys.argv)

app.setStyleSheet("""
    QWidget {
        background-color: #020617;
        color: #22c55e;
        font-family: "JetBrains Mono", Consolas;
        font-weight: bold;
    }

    QTextEdit, QLineEdit {
        background-color: #020617;
        border: 2px solid #22c55e;
        border-radius: 10px;
        padding: 10px;
    }

    QTextEdit:focus, QLineEdit:focus {
        border: 2px solid #4ade80;
    }

    QPushButton {
        background-color: #022c22;
        border: 2px solid #22c55e;
        border-radius: 8px;
        padding: 10px;
    }

    QPushButton:hover {
        background-color: #22c55e;
        color: black;
    }
""")

window = CryptoApp()
window.show()

sys.exit(app.exec())