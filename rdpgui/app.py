from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QRect
from PySide6.QtGui import QFontDatabase
from sys import argv
from rdpgui.window import Window
import rdpgui.data as data
from rdpgui.data import DATA_DIR
import os


def main():
    data.init()
    app = QApplication(argv)

    with open(os.path.join(DATA_DIR, "style.css")) as style:
        app.setStyleSheet(style.read())

    font_path = os.path.join(DATA_DIR, "fonts", "RobotoMono-Regular.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    window = Window(QRect(0, 0, 2550, 30))
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
