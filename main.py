import sys
import cv2
from pyzbar.pyzbar import decode
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QTextEdit

class QRCodeScanner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QR Code Scanner")
        self.setGeometry(100, 100, 960, 480)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tab_widget = QTabWidget(self)
        self.layout.addWidget(self.tab_widget)

        self.video_tab = QWidget()
        self.result_tab = QWidget()

        self.tab_widget.addTab(self.video_tab, "Video")
        self.tab_widget.addTab(self.result_tab, "Data")

        self.video_layout = QVBoxLayout(self.video_tab)
        self.result_layout = QVBoxLayout(self.result_tab)

        self.video_label = QLabel(self.video_tab)
        self.video_layout.addWidget(self.video_label)

        self.result_text_edit = QTextEdit(self.result_tab)
        self.result_layout.addWidget(self.result_text_edit)

        self.video_capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.found_qrcodes = set()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            barcodes = decode(frame)
            for barcode in barcodes:
                data = barcode.data.decode('utf-8')
                if data not in self.found_qrcodes:
                    self.found_qrcodes.add(data)
                    print("Data Terinput:", data)
                    self.result_text_edit.append("Data Terinput: " + data)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(q_image))

def main():
    app = QApplication(sys.argv)
    window = QRCodeScanner()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
