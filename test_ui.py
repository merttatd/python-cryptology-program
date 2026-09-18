import os
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFontDatabase
from kriptoloji import CryptoApp


class InterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        # The offscreen Windows platform does not enumerate system fonts.
        for font in ("segoeui.ttf", "segoeuib.ttf", "consola.ttf"):
            QFontDatabase.addApplicationFont(os.path.join(os.environ.get("WINDIR", "C:/Windows"), "Fonts", font))
        cls.app.setStyle("Fusion")

    def setUp(self):
        self.window = CryptoApp()

    def tearDown(self):
        self.window.close()

    def test_buttons_and_round_trip(self):
        w = self.window
        for index, key in [(0, "3"), (1, "GÜNEŞ"), (2, ""), (3, "3"), (4, "")]:
            w.method_combo.setCurrentIndex(index)
            w.input_text.setPlainText("İstanbul <b>ışık</b> 🙂")
            w.key_input.setText(key)
            w.encrypt_btn.click()
            self.assertTrue(w.copy_btn.isEnabled())
            w.copy_btn.click()
            self.assertEqual(self.app.clipboard().text(), w.output_text.toPlainText())
            w.use_btn.click()
            w.decrypt_btn.click()
            self.assertEqual(w.output_text.toPlainText(), "İstanbul <b>ışık</b> 🙂")
        w.clear_btn.click()
        self.assertFalse(w.copy_btn.isEnabled())
        self.assertEqual(w.input_text.toPlainText(), "")

    def test_method_controls_and_errors(self):
        w = self.window
        w.method_combo.setCurrentIndex(5)
        self.assertFalse(w.decrypt_btn.isEnabled())
        self.assertFalse(w.key_input.isEnabled())
        w.input_text.setPlainText("abc")
        w.encrypt_btn.click()
        self.assertEqual(len(w.output_text.toPlainText()), 64)
        w.method_combo.setCurrentIndex(0)
        self.assertEqual(w.output_text.toPlainText(), "")
        w.encrypt_btn.click()
        self.assertTrue(w.status.property("error"))
        self.assertEqual(w.output_text.toPlainText(), "")
        w.clear_btn.click()
        w.encrypt_btn.click()
        self.assertTrue(w.status.property("error"))

    def test_layout_preview(self):
        w = self.window
        w.method_combo.setCurrentIndex(1)
        w.key_input.setText("GÜNEŞ")
        w.input_text.setPlainText("Merhaba dünya!\n\nTürkçe karakterlerle kriptografiyi keşfet:\nç ğ ı İ ö ş ü")
        w.encrypt_btn.click()
        w.show()
        self.app.processEvents()
        with TemporaryDirectory() as directory:
            self.assertTrue(w.grab().save(str(Path(directory) / "preview.png")))
            w.resize(800, 620)
            self.app.processEvents()
            self.assertTrue(w.grab().save(str(Path(directory) / "preview_small.png")))


if __name__ == "__main__":
    unittest.main()
