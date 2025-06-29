import random
from PyQt6.QtCore import QThread, pyqtSignal


class WiFiSimulatorThread(QThread):
    data_generated = pyqtSignal(dict)

    def __init__(self, aps, workers, interval=0.5):
        super().__init__()
        self.aps = aps
        self.workers = workers
        self.interval = interval
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            data = {
                worker: {ap: random.randint(-90, -50) for ap in self.aps}
                for worker in self.workers
            }
            self.data_generated.emit(data)
            QThread.msleep(int(self.interval * 1000))

    def stop(self):
        self.running = False
        self.wait()
