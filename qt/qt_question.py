#!/usr/bin/env python

import sys
from typing import List

from PyQt6.QtCore import QRect, Qt
from PyQt6.QtWidgets import QApplication, QMessageBox, QStyle, QWidget



class QTApp (QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)

        main_window = Window ()        

        answer = QMessageBox.question (
            main_window,
            "Question",
            argv[1],
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if (answer == QMessageBox.StandardButton.Yes):
            self.exit (0)
        else:
            self.exit (1)


class Window (QWidget):
    def __init__(self, parent: QWidget = None, 
                 flags: Qt.WindowType = Qt.WindowType.Window) -> None:
        
        super().__init__(parent, flags)


DEBUGGING = True


if __name__ == "__main__":
    if (DEBUGGING):
        app = QTApp (["DUMMY", "Are you ok?"])
    else:
        app = QTApp (sys.argv)

    sys.exit(app.exec())