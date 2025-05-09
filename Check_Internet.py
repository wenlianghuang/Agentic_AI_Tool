import sys
from speedtest import Speedtest  # 確保使用的是 speedtest-cli 提供的 Speedtest 類別
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QThread, Signal
import os

# 確保 sys.stdout 和 sys.stderr 不為 None
if not sys.stdout:
    sys.stdout = open(os.devnull, 'w')
if not sys.stderr:
    sys.stderr = open(os.devnull, 'w')

class SpeedTestThread(QThread):
    # 定義訊號，用於傳遞測試結果
    result_ready = Signal(float, float, float)

    def run(self):
        try:
            st = Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Mbps
            upload_speed = st.upload() / 1_000_000  # Mbps
            ping = st.results.ping
            self.result_ready.emit(download_speed, upload_speed, ping)
        except Exception as e:
            print(f"Error during speed test: {e}")
            self.result_ready.emit(0.0, 0.0, 0.0)

class NetworkTester(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("網路速度測試工具")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("測試中，請稍候...", self)
        layout.addWidget(self.label)

        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        # 啟動網速測試執行緒
        self.start_speed_test()

    def start_speed_test(self):
        self.thread = SpeedTestThread()
        self.thread.result_ready.connect(self.display_results)
        self.thread.start()

    def display_results(self, download_speed, upload_speed, ping):
        self.result_label.setText(f"下載速度: {download_speed:.2f} Mbps\n上傳速度: {upload_speed:.2f} Mbps\n延遲: {ping} ms")
        self.label.setText("測試完成！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkTester()
    window.show()
    sys.exit(app.exec())