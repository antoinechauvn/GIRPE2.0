# Standard library imports
import sys

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPixmap, QPainter
from qfluentwidgets import (
    setTheme, Theme, InfoBar, InfoBarPosition
)

from Ui_LoginWindow import Ui_Form
from Ui_MainWindow import Ui_MainWindow


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class LoginWindow(Window, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.titleBar.raise_()
        self.setWindowIcon(QIcon(":/newPrefix/images/logo.png"))
        
        # Connecter le signal de fin de progression
        self.progress_ring.progress_complete.connect(self.complete_login)
        
        # Connecter les signaux
        self.button_login.clicked.connect(self.login)
        self.username_edit.returnPressed.connect(self.password_edit.setFocus)
        self.password_edit.returnPressed.connect(self.login)

    def login(self):
        # Récupérer les identifiants
        self.username = self.username_edit.text().strip()
        self.password = self.password_edit.text().strip()

        # Désactiver le bouton de login
        self.button_login.setEnabled(False)

        # Vérifier les identifiants
        if self.verify_credentials(self.username, self.password):
            # Si les identifiants sont corrects, démarrer la progression
            self.progress_ring.show()
            self.progress_ring.start()
        else:
            # Réactiver le bouton
            self.button_login.setEnabled(True)

    def verify_credentials(self, username, password):
        if username == "admin" and password == "admin":
            return True
        else:
            # Afficher le message d'erreur
            InfoBar.error(
                title='Erreur de connexion',
                content="Nom d'utilisateur ou mot de passe incorrect",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            
            # Vider le champ du mot de passe
            self.password_edit.clear()
            self.password_edit.setFocus()
            return False
            
    def complete_login(self):
        # Cacher le progress ring et réactiver le bouton
        self.progress_ring.hide()
        self.button_login.setEnabled(True)
        
        # Créer et afficher la fenêtre principale
        self.main_window = Ui_MainWindow()
        self.main_window.show()
        self.close()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(r"c:\Users\CHAUVIN ANTOINE\PycharmProjects\GIRPE2.0\resource\images\news__20250225150811.jpg").scaled(
            self.background.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.background.setPixmap(pixmap)


if __name__ == '__main__':
    # enable high dpi scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # Modern way to handle high DPI scaling
    if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    app.exec()
