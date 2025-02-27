# Third-party imports
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QCompleter
)
from PySide6.QtCore import Qt
from qfluentwidgets import (
    PrimaryPushButton, FluentIcon, SearchLineEdit,
    ComboBox, InfoBar)

# Local imports
from pages.match import MatchWidget
from utils.match_manager import MatchManager


class PartyWidget(QFrame):
    """Widget pour la création d'une nouvelle partie."""
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_window = parent
        self.match_manager = MatchManager(parent=self, main_window=parent)
        
        # UI
        self.initUI()
    
    def initUI(self):
        """Initialise l'interface utilisateur."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Ajouter un espace extensible en haut
        layout.addStretch()
        
        # Label principal
        welcome_label = QLabel("Feuille de Match", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(welcome_label)
        
        # ComboBox pour le nombre de joueurs
        self.division_combo = ComboBox(self)
        self.division_combo.setPlaceholderText("JOUEURS")
        self.division_combo.addItems(["4", "3", "2", "1"])
        self.division_combo.setCurrentIndex(-1)
        self.division_combo.setFixedWidth(200)
        layout.addWidget(self.division_combo, 0, Qt.AlignCenter)
        
        # Layout pour les clubs
        clubs_layout = QHBoxLayout()
        clubs_layout.setSpacing(10)
        
        # Club 1
        self.club1lineEdit = SearchLineEdit(self)
        self.club1lineEdit.setPlaceholderText("Club A")
        self.club1lineEdit.setFixedWidth(200)
        completer1 = QCompleter(["Club 1", "Club 2", "Club 3", "Club 4", "Club 5"], self)
        self.club1lineEdit.setCompleter(completer1)
        
        # Label "Contre"
        label2 = QLabel("Contre", self)
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet("font-size: 14px;")
        label2.setFixedWidth(80)
        
        # Club 2
        self.club2lineEdit = SearchLineEdit(self)
        self.club2lineEdit.setPlaceholderText("Club B")
        self.club2lineEdit.setFixedWidth(200)
        completer2 = QCompleter(["Club 1", "Club 2", "Club 3", "Club 4", "Club 5"], self)
        self.club2lineEdit.setCompleter(completer2)
        
        # Ajout au layout horizontal avec centrage
        clubs_layout.addStretch()
        clubs_layout.addWidget(self.club1lineEdit)
        clubs_layout.addWidget(label2)
        clubs_layout.addWidget(self.club2lineEdit)
        clubs_layout.addStretch()
        
        layout.addLayout(clubs_layout)
        
        # Bouton de création
        self.create_match_button = PrimaryPushButton('Créer une nouvelle partie', self, icon=FluentIcon.ADD)
        self.create_match_button.setFixedWidth(300)
        self.create_match_button.clicked.connect(self._create_match)
        layout.addWidget(self.create_match_button, 0, Qt.AlignCenter)
        
        # Ajouter un espace extensible en bas
        layout.addStretch()
    
    def _create_match(self):
        """Appelle la méthode create_match du MatchManager."""
        nb_players = self.division_combo.currentText()
        club1 = self.club1lineEdit.text().strip()
        club2 = self.club2lineEdit.text().strip()
        
        if nb_players and club1 and club2:
            # Vérifier si la limite de matchs est atteinte
            if self.match_manager.has_reached_match_limit():
                InfoBar.warning(
                    title='Limite atteinte',
                    content='Il y a déjà 8 matchs en cours. Impossible d\'en créer plus.',
                    parent=self
                )
                return
            
            self.match_manager.create_match(nb_players, club1, club2)
