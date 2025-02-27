from PySide6.QtCore import QTimer, Signal
from qfluentwidgets import ProgressRing


class LoginProgressRing(ProgressRing):
    """ProgressRing personnalisé pour la connexion avec timer intégré."""
    progress_complete = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStrokeWidth(4)
        
        # Timer pour la progression
        self._timer = QTimer()
        self._timer.timeout.connect(self._update)
        
    def start(self, interval=50):
        """Démarre la progression."""
        self.setValue(0)
        self._timer.start(interval)
        
    def stop(self):
        """Arrête la progression."""
        self._timer.stop()
        
    def _update(self):
        """Met à jour la valeur de progression."""
        new_value = self.getVal() + 4
        self.setValue(new_value)
        
        if new_value >= 100:
            self._timer.stop()
            self.progress_complete.emit()
