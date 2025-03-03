from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QSizePolicy, 
                             QSpacerItem, QVBoxLayout, QWidget)
from qfluentwidgets import (LineEdit, PasswordLineEdit,
                          PrimaryPushButton, HyperlinkButton)
from widgets.progress import LoginProgressRing
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(1119, 693)
        Form.setMinimumSize(QSize(700, 500))
        
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        
        # Background image
        self.background = QLabel(Form)
        self.background.setObjectName(u"background")
        pixmap = QPixmap(r"c:\Users\CHAUVIN ANTOINE\PycharmProjects\GIRPE2.0\resource\images\news__20250225150811.jpg")
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(False)
        self.horizontalLayout.addWidget(self.background)

        # Login widget container
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(360, 0))
        
        # Login layout
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(40, 60, 40, 60)
        
        # Top spacer
        self.verticalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Logo
        self.logo = QLabel(self.widget)
        self.logo.setObjectName(u"logo")
        self.logo.setPixmap(QPixmap(u":/newPrefix/images/logo.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.logo)
        
        # Spacer after logo
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        # Login form container
        self.form_container = QWidget(self.widget)
        self.form_container.setObjectName(u"form_container")
        self.form_layout = QVBoxLayout(self.form_container)
        self.form_layout.setSpacing(15)
        self.form_layout.setObjectName(u"form_layout")
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Username
        self.username_edit = LineEdit(self.form_container)
        self.username_edit.setObjectName(u"username_edit")
        self.username_edit.setPlaceholderText("Nom d'utilisateur")
        self.username_edit.setMinimumHeight(40)
        self.form_layout.addWidget(self.username_edit)
        
        # Password
        self.password_edit = PasswordLineEdit(self.form_container)
        self.password_edit.setObjectName(u"password_edit")
        self.password_edit.setPlaceholderText("Mot de passe")
        self.password_edit.setMinimumHeight(40)
        self.form_layout.addWidget(self.password_edit)
        
        # Forgot password link
        self.forgot_password = HyperlinkButton(self.form_container)
        self.forgot_password.setObjectName(u"forgot_password")
        self.forgot_password.setText(u"Mot de passe oublié ?")
        forgot_layout = QHBoxLayout()
        forgot_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        forgot_layout.addWidget(self.forgot_password)
        self.form_layout.addLayout(forgot_layout)
        
        # Login button
        self.button_login = PrimaryPushButton(self.form_container)
        self.button_login.setObjectName(u"button_login")
        self.button_login.setMinimumHeight(40)
        self.button_login.setMaximumWidth(200)
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.button_login)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.form_layout.addLayout(button_layout)
        
        self.verticalLayout.addWidget(self.form_container)
        
        # Progress ring
        self.progress_ring = LoginProgressRing(self.widget)
        self.progress_ring.setObjectName(u"progress_ring")
        self.progress_ring.setFixedSize(100, 100)
        self.progress_ring.setTextVisible(True)  
        self.progress_ring.hide()
        progress_layout = QHBoxLayout()
        progress_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        progress_layout.addWidget(self.progress_ring)
        progress_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(progress_layout)
        
        # Bottom spacer
        self.verticalLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.horizontalLayout.addWidget(self.widget)
        
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"GIRPE 2.0", None))
        self.button_login.setText(QCoreApplication.translate("Form", u"Se connecter", None))
        self.forgot_password.setText(QCoreApplication.translate("Form", u"Mot de passe oublié ?", None))
