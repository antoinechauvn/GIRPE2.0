from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from qfluentwidgets import (PrimaryPushButton, FluentIcon as FIF, Flyout, 
                          FlyoutView, FlyoutAnimationType, TeachingTip,
                          TeachingTipView, TeachingTipTailPosition, NavigationWidget)
import os

class WelcomeWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("Bienvenue")
        self.initUI()
        self.flyout_window = None

    def initUI(self):
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Titre de bienvenue
        welcome_label = QLabel("Bienvenue dans GIRPE 2.0", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #1a1a1a;
            }
        """)
        layout.addWidget(welcome_label)

        # Bouton tutoriel
        self.tutorial_button = PrimaryPushButton("Démarrer le tutoriel", self)
        self.tutorial_button.setIcon(FIF.HELP)
        self.tutorial_button.clicked.connect(self.start_tutorial)
        layout.addWidget(self.tutorial_button, 0, Qt.AlignCenter)

    def show_teaching_tip(self):
        # Fermer le Flyout avant d'afficher le TeachingTip
        if self.flyout_window:
            self.flyout_window.close()
            
        # Accéder à la fenêtre principale
        main_window = self.window()
        
        # Créer et afficher le TeachingTip
        view = TeachingTipView(
            icon=FIF.ADD,
            title='Créer une partie',
            content="Cliquez ici pour créer une nouvelle partie.\nVous pourrez y ajouter les joueurs et les scores.",
            image=None,
            isClosable=True,
            tailPosition=TeachingTipTailPosition.NONE,
        )

        # Ajouter un bouton pour continuer
        next_button = PrimaryPushButton('Continuer')
        next_button.setFixedWidth(120)
        view.addWidget(next_button, align=Qt.AlignRight)

        w = TeachingTip.make(
            target=main_window.navigationInterface.widget(main_window.partyInterface.objectName()),
            view=view,
            duration=-1,
            tailPosition=TeachingTipTailPosition.LEFT,
            parent=main_window
        )
        view.closed.connect(w.close)

    def start_tutorial(self):
        # Créer la vue du Flyout
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resource", "flyout1.png")
        view = FlyoutView(
            title='Tutoriel GIRPE 2.0',
            content="Bienvenue dans le tutoriel de GIRPE 2.0.\nSuivez les étapes pour apprendre à utiliser l'application.",
            image=image_path,
            isClosable=True
        )

        # Ajouter un bouton "Suivant"
        next_button = PrimaryPushButton('Suivant')
        next_button.setFixedWidth(120)
        next_button.clicked.connect(self.show_teaching_tip)
        view.addWidget(next_button, align=Qt.AlignRight)

        # Ajuster le layout
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.addSpacing(5)

        # Afficher le Flyout
        self.flyout_window = Flyout.make(view, self.tutorial_button, self, aniType=FlyoutAnimationType.FADE_IN)
        view.closed.connect(self.flyout_window.close)
