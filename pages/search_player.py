from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt
from qfluentwidgets import (LineEdit, PrimaryPushButton, CardWidget, 
                          SubtitleLabel, BodyLabel, FlowLayout,
                          StrongBodyLabel, HorizontalSeparator)

from utils.fftt_api import FFTTApi

class InfoCard(CardWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = SubtitleLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.title)
        self.vBoxLayout.addWidget(HorizontalSeparator())
        
    def add_info_row(self, label, value):
        row = QHBoxLayout()
        label_widget = StrongBodyLabel(label, self)
        value_widget = BodyLabel(str(value), self)
        row.addWidget(label_widget)
        row.addWidget(value_widget)
        row.addStretch(1)
        self.vBoxLayout.addLayout(row)

class SearchPlayerWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SearchPlayer")
        self.initUI()

    def initUI(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Layout horizontal pour la recherche
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        # LineEdit pour le numéro de licence
        self.license_edit = LineEdit(self)
        self.license_edit.setPlaceholderText("Numéro de licence")
        self.license_edit.setFixedWidth(200)
        search_layout.addWidget(self.license_edit)

        # Bouton de recherche
        self.search_button = PrimaryPushButton("Rechercher", self)
        self.search_button.clicked.connect(self.search_player)
        search_layout.addWidget(self.search_button)
        search_layout.addStretch(1)

        # Ajouter le layout de recherche au layout principal
        main_layout.addLayout(search_layout)

        # Zone de scroll pour les résultats
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        main_layout.addWidget(scroll)

        # Widget contenant les résultats
        self.result_widget = QWidget()
        self.result_layout = FlowLayout(self.result_widget)
        self.result_layout.setSpacing(20)
        self.result_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(self.result_widget)

    def display_player_data(self, data):
        # Nettoyer les résultats précédents
        for i in reversed(range(self.result_layout.count())): 
            self.result_layout.itemAt(i).widget().deleteLater()

        # Carte Identité
        identity_card = InfoCard("Identité")
        identity_card.add_info_row("Nom", data['nom'])
        identity_card.add_info_row("Prénom", data['prenom'])
        identity_card.add_info_row("Licence", data['licence'])
        identity_card.add_info_row("Sexe", 'Homme' if data['sexe'] == 'M' else 'Femme')
        self.result_layout.addWidget(identity_card)

        # Carte Club
        club_card = InfoCard("Club")
        club_card.add_info_row("Nom", data['nomclub'])
        club_card.add_info_row("Numéro", data['numclub'])
        self.result_layout.addWidget(club_card)

        # Carte Classement
        ranking_card = InfoCard("Classement")
        ranking_card.add_info_row("Points", data['point'])
        ranking_card.add_info_row("Points mensuels", data['pointm'])
        ranking_card.add_info_row("Points virtuels", data['virtual'])
        self.result_layout.addWidget(ranking_card)

        # Carte Statistiques
        stats_card = InfoCard("Statistiques de la saison")
        stats_card.add_info_row("Victoires", data['victoires'])
        stats_card.add_info_row("Défaites", data['defaites'])
        stats_card.add_info_row("Performances", data['perfs'])
        stats_card.add_info_row("Contre-performances", data['contres'])
        self.result_layout.addWidget(stats_card)

        # Carte Positions
        positions_card = InfoCard("Classements")
        positions_card.add_info_row("National", data['rangnat'])
        positions_card.add_info_row("Régional", data['rangreg'])
        positions_card.add_info_row("Départemental", data['rangdep'])
        positions_card.add_info_row("Club", data['rangclub'])
        self.result_layout.addWidget(positions_card)

        # Carte Détails techniques
        details_card = InfoCard("Détails techniques")
        details_card.add_info_row("Points mensuels initiaux", data['initm'])
        details_card.add_info_row("Points mensuels précédents", data['ppointm'])
        details_card.add_info_row("Points annuels", data['apointm'])
        details_card.add_info_row("Points annuels précédents", data['papointm'])
        details_card.add_info_row("Qualité des adversaires", data['opponents_quality'])
        self.result_layout.addWidget(details_card)

    def search_player(self):
        license_number = self.license_edit.text().strip()
        if not license_number:
            print("Erreur: Veuillez entrer un numéro de licence")
            return

        # Appel à l'API FFTT
        result = FFTTApi.get_player(license_number)
        
        if "error" in result:
            print(f"Erreur lors de la recherche : {result['error']}")
            return

        # Afficher la réponse brute dans la console
        print("\nRéponse brute de l'API:")
        print("=" * 50)
        print(result)
        print("=" * 50 + "\n")

        # Afficher le résultat avec les widgets
        self.display_player_data(result)
