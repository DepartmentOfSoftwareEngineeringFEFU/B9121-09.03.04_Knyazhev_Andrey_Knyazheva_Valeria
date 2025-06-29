import sys
from PyQt6.QtWidgets import QApplication
from ui.startup_window import StartupWindow

app = QApplication(sys.argv)
window = StartupWindow()
window.show()
sys.exit(app.exec())
