import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QAction, QFileDialog,
                             QMessageBox, QFontComboBox, QSpinBox)
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtCore import Qt
import os

from ui_qt_deneme_1 import Ui_MainWindow 

class NotepadApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Arayüzü yükle
        self.current_file = None  # Açık dosya yok
        self.createActions()  # Menü eylemleri oluştur
        self.addActionsToMenus()  # Menüye eylemleri ekle
        self.connectActions()  # Sinyal-slot bağlantılarını kur
        self.setupEditor()  # Metin editörünü ayarla
        self.setupToolbar()  # Araç çubuğunu ayarla

    def createActions(self):
        # Menü ve butonlar için eylemler
        self.actionYeni = QAction('Yeni', self)
        self.actionYeni.setShortcut(QKeySequence.New)

        self.actionAc = QAction('Aç...', self)
        self.actionAc.setShortcut(QKeySequence.Open)

        self.actionKaydet = QAction('Kaydet', self)
        self.actionKaydet.setShortcut(QKeySequence.Save)

        self.actionFarkliKaydet = QAction('Farklı Kaydet...', self)
        self.actionFarkliKaydet.setShortcut(QKeySequence.SaveAs)

        self.actionKapat = QAction('Çıkış', self)
        self.actionKapat.setShortcut(QKeySequence.Quit)

        self.actionKes = QAction('Kes', self)
        self.actionKes.setShortcut(QKeySequence.Cut)

        self.actionKopyala = QAction( 'Kopyala', self)
        self.actionKopyala.setShortcut(QKeySequence.Copy)

        self.actionYapistir = QAction('Yapıştır', self)
        self.actionYapistir.setShortcut(QKeySequence.Paste)

        self.actionBold = QAction('Bold', self)
        self.actionBold.setShortcut(QKeySequence.Bold)
        self.actionBold.setCheckable(True)

        self.actionItalik = QAction('İtalik', self)
        self.actionItalik.setShortcut(QKeySequence.Italic)
        self.actionItalik.setCheckable(True)

    def addActionsToMenus(self):
        # Menüye eylemleri ekle
        self.menuYeni.addAction(self.actionYeni)
        self.menuA.addAction(self.actionAc)
        self.menuKaydet.addAction(self.actionKaydet)
        self.menuKaydet.addAction(self.actionFarkliKaydet)
        self.menuKapat.addAction(self.actionKapat)

    def connectActions(self):
        # Eylemleri fonksiyonlara bağla
        self.actionYeni.triggered.connect(self.newFile)
        self.actionAc.triggered.connect(self.openFile)
        self.actionKaydet.triggered.connect(self.saveFile)
        self.actionFarkliKaydet.triggered.connect(self.saveAsFile)
        self.actionKapat.triggered.connect(self.close)

        # Kes, kopyala, yapıştır
        self.pushButton_5.clicked.connect(self.textEdit.cut)
        self.pushButton_4.clicked.connect(self.textEdit.copy)
        self.pushButton.clicked.connect(self.textEdit.paste)

        # Yazı tipi ve boyutu değişiklikleri
        self.fontComboBox.currentFontChanged.connect(self.textEdit.setCurrentFont)
        self.spinBox.valueChanged.connect(self.changeFontSize)

        # Kalın ve italik biçimlendirme
        self.pushButton_2.clicked.connect(self.toggleBold)
        self.pushButton_3.clicked.connect(self.toggleItalic)

        # Biçimlendirme değiştikçe arayüzü güncelle
        self.textEdit.currentCharFormatChanged.connect(self.updateFormatToolbar)
        # Belge değişince başlığı güncelle
        self.textEdit.document().contentsChanged.connect(self.documentModified)

    def setupEditor(self):
        # Varsayılan yazı tipi ve boyut
        self.textEdit.setFont(QFont("MS Shell Dlg 2", 10))
        self.spinBox.setValue(10)
        self.textEdit.setPlaceholderText("Buraya metin girin...")

    def setupToolbar(self):
        # Kalın ve italik butonları seçilebilir yapılsın
        self.pushButton_2.setCheckable(True)
        self.pushButton_3.setCheckable(True)

    def documentModified(self):
        # Belge değiştiğinde başlığa * ekle
        title = f'Basit Not Defteri - {os.path.basename(self.current_file)}*' if self.current_file else 'Basit Not Defteri*'
        self.setWindowTitle(title)

    def newFile(self):
        # Yeni dosya oluştururken değişiklik varsa uyar
        if self.textEdit.document().isModified():
            reply = QMessageBox.question(self, 'Kaydet', 'Mevcut dosyayı kaydetmek istiyor musunuz?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes and self.saveFile():
                self.textEdit.clear()
            elif reply == QMessageBox.No:
                self.textEdit.clear()
            else:
                return
        else:
            self.textEdit.clear()
        self.current_file = None
        self.setWindowTitle('Basit Not Defteri')

    def openFile(self):
        # Dosya açma işlemi
        file_name, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    self.textEdit.setPlainText(f.read())
                self.current_file = file_name
                self.setWindowTitle(f'Basit Not Defteri - {os.path.basename(self.current_file)}')
                self.textEdit.document().setModified(False)
            except Exception as e:
                QMessageBox.critical(self, 'Hata', f'Dosya açılamadı: {e}')

    def saveFile(self):
        # Dosya kaydetme işlemi
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.textEdit.toPlainText())
                self.textEdit.document().setModified(False)
                self.setWindowTitle(f'Basit Not Defteri - {os.path.basename(self.current_file)}')
                return True
            except Exception as e:
                QMessageBox.critical(self, 'Hata', f'Dosya kaydedilemedi: {e}')
                return False
        return self.saveAsFile()

    def saveAsFile(self):
        # Farklı kaydet işlemi
        file_name, _ = QFileDialog.getSaveFileName(self, "Dosyayı Kaydet", "", "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.textEdit.toPlainText())
                self.current_file = file_name
                self.setWindowTitle(f'Basit Not Defteri - {os.path.basename(self.current_file)}')
                self.textEdit.document().setModified(False)
                return True
            except Exception as e:
                QMessageBox.critical(self, 'Hata', f'Dosya kaydedilemedi: {e}')
        return False

    def closeEvent(self, event):
        # Uygulama kapatılırken kaydedilmemiş dosya varsa uyar
        if self.textEdit.document().isModified():
            reply = QMessageBox.question(self, 'Çıkış', 'Değişiklikleri kaydetmek istiyor musunuz?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes and self.saveFile():
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def changeFontSize(self, size):
        # Yazı boyutunu değiştir
        self.textEdit.setFontPointSize(size)

    def toggleBold(self):
        # Kalın yazı seçimi
        self.textEdit.setFontWeight(QFont.Bold if self.pushButton_2.isChecked() else QFont.Normal)

    def toggleItalic(self):
        # İtalik yazı seçimi
        self.textEdit.setFontItalic(self.pushButton_3.isChecked())

    def updateFormatToolbar(self, format):
        # Biçimlendirme değişince araç çubuğunu güncelle
        self.fontComboBox.setCurrentFont(format.font())
        self.spinBox.setValue(int(format.fontPointSize()))
        self.pushButton_2.setChecked(format.fontWeight() == QFont.Bold)
        self.pushButton_3.setChecked(format.fontItalic())

# Uygulama başlatılıyor
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = NotepadApp()
    mainWin.show()
    sys.exit(app.exec_())