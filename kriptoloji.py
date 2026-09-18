import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from PyQt6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSplitter, QTextEdit, QVBoxLayout, QWidget)
from crypto_methods import ALPHABET, transform

alphabet = ALPHABET
METHODS = [
    ("Sezar", "caesar", "Tam sayı · ör. 3", "Türkçe alfabe üzerinde kaydırma. Önceki sürümün 58 karakterlik sırası korunur."),
    ("Vigenère", "vigenere", "Anahtar sözcük · ör. GÜNEŞ", "Türkçe alfabe ile çoklu kaydırma. Harf büyüklüğü ve noktalama korunur."),
    ("Atbash", "atbash", "Anahtar gerektirmez", "Türkçe alfabenin harflerini ters sıradaki karşılıklarıyla değiştirir."),
    ("Raylı Çit", "rail", "Ray sayısı · 2–100", "Metni zikzak satırlara dağıtarak karakterlerin yerini değiştirir."),
    ("Base64 · Kodlama", "base64", "Anahtar gerektirmez", "UTF-8 metni Base64 biçimine dönüştürür. Şifreleme değildir."),
    ("SHA-256 · Özet", "sha256", "Anahtar gerektirmez", "Metnin 256 bit özetini üretir. Tek yönlüdür; geri çözülemez."),
]
STYLE = """
QWidget { background: #0c1220; color: #e6edf7; font-family: 'Segoe UI'; font-size: 14px; }
QLabel#eyebrow { color: #6de1c2; font-size: 12px; font-weight: 700; }
QLabel#title { font-size: 30px; font-weight: 700; }
QLabel#muted, QLabel#count { color: #94a5bd; }
QFrame#card { background: #141e30; border: 1px solid #26344b; border-radius: 14px; }
QFrame#card QLabel { background: transparent; }
QLabel#section { font-weight: 600; font-size: 15px; }
QTextEdit, QLineEdit, QComboBox { background: #0e1727; border: 1px solid #33435c; border-radius: 8px; padding: 10px; selection-background-color: #286f79; }
QTextEdit { font-family: 'Consolas'; font-size: 15px; }
QTextEdit:focus, QLineEdit:focus, QComboBox:focus { border-color: #6de1c2; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox QAbstractItemView { background: #18243a; selection-background-color: #286f79; }
QPushButton { background: #20304a; border: 1px solid #354761; border-radius: 8px; padding: 11px 18px; font-weight: 600; }
QPushButton:hover { background: #2c4261; border-color: #8299b9; }
QPushButton:pressed { background: #17263e; }
QPushButton#primary { background: #6de1c2; color: #082a29; border: 1px solid #6de1c2; }
QPushButton#primary:hover { background: #99efd8; }
QPushButton:disabled, QLineEdit:disabled { color: #65738a; background: #141e30; border-color: #26344b; }
QSplitter::handle { background: #0c1220; width: 12px; }
QLabel#status { color: #6de1c2; }
QLabel#status[error="true"] { color: #ffaaa5; }
"""


class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kripto Atölyesi")
        self.setWindowIcon(QIcon(str(Path(__file__).with_name("icon.ico"))))
        self.resize(1120, 740)
        self.setMinimumSize(800, 620)
        self.setStyleSheet(STYLE)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 26, 30, 22)
        layout.setSpacing(16)
        layout.addWidget(self.label("KRİPTO ATÖLYESİ / METİN ARAÇLARI", "eyebrow"))
        layout.addWidget(self.label("Kelimelerin başka bir hâli.", "title"))
        layout.addWidget(self.label("Bir yöntem seçin, metninizi dönüştürün ve sonucu keşfedin.", "muted"))
        settings = QFrame()
        settings.setObjectName("card")
        settings_layout = QVBoxLayout(settings)
        settings_layout.setContentsMargins(18, 16, 18, 16)
        fields = QHBoxLayout()
        self.method_combo = QComboBox()
        self.method_combo.setAccessibleName("Kriptografi yöntemi")
        for title, code, _, _ in METHODS:
            self.method_combo.addItem(title, code)
        self.key_input = QLineEdit()
        self.key_input.setAccessibleName("Anahtar")
        for title, widget in [("YÖNTEM", self.method_combo), ("ANAHTAR", self.key_input)]:
            column = QVBoxLayout()
            column.addWidget(self.label(title, "muted"))
            column.addWidget(widget)
            fields.addLayout(column, 1)
        settings_layout.addLayout(fields)
        self.method_description = self.label("", "muted")
        self.method_description.setWordWrap(True)
        settings_layout.addWidget(self.method_description)
        layout.addWidget(settings)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.input_text = QTextEdit()
        self.input_text.setAcceptRichText(False)
        self.input_text.setPlaceholderText("Dönüştürmek istediğiniz metni buraya yazın…")
        self.input_text.setAccessibleName("Giriş metni")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Sonucunuz burada görünecek…")
        self.output_text.setAccessibleName("Sonuç metni")
        self.input_count = self.label("0 karakter", "count")
        self.output_count = self.label("0 karakter", "count")
        for title, editor, count in [("01 / Giriş metni", self.input_text, self.input_count), ("02 / Sonuç", self.output_text, self.output_count)]:
            editor.setTabChangesFocus(True)
            panel = QFrame()
            panel.setObjectName("card")
            panel_layout = QVBoxLayout(panel)
            panel_layout.setContentsMargins(16, 16, 16, 12)
            panel_layout.addWidget(self.label(title, "section"))
            panel_layout.addWidget(editor)
            panel_layout.addWidget(count)
            splitter.addWidget(panel)
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter, 1)
        buttons = QHBoxLayout()
        self.encrypt_btn = QPushButton("Şifrele")
        self.encrypt_btn.setObjectName("primary")
        self.decrypt_btn = QPushButton("Çöz")
        self.use_btn = QPushButton("Girişe aktar")
        self.copy_btn = QPushButton("Kopyala")
        self.clear_btn = QPushButton("Temizle")
        for button, action in [(self.encrypt_btn, self.encrypt), (self.decrypt_btn, self.decrypt), (self.use_btn, self.use_output), (self.copy_btn, self.copy_text), (self.clear_btn, self.clear_all)]:
            buttons.addWidget(button)
            button.clicked.connect(action)
        layout.addLayout(buttons)
        self.status = self.label("Hazır. Başlamak için metin girin.", "status")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        note = self.label("Klasik şifreler eğitim amaçlıdır; hassas verileri korumak için uygun değildir. İşlemler cihazınızda yapılır.", "muted")
        note.setWordWrap(True)
        layout.addWidget(note)
        self.method_combo.currentIndexChanged.connect(self.method_changed)
        self.input_text.textChanged.connect(self.update_counts)
        self.output_text.textChanged.connect(self.update_counts)
        self.key_input.returnPressed.connect(self.encrypt)
        self.shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.shortcut.activated.connect(self.encrypt)
        self.encrypt_btn.setToolTip("Ctrl+Enter")
        self.method_changed()

    @staticmethod
    def label(text, name):
        label = QLabel(text)
        label.setObjectName(name)
        return label

    def set_status(self, message, error=False):
        self.status.setText(message)
        self.status.setProperty("error", error)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def method_changed(self):
        _, method, placeholder, description = METHODS[self.method_combo.currentIndex()]
        self.key_input.clear()
        self.key_input.setEnabled(method in ("caesar", "vigenere", "rail"))
        self.key_input.setPlaceholderText(placeholder)
        self.method_description.setText(description)
        self.encrypt_btn.setText("Özet oluştur" if method == "sha256" else "Kodla" if method == "base64" else "Şifrele")
        self.decrypt_btn.setText("Kod çöz" if method == "base64" else "Çöz")
        self.decrypt_btn.setEnabled(method != "sha256")
        self.output_text.clear()
        self.update_counts()
        self.set_status("Hazır. Ctrl+Enter ile hızlıca dönüştürebilirsiniz.")

    def update_counts(self):
        self.input_count.setText(f"{len(self.input_text.toPlainText()):,} karakter")
        size = len(self.output_text.toPlainText())
        self.output_count.setText(f"{size:,} karakter")
        self.copy_btn.setEnabled(size > 0)
        self.use_btn.setEnabled(size > 0)

    def run_transform(self, decrypt=False):
        text = self.input_text.toPlainText()
        if not text:
            self.output_text.clear()
            self.set_status("Önce giriş alanına bir metin yazın.", True)
            self.input_text.setFocus()
            return
        try:
            result = transform(text, self.method_combo.currentData(), self.key_input.text(), decrypt)
        except ValueError as error:
            self.output_text.clear()
            self.set_status(str(error), True)
            return
        self.output_text.setPlainText(result)
        self.set_status(f"{self.method_combo.currentText()} · İşlem tamamlandı.")

    def encrypt(self):
        self.run_transform()

    def decrypt(self):
        self.run_transform(True)

    def use_output(self):
        self.input_text.setPlainText(self.output_text.toPlainText())
        self.output_text.clear()
        self.set_status("Sonuç girişe aktarıldı. Yeni bir işlem yapabilirsiniz.")

    def copy_text(self):
        QApplication.clipboard().setText(self.output_text.toPlainText())
        self.set_status("Sonuç panoya kopyalandı.")

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()
        self.key_input.clear()
        self.set_status("Tüm alanlar temizlendi.")
        self.input_text.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = CryptoApp()
    window.show()
    sys.exit(app.exec())
