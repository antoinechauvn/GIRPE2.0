from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from datetime import datetime
from qfluentwidgets import InfoBar, StateToolTip
from .excel_to_pdf import ExcelToPdfWorker
from pages.match import MatchWidget
from qfluentwidgets import FluentIcon as FIF, NavigationItemPosition
from utils.excel_to_pdf import ExcelToPdfWorker
import time
import os


class MatchManager(QObject):
    """Gestionnaire pour la création et la manipulation des fichiers de match."""
    
    _match_count = 0  # Compteur statique pour le numéro du match
    MAX_MATCHES = 8  # Nombre maximum de matchs autorisés
    
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.excel_worker = ExcelToPdfWorker()
        self.parent = parent
        self.main_window = main_window
    
    def create_match(self, nb_players: str, club1: str, club2: str):
        """
        Crée un nouveau fichier de match.
        
        Args:
            nb_players: Nombre de joueurs par équipe
            club1: Nom du club 1
            club2: Nom du club 2
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{club1}_vs_{club2}_{timestamp}"
        
        # Configuration des chemins
        self.excel_worker.set_paths(filename)
        
        # Création du fichier Excel
        InfoBar.success(
            title='Création du match',
            content='Création de la feuille de match...',
            duration=2000,
            parent=self.parent
        )
        self.excel_worker.create_excel_file()
        
        # Conversion en PDF
        InfoBar.success(
            title='Création du match',
            content='Conversion en PDF...',
            duration=2000,
            parent=self.parent
        )
        
        # Récupérer le thread de conversion
        thread = self.excel_worker.convert()
        if thread:
            # Fonction de callback qui se déconnecte après utilisation
            def on_finished():
                try:
                    thread.finished.disconnect()
                except TypeError:
                    pass  # Le signal était déjà déconnecté
                self.add_to_menu(club1, club2)
                
            # Connecter le signal avant de démarrer
            thread.finished.connect(on_finished)
            # Démarrer la conversion
            thread.start()
        
    def add_to_menu(self, club1: str, club2: str):
        """
        Met à jour l'interface en créant une nouvelle sous-interface pour le match.
        
        Args:
            club1: Nom du club 1
            club2: Nom du club 2
        """
        MatchManager._match_count += 1
        
        # Notification finale
        InfoBar.success(
            title='Match créé',
            content=f'Match {club1} vs {club2} créé avec succès !',
            duration=3000,
            parent=self.parent
        )
        
        # Créer le widget de match avec le chemin du PDF généré
        match_widget = MatchWidget(self.excel_worker.pdf_path, self.excel_worker.excel_path, club1, club2, self.main_window)
        match_widget.setObjectName(f"match_{club1}_{club2}")
        
        # Ajouter l'interface au UI_MainWindow en utilisant addSubInterface
        self.main_window.addSubInterface(
            interface=match_widget,
            icon=FIF.DOCUMENT,
            text=f"{club1} vs {club2}",
            position=NavigationItemPosition.SCROLL
        )

    def has_reached_match_limit(self) -> bool:
        """
        Vérifie si la limite de 8 matchs est atteinte.
        
        Returns:
            bool: True si la limite est atteinte, False sinon
        """
        return MatchManager._match_count >= self.MAX_MATCHES
        
    def update_player(self, excel_path: str, players: list, match_widget):
        """
        Met à jour les joueurs dans le fichier Excel et convertit en PDF.
        
        Args:
            excel_path: Chemin vers le fichier Excel
            players: Liste des joueurs
            match_widget: Widget du match
        """
        # Créer et afficher le StateToolTip
        self.state_tooltip = StateToolTip(
            'Mise à jour en cours', 
            'Veuillez patienter pendant la mise à jour des joueurs...', 
            match_widget
        )
        self.state_tooltip.move(match_widget.width() - 400, 20)
        self.state_tooltip.show()
        
        # Créer le dictionnaire des variables
        variables = {
            'club1_j1': players[0],
            'club1_j2': players[1],
            'club1_j3': players[2],
            'club1_j4': players[3],
            'club2_j1': players[4],
            'club2_j2': players[5],
            'club2_j3': players[6],
            'club2_j4': players[7]
        }
        
        # Mettre à jour les variables dans le fichier Excel
        ExcelToPdfWorker.update_variables(excel_path, variables)

        # Connecter le signal avant de décharger le PDF
        match_widget.editor.pdf_unloaded.connect(
            lambda: self._convert_after_unload(match_widget, excel_path)
        )
        match_widget.editor.unload_pdf()

    def _convert_after_unload(self, match_widget, excel_path):
        """Appelé quand le PDF est vraiment déchargé."""
        self.excel_worker.excel_path = excel_path
        
        # Récupérer le thread de conversion
        thread = self.excel_worker.convert()
        if thread:
            # Fonction de callback qui se déconnecte après utilisation
            def on_finished():
                try:
                    thread.finished.disconnect()
                except TypeError:
                    pass  # Le signal était déjà déconnecté
                match_widget.editor.load_new_pdf(match_widget.pdf_path)
                # Mettre à jour le StateToolTip
                if hasattr(self, 'state_tooltip'):
                    self.state_tooltip.setContent('Les compositions ont été enregistrées 😊')
                    self.state_tooltip.setState(True)
                
            # Connecter le signal avant de démarrer
            thread.finished.connect(on_finished)
            # Démarrer la conversion
            thread.start()