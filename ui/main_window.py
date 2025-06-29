from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.cad_loader import load_dxf
from models.visualization import create_3d_figure, plot_dxf_lines, plot_workers
from core.positioning import calculate_positions
import json
import random
from pathlib import Path


class WiFiSimulatorThread(QThread):
    data_generated = pyqtSignal(dict)

    def __init__(self, aps, workers, interval=0.5):
        super().__init__()
        self.aps = aps
        self.workers = workers
        self.interval = interval
        self._is_running = False

    def run(self):
        self._is_running = True
        while self._is_running:
            data = {
                worker: {ap: random.randint(-90, -50) for ap in self.aps}
                for worker in self.workers
            }
            self.data_generated.emit(data)
            self.msleep(int(self.interval * 1000))

    def stop(self):
        self._is_running = False
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self, filepath):
        super().__init__()
        self.setWindowTitle("Система позиционирования")
        self.resize(1200, 600)
        self.filepath = filepath
        self.worker_positions = {}

        self.init_ui()

        self.load_model()

        self.simulator_thread = WiFiSimulatorThread(
            aps=["ap1", "ap2", "ap3"],
            workers=["w1", "w2", "w3"],
            interval=0.5
        )
        self.simulator_thread.data_generated.connect(self.handle_new_data)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_positions)
        self.update_timer.setInterval(500)

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.model_3d_frame = QFrame()
        self.model_3d_frame.setStyleSheet("background: #252525;")
        main_layout.addWidget(self.model_3d_frame, stretch=4)

        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel, stretch=1)

        self.workers_list = QListWidget()
        self.workers_list.setStyleSheet("""
            QListWidget {

                font-size: 14px;
                border: 1px solid #454545;
            }
        """)
        right_layout.addWidget(self.workers_list)

        self.btn_control = QPushButton("Старт")
        self.btn_control.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 12px;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        self.btn_control.clicked.connect(self.toggle_positioning)
        right_layout.addWidget(self.btn_control)

    def load_model(self):
        lines = load_dxf(self.filepath)
        if not lines:
            return

        self.fig, self.ax = create_3d_figure()
        plot_dxf_lines(self.ax, lines)

        self.canvas = FigureCanvas(self.fig)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.model_3d_frame.setLayout(layout)

    def toggle_positioning(self):
        if self.btn_control.text() == "Старт":
            self.start_positioning()
        else:
            self.pause_positioning()

    def start_positioning(self):
        self.btn_control.setText("Пауза")
        self.btn_control.setStyleSheet("""
            QPushButton {
                background: #de9b0b;
                color: white;
                font-weight: bold;
                padding: 12px;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #b57d07;
            }
        """)
        self.simulator_thread.start()
        self.update_timer.start()

        self.worker_positions.clear()
        self.workers_list.clear()

    def pause_positioning(self):
        self.btn_control.setText("Старт")
        self.btn_control.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 12px;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        self.simulator_thread.stop()
        self.update_timer.stop()

    def handle_new_data(self, data):
        try:
            Path("data").mkdir(exist_ok=True)
            with open("data/simulated_data.json", 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def update_positions(self):
        try:
            with open("data/simulated_data.json", 'r') as f:
                wifi_data = json.load(f)
            self.worker_positions = calculate_positions(wifi_data)

            self.ax.clear()
            plot_dxf_lines(self.ax, load_dxf(self.filepath))
            plot_workers(self.ax, self.worker_positions)
            self.canvas.draw()

            self.workers_list.clear()
            for worker_id, pos in self.worker_positions.items():
                item = QListWidgetItem(f"{worker_id}: ({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f})")
                self.workers_list.addItem(item)

        except Exception as e:
            print(f"Ошибка обновления позиций: {e}")

    def closeEvent(self, event):
        self.simulator_thread.stop()
        self.update_timer.stop()
        event.accept()
