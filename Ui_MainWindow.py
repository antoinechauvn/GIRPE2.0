# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QFrame, QStackedWidget, QHBoxLayout, QLabel, QApplication
from qfluentwidgets import (
    NavigationInterface, NavigationItemPosition, NavigationAvatarWidget,
    MessageBox, FluentIcon as FIF, isDarkTheme
)
from qframelesswindow import FramelessWindow

# Local imports
from pages.welcome import WelcomeWidget
from pages.create_party import PartyWidget
from pages.search_player import SearchPlayerWidget


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Ui_MainWindow(FramelessWindow):

    def __init__(self):
        super().__init__()

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.welcomeInterface = WelcomeWidget(self)
        self.settingInterface = Widget('Setting Interface', self)
        self.clubInterface = Widget('Search Club', self)
        self.playerInterface = SearchPlayerWidget(self)
        self.partyInterface = PartyWidget(self)
        print("test")
        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.welcomeInterface, FIF.HOME, 'Bienvenue')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.partyInterface, FIF.ADD, 'Create Party')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.clubInterface, FIF.SEARCH, 'Search Club')
        self.addSubInterface(self.playerInterface, FIF.PEOPLE, 'Search Player')

        self.navigationInterface.addSeparator()

        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('zhiyiYo', 'resource/shoko.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(0)
        self.navigationInterface.setCurrentItem('Bienvenue')

    def initWindow(self):
        self.resize(1119, 693)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, parent=None):
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            '支持作者',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水。您的支持就是作者开发和维护项目的动力',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))
