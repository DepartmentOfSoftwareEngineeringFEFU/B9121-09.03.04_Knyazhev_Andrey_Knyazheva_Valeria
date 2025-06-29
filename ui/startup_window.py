from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
)


class StartupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система позиционирования")
        self.setFixedSize(300, 200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.btn_load = QPushButton("Загрузить чертеж")
        self.btn_load.setMinimumHeight(30)
        self.btn_load.clicked.connect(self.load_drawing)

        layout.addStretch()
        layout.addWidget(self.btn_load)
        layout.addStretch()

        self.setLayout(layout)

    def load_drawing(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл чертежа",
            "",
            "DXF Files (*.dxf);;All Files (*)"
        )

        if filepath:
            from ui.main_window import MainWindow
            self.main_window = MainWindow(filepath)
            self.main_window.show()
            self.close()
