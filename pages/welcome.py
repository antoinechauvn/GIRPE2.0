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

        # Connecter le bouton à l'affichage du deuxième TeachingTip
        next_button.clicked.connect(self.show_player_teaching_tip)

        self.party_tip = TeachingTip.make(
            target=main_window.navigationInterface.widget(main_window.partyInterface.objectName()),
            view=view,
            duration=-1,
            tailPosition=TeachingTipTailPosition.LEFT,
            parent=main_window
        )
        view.closed.connect(self.party_tip.close)

    def show_player_teaching_tip(self):
        # Fermer le TeachingTip précédent
        if hasattr(self, 'party_tip'):
            self.party_tip.close()
            
        # Accéder à la fenêtre principale
        main_window = self.window()
        
        # Créer et afficher le TeachingTip pour les joueurs
        player_view = TeachingTipView(
            icon=FIF.PEOPLE,
            title='Gérer les joueurs',
            content="Accédez à cette section pour gérer vos joueurs.\nVous pouvez ajouter, modifier ou rechercher des joueurs.",
            image=None,
            isClosable=True,
            tailPosition=TeachingTipTailPosition.NONE,
        )

        # Ajouter un bouton pour continuer
        player_next_button = PrimaryPushButton('Continuer')
        player_next_button.setFixedWidth(120)
        player_view.addWidget(player_next_button, align=Qt.AlignRight)
        
        # Connecter le bouton à l'affichage du Flyout final
        player_next_button.clicked.connect(self.show_final_flyout)

        self.player_tip = TeachingTip.make(
            target=main_window.navigationInterface.widget(main_window.playerInterface.objectName()),
            view=player_view,
            duration=-1,
            tailPosition=TeachingTipTailPosition.LEFT,
            parent=main_window
        )
        player_view.closed.connect(self.player_tip.close)

    def show_final_flyout(self):
        # Fermer le TeachingTip précédent
        if hasattr(self, 'player_tip'):
            self.player_tip.close()

        # Créer la vue finale
        view = FlyoutView(
            title='Tutoriel terminé !',
            content="Félicitations ! Vous avez terminé le tutoriel de GIRPE 2.0.\nVous pouvez maintenant créer des parties et gérer vos joueurs.\n\nBon match !",
            image=os.path.join(os.path.dirname(os.path.dirname(__file__)), "resource", "flyout2.jpg"),
            isClosable=True
        )

        # Ajouter un bouton pour terminer
        finish_button = PrimaryPushButton('Terminer')
        finish_button.setFixedWidth(120)
        view.addWidget(finish_button, align=Qt.AlignRight)

        # Ajuster le layout
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.addSpacing(5)

        # Afficher le Flyout final
        self.final_flyout = Flyout.make(view, self.tutorial_button, self, aniType=FlyoutAnimationType.FADE_IN)
        view.closed.connect(self.final_flyout.close)

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
