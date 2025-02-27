from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import HorizontalSeparator, PillToolButton
from qfluentwidgets import FluentIcon as FIF


class PlayerWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setObjectName("PlayerWidget")

    def initUI(self):
        # Configurer le layout principal
        layout = QVBoxLayout(self)

        # Ajouter un message de bienvenue
        welcome_label = QLabel("TEST", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Ajouter un séparateur
        separator = HorizontalSeparator()
        layout.addWidget(separator)

        # Ajouter un titre pour le tutoriel
        tutorial_label = QLabel("Tutoriel rapide", self)
        tutorial_label.setAlignment(Qt.AlignCenter)
        tutorial_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(tutorial_label)

        # Créer et ajouter l'étape 1 avec un bouton collé au texte
        step1_layout = QHBoxLayout()
        step1_layout.setSpacing(0)  # Supprimer l'espacement entre les widgets
        step1_layout.setContentsMargins(0, 0, 0, 0)  # Supprimer les marges

        step1_label = QLabel("• Étape 1: Ouvrez le fichier PDF", self)
        step1_label.setAlignment(Qt.AlignLeft)
        step1_label.setStyleSheet("font-size: 14px; margin-top: 5px;")

        pillToolButton1 = PillToolButton(FIF.ADD, self)

        step1_layout.addWidget(step1_label)
        step1_layout.addWidget(pillToolButton1, 0, Qt.AlignLeft)  # Bouton aligné à gauche

        layout.addLayout(step1_layout)

        # Créer et ajouter l'étape 2 avec un bouton collé au texte
        step2_layout = QHBoxLayout()
        step2_layout.setSpacing(0)
        step2_layout.setContentsMargins(0, 0, 0, 0)

        step2_label = QLabel("• Étape 2: Utilisez les flèches pour naviguer", self)
        step2_label.setAlignment(Qt.AlignLeft)
        step2_label.setStyleSheet("font-size: 14px; margin-top: 5px;")

        pillToolButton2 = PillToolButton(FIF.ADD, self)

        step2_layout.addWidget(step2_label)
        step2_layout.addWidget(pillToolButton2, 0, Qt.AlignLeft)

        layout.addLayout(step2_layout)

        # Créer et ajouter l'étape 3 avec un bouton collé au texte
        step3_layout = QHBoxLayout()
        step3_layout.setSpacing(0)
        step3_layout.setContentsMargins(0, 0, 0, 0)

        step3_label = QLabel("• Étape 3: Ajoutez des annotations si nécessaire", self)
        step3_label.setAlignment(Qt.AlignLeft)
        step3_label.setStyleSheet("font-size: 14px; margin-top: 5px;")

        pillToolButton3 = PillToolButton(FIF.ADD, self)

        step3_layout.addWidget(step3_label)
        step3_layout.addWidget(pillToolButton3, 0, Qt.AlignLeft)

        layout.addLayout(step3_layout)

        # Ajouter un espace vide en bas pour centrer verticalement le contenu
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Appliquer un layout principal au frame
        self.setLayout(layout)

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from qfluentwidgets import HorizontalSeparator, PillToolButton
from qfluentwidgets import FluentIcon as FIF


class PlayerWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setObjectName("PlayerWidget")

    def initUI(self):
        # Configurer le layout principal
        layout = QVBoxLayout(self)

        # Ajouter un message de bienvenue
        welcome_label = QLabel("TEST", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)

        # Ajouter un séparateur
        separator = HorizontalSeparator()
        layout.addWidget(separator)

        # Ajouter un titre pour le tutoriel
        tutorial_label = QLabel("Tutoriel rapide", self)
        tutorial_label.setAlignment(Qt.AlignCenter)
        tutorial_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(tutorial_label)

        # Créer et ajouter l'étape 1 avec un bouton collé au texte
        step1_layout = QHBoxLayout()
        step1_layout.setSpacing(0)  # Supprimer l'espacement entre les widgets
        step1_layout.setContentsMargins(0, 0, 0, 0)  # Supprimer les marges

        step1_label = QLabel("• Étape 1: Ouvrez le fichier PDF", self)
        step1_label.setAlignment(Qt.AlignLeft)
        step1_label.setStyleSheet("font-size: 14px; margin-top: 5px;")

        pillToolButton1 = PillToolButton(FIF.ADD, self)

        step1_layout.addWidget(step1_label)
        step1_layout.addWidget(pillToolButton1, 0, Qt.AlignLeft)  # Bouton aligné à gauche

        layout.addLayout(step1_layout)

        # Créer et ajouter l'étape 2 avec un bouton collé au texte
        step2_layout = QHBoxLayout()
        step2_layout.setSpacing(0)
        step2_layout.setContentsMargins(0, 0, 0, 0)

        step2_label = QLabel("• Étape 2: Utilisez les flèches pour naviguer", self)
        step2_label.setAlignment(Qt.AlignLeft)
        step2_label.setStyleSheet("font-size: 14px; margin-top: 5px;")

        pillToolButton2 = PillToolButton(FIF.ADD, self)

        step2_layout.addWidget(step2_label)
        step2_layout.addWidget(pillToolButton2, 0, Qt.AlignLeft)

        layout.addLayout(step2_layout)

        # Créer et ajouter l'étape 3 avec un bouton collé au texte
        step3_layout = QHBoxLayout()
        step3_layout.setSpacing(0)
        step3_layout.setContentsMargins(0, 0, 0, 0)

        step3_label = QLabel("• Étape 3: Ajoutez des annotations si nécessaire", self)
        step3_label.setAlignment(Qt.AlignLeft)
        step3_label.setStyleSheet("font-size: 14px; margin-top: 5px;")

        pillToolButton3 = PillToolButton(FIF.ADD, self)

        step3_layout.addWidget(step3_label)
        step3_layout.addWidget(pillToolButton3, 0, Qt.AlignLeft)

        layout.addLayout(step3_layout)

        # Ajouter un espace vide en bas pour centrer verticalement le contenu
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Appliquer un layout principal au frame
        self.setLayout(layout)
