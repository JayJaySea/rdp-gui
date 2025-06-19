from PySide6 import QtGui
from PySide6.QtCore import QSize, Qt, QPoint, Signal, QEvent, QTimer
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QPushButton, QStyleOption, QStyle, QFrame, QLabel, QHBoxLayout
import os

class LabelButton(QFrame):
    clicked = Signal(str)

    def __init__(self, label, color, font_size=None, parent=None):
        super().__init__(parent)
        self.setObjectName("LabelButton")
        self.label = label
        self.hovering = False
        self.active = False
        self.color = color

        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setProperty("color", color)

        self.indicator = QLabel(label, self)
        self.indicator.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.indicator.setAlignment(Qt.AlignCenter)
        self.indicator.setObjectName("LabelButtonIndicator")
        self.indicator.setProperty(font_size, True)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.indicator)

        self.setLayout(layout)

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.hoverStyle()

    def mouseMoveEvent(self, event):
        mouse_pos = event.globalPosition().toPoint()
        button_rect = self.rect().translated(self.mapToGlobal(QPoint(0, 0)))

        if button_rect.contains(mouse_pos):
            if not self.hovering:
                self.hovering = True
        else:
            if self.hovering:
                self.hovering = False

        if not self.hovering:
            self.unsetCursor()
            self.defaultStyle()
        elif self.active:
            self.activeStyle()

    def leaveEvent(self, event):
        self.defaultStyle()

    def mousePressEvent(self, event):
        self.active = True
        self.activeStyle()

    def mouseReleaseEvent(self, event):
        self.active = False
        self.defaultStyle()
        if self.hovering:
            self.clicked.emit(self.label)

    def defaultStyle(self):
        self.indicator.setProperty("hover", False)
        self.indicator.setProperty("color", False)
        self.refreshStyle()

    def hoverStyle(self):
        self.indicator.setProperty("hover", True)
        self.refreshStyle()

    def activeStyle(self):
        self.indicator.setProperty("color", self.color)
        self.refreshStyle()

    def refreshStyle(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        self.indicator.style().unpolish(self.indicator)
        self.indicator.style().polish(self.indicator)
        self.indicator.update()

    def setLabel(self, label):
        self.indicator.setText(label)

class CheckableLabelButton(LabelButton):
    clicked = Signal(str)

    def __init__(self, active_label, inactive_label, color, active, parent=None):
        label = active_label if active else inactive_label
        super().__init__(label, color, "medium", parent)

        self.focused = False
        self.focused_color = "yellow"
        self.active = active
        self.active_label = active_label
        self.inactive_label = inactive_label
        self.indicator.setObjectName("CheckableButtonIndicator")

        self.updateStyle()

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        self.hoverStyle()

    def mouseMoveEvent(self, event):
        pass

    def leaveEvent(self, event):
        if not self.active:
            self.defaultStyle()

    def mousePressEvent(self, event):
        self.toggleActive()
        self.clicked.emit(self.active)

    def focusInEvent(self, event):
        self.focused = True
        self.focusedStyle()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.focused = False
        self.unfocusedStyle()
        super().focusOutEvent(event)

    def updateStyle(self):
        if self.active:
            self.setLabel(self.active_label)
            self.activeStyle()
        else:
            self.setLabel(self.inactive_label)
            self.defaultStyle()

    def mouseReleaseEvent(self, event):
        pass

    def toggleActive(self):
        self.active = not self.active
        self.updateStyle()

    def setInactive(self):
        self.active = False
        self.defaultStyle()

    def setActive(self):
        self.active = True
        self.activeStyle()

    def focusedStyle(self):
        self.setProperty("color", self.focused_color)
        if self.active:
            self.indicator.setProperty("color", self.focused_color)
        self.refreshStyle()

    def unfocusedStyle(self):
        self.setProperty("color", self.color)
        if self.active:
            self.indicator.setProperty("color", self.color)
        self.refreshStyle()

    def activeStyle(self):
        if self.focused:
            self.indicator.setProperty("color", self.focused_color)
        else:
            self.indicator.setProperty("color", self.color)
        self.refreshStyle()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.toggleActive()
        else:
            super().keyPressEvent(event)  # Don't block other keys
