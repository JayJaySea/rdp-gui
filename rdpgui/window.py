from PySide6.QtCore import  QSize, Qt, QTime, QObject, QEvent, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
    QApplication
)
from rdpgui.widgets.button import CheckableLabelButton
import rdpgui.controller as controller

class Window(QMainWindow):
    def __init__(self, geometry):
        super().__init__()
        self.memory = controller.getMemory()

        self.setObjectName("Window")
        self.setGeometry(geometry)
        self.initCentralWidget()

        self.navigator = ArrowKeyNavigator()
        self.executor = Executor()
        self.executor.execute.connect(self.connectViaRDP)
        for child in self.findChildren(QWidget):
            child.installEventFilter(self.navigator)
            child.installEventFilter(self.executor)

    def initCentralWidget(self):
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addLayout(self.initIpInput())
        layout.addLayout(self.initUsernameInput())
        layout.addLayout(self.initPasswordInput())
        use_proxychains = True if self.memory.get("use_proxychains") else False
        self.use_proxychains = CheckableLabelButton("On", "Off", "white", use_proxychains)
        self.use_proxychains.setFixedWidth(200)
        self.use_proxychains.setFocusPolicy(Qt.StrongFocus)
        layout.addWidget(QLabel("Use ProxyChains", alignment=Qt.AlignCenter))
        layout.addWidget(self.use_proxychains, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.central = QWidget()
        self.central.setLayout(layout)
        self.setCentralWidget(self.central)

    def initIpInput(self):
        layout = QVBoxLayout()
        label = QLabel("IP address", alignment=Qt.AlignCenter)
        self.ip_input = SelectAllLineEdit()
        self.ip_input.setMaximumWidth(200)
        self.ip_input.setText(self.memory.get("ip_address"))
        layout.addWidget(label)
        layout.addWidget(self.ip_input, alignment=Qt.AlignCenter)
        return layout

    def initUsernameInput(self):
        layout = QVBoxLayout()
        label = QLabel("Username", alignment=Qt.AlignCenter)
        self.username_input = SelectAllLineEdit()
        self.username_input.setMaximumWidth(200)
        self.username_input.setText(self.memory.get("username"))
        layout.addWidget(label)
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        return layout

    def initPasswordInput(self):
        layout = QVBoxLayout()
        label = QLabel("Password", alignment=Qt.AlignCenter)
        self.password_input = SelectAllLineEdit()
        self.password_input.setMaximumWidth(200)
        self.password_input.setText(self.memory.get("password"))
        layout.addWidget(label)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        return layout

    def connectViaRDP(self):
        ip_address = self.ip_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        use_proxychains = self.use_proxychains.active
        controller.connectViaRDP(ip_address, username, password, use_proxychains)
        controller.writeMemory(ip_address, username, password, use_proxychains)
        QApplication.quit()

class ArrowKeyNavigator(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Up:
                obj.focusPreviousChild()
                return True
            elif event.key() == Qt.Key_Down:
                obj.focusNextChild()
                return True
        return super().eventFilter(obj, event)

class Executor(QObject):
    execute = Signal()
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.execute.emit()
                return True
        return super().eventFilter(obj, event)

class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.selectAll()
