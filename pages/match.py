# Third-party imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QFrame, QLabel, QHBoxLayout, QPushButton, QDialog, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import time
from qfluentwidgets import (
    SegmentedWidget, Action, FluentIcon, CommandBar,
    SubtitleLabel, LineEdit, CaptionLabel, MessageBoxBase, InfoBar
)

# Local imports
from widgets.editor import EditorWidget


class MatchWidget(QWidget):
    """Widget pour l'affichage et la gestion d'un match."""
    
    def __init__(self, pdf_path: str, excel_path: str, club1: str = "Club A", club2: str = "Club B", parent=None):
        super().__init__(parent)
        
        # Données du match
        self.pdf_path = pdf_path
        self.excel_path = excel_path
        self.club1 = club1
        self.club2 = club2
        self.main_window = parent
        
        # Joueurs des équipes
        self.club1_j1 = ""
        self.club1_j2 = ""
        self.club1_j3 = ""
        self.club1_j4 = ""
        self.club2_j1 = ""
        self.club2_j2 = ""
        self.club2_j3 = ""
        self.club2_j4 = ""
        
        # UI
        self.initUI()
    
    def initUI(self):
        """Initialise l'interface utilisateur."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Segmented control et stack
        self.segment = SegmentedWidget(self)
        self.stack = QStackedWidget(self)
        layout.addWidget(self.segment)
        layout.addWidget(self.stack)
        
        # Widgets d'édition et d'info
        self.editor = EditorWidget(self.pdf_path)
        self.editor.setObjectName('match_sheet')
        self.info_widget = MatchInfo(self)
        self.info_widget.setObjectName('match_info')
        
        # Configuration du stack et segment
        self.stack.addWidget(self.editor)
        self.stack.addWidget(self.info_widget)
        self.segment.addItem(routeKey='match_sheet', text='Feuille de match')
        self.segment.addItem(routeKey='match_info', text='Informations')
        
        # État initial
        self.stack.setCurrentWidget(self.editor)
        self.segment.setCurrentItem('match_sheet')
        
        # Connexion
        self.segment.currentItemChanged.connect(
            lambda k: self.stack.setCurrentWidget(self.findChild(QWidget, k))
        )


class MatchInfo(QFrame):
    """Widget d'informations pour un match."""
    
    def __init__(self, match_widget=None):
        super().__init__(match_widget)
        self.setObjectName("match_info")
        self.match_widget = match_widget
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Barre d'information avec les boutons d'équipe
        self.info_bar = InfoCommandBar(self)
        layout.addWidget(self.info_bar)
        
        layout.addStretch()


class InfoCommandBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initBar()
    
    def initBar(self):
        # Créer le layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Créer la barre de commandes
        self.commandBar = CommandBar(self)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        layout.addWidget(self.commandBar)
        
        # Créer et ajouter les actions
        add_action = Action(FluentIcon.ADD, 'Composition Équipe')
        add_action.triggered.connect(self.show_add_team_dialog)
        self.commandBar.addAction(add_action)
        
        edit_action = Action(FluentIcon.EDIT, 'Modifier Équipe')
        edit_action.triggered.connect(self.edit_team)
        self.commandBar.addAction(edit_action)
        
        # Stocker les références aux actions
        self.add_team_action = add_action
        self.edit_team_action = edit_action
    
    def show_add_team_dialog(self):
        """Affiche la boîte de dialogue pour ajouter une équipe."""
        match_widget = self.parent().parent().parent()
        dialog = TeamCompositionDialog(match_widget.club1, match_widget.club2, match_widget)
        if dialog.exec():
            players = dialog.get_players()
            # Assigner les joueurs aux variables
            match_widget.club1_j1 = players[0]
            match_widget.club1_j2 = players[1]
            match_widget.club1_j3 = players[2]
            match_widget.club1_j4 = players[3]
            match_widget.club2_j1 = players[4]
            match_widget.club2_j2 = players[5]
            match_widget.club2_j3 = players[6]
            match_widget.club2_j4 = players[7]
            
            # Mettre à jour le fichier Excel
            match_widget.main_window.partyInterface.match_manager.update_player(
                match_widget.excel_path,
                players,
                match_widget
            )
    
    def edit_team(self):
        """Affiche la boîte de dialogue pour modifier une équipe."""
        # TODO: Implémenter la boîte de dialogue de modification d'équipe
        InfoBar.success(
            title='Modification d\'équipe',
            content='Cette fonctionnalité sera bientôt disponible',
            duration=3000,
            parent=self.parent().parent().parent()
        )


class TeamCompositionDialog(MessageBoxBase):
    """Boîte de dialogue pour la composition des équipes."""
    
    def __init__(self, club1: str, club2: str, parent=None):
        super().__init__(parent)
        self.club1 = club1
        self.club2 = club2
        self.club1_players = []
        self.club2_players = []
        
        # Configuration du titre
        self.titleLabel = SubtitleLabel('Composition des Équipes', self)
        
        # Création du layout pour les équipes
        teams_layout = QHBoxLayout()
        
        # Layout pour l'équipe 1
        team1_layout = QVBoxLayout()
        team1_label = SubtitleLabel(club1, self)
        team1_layout.addWidget(team1_label)
        
        # Layout pour l'équipe 2
        team2_layout = QVBoxLayout()
        team2_label = SubtitleLabel(club2, self)
        team2_layout.addWidget(team2_label)
        
        # Ajout des LineEdit pour chaque équipe
        for i in range(4):
            # Équipe 1
            player1_input = LineEdit(self)
            player1_input.setPlaceholderText(f'Joueur {i+1}')
            team1_layout.addWidget(player1_input)
            self.club1_players.append(player1_input)
            
            # Équipe 2
            player2_input = LineEdit(self)
            player2_input.setPlaceholderText(f'Joueur {i+1}')
            team2_layout.addWidget(player2_input)
            self.club2_players.append(player2_input)
        
        # Ajout des layouts d'équipe au layout principal
        teams_layout.addLayout(team1_layout)
        teams_layout.addLayout(team2_layout)
        
        # Ajout des widgets au layout de la vue
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(teams_layout)
        
        # Configuration des boutons
        self.yesButton.setText('Valider')
        self.cancelButton.setText('Annuler')
        
        # Configuration de la taille minimale
        self.widget.setMinimumWidth(500)
    
    def get_players(self):
        """Récupère la liste des joueurs dans l'ordre."""
        players = []
        # Club 1
        for i in range(4):
            players.append(self.club1_players[i].text())
        # Club 2
        for i in range(4):
            players.append(self.club2_players[i].text())
        return players