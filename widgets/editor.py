# Third-party imports
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument
from qfluentwidgets import (
    CommandBar, Action, FluentIcon as FIF, 
    SmoothScrollDelegate
)


class CustomPdfView(QPdfView):
    """Vue PDF personnalisée avec zoom via souris et boutons."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.min_zoom = 0.3  # 30%
        self.max_zoom = 5.0  # 500%
        self.setPageMode(QPdfView.PageMode.SinglePage)
        self.setZoomMode(QPdfView.ZoomMode.Custom)

        # Désactiver la bordure
        self.setFrameShape(QFrame.NoFrame)  

    def _clamp_zoom(self, factor):
        """Limite le facteur de zoom entre min_zoom et max_zoom."""
        return max(self.min_zoom, min(self.max_zoom, factor))

    def setZoomFactor(self, factor):
        super().setZoomFactor(self._clamp_zoom(factor))

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)

    def zoom_in(self):
        current_zoom = self.zoomFactor()
        new_zoom = self._clamp_zoom(current_zoom * 1.25)
        self.setZoomFactor(new_zoom)

    def zoom_out(self):
        current_zoom = self.zoomFactor()
        new_zoom = self._clamp_zoom(current_zoom * 0.8)
        self.setZoomFactor(new_zoom)

    def reset_zoom(self):
        self.setZoomFactor(1.0)


class EditorWidget(QFrame):
    pdf_unloaded = Signal()
    
    def __init__(self, pdf_path: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("EditorWidget")
        self.pdf_path = pdf_path

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.commandBar = EditorCommandBar(self)
        self.layout.addWidget(self.commandBar)

        self.container = QWidget(self)
        self.container.setLayout(QVBoxLayout())
        self.container.layout().setContentsMargins(0, 0, 0, 0)
        
        # Initialisation du PDF viewer
        self.pdfView = CustomPdfView(self.container)
        self.pdfDocument = QPdfDocument(self)
        
        self.pdfDocument.load(self.pdf_path)
        self.pdfView.setDocument(self.pdfDocument)
        
        self.container.layout().addWidget(self.pdfView)
        self.layout.addWidget(self.container)
        
        # Créer le ScrollDelegate après avoir ajouté la vue
        self.scrollDelegate = SmoothScrollDelegate(self.pdfView)
        self.scrollDelegate.useAni = True

        # Connecter les actions de zoom
        self.commandBar.zoomInAction.triggered.connect(self.pdfView.zoom_in)
        self.commandBar.zoomOutAction.triggered.connect(self.pdfView.zoom_out)
        self.commandBar.resetZoomAction.triggered.connect(self.pdfView.reset_zoom)

    def unload_pdf(self):
        """Ferme le PDF actuel et nettoie les références."""
        self.pdfView.setDocument(None)
        
        # Fermer et supprimer l'ancien document
        if self.pdfDocument:
            old_document = self.pdfDocument
            # Créer un nouveau document vide avant de détruire l'ancien
            self.pdfDocument = QPdfDocument(self)
            # Connecter le signal destroyed à l'émission de notre signal
            old_document.destroyed.connect(self.pdf_unloaded.emit)
            old_document.close()
            old_document.deleteLater()
            
    def load_new_pdf(self, pdf_path):
        """Charge un nouveau fichier PDF."""
        # Charger le nouveau PDF
        self.pdfDocument.load(pdf_path)
        self.pdfView.setDocument(self.pdfDocument)
        
        print(f"Nouveau PDF chargé: {pdf_path}")
        
        return True


class EditorCommandBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initBar()

    def initBar(self):
        self.commandBar = CommandBar(self)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.commandBar)

        self.zoomInAction = self.addButton(FIF.ZOOM_IN, 'Zoom in')
        self.zoomOutAction = self.addButton(FIF.ZOOM_OUT, 'Zoom out')
        self.resetZoomAction = self.addButton(FIF.RETURN, 'Reset zoom')

    def addButton(self, icon, text, slot=None):
        action = Action(icon, text)
        if slot:
            action.triggered.connect(slot)
        self.commandBar.addAction(action)
        return action