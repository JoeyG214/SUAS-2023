from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget
from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2

picam2a = Picamera2(0)
picam2b = Picamera2(1)

picam2a.configure(picam2a.create_preview_configuration())
picam2b.configure(picam2b.create_preview_configuration())

image_numA = 0
image_numB = 0

current_cam = 'A'

def on_button_clicked():
  global image_numA, image_numB, current_cam
  button_capture.setEnabled(False)
  if current_cam == 'A':
      cfg = picam2a.create_still_configuration()
      picam2a.switch_mode_and_capture_file(cfg, f'./images/imageA{image_numA}.jpg', signal_function=qpicamera2.signal_done)
      image_numA += 1
  else:
      cfg = picam2b.create_still_configuration()
      picam2b.switch_mode_and_capture_file(cfg, f'./images/imageB{image_numB}.jpg', signal_function=qpicamera2.signal_done)
      image_numB += 1

def capture_done(job):
  result = picam2a.wait(job) if current_cam == 'A' else picam2b.wait(job)
  button_capture.setEnabled(True)

def switch_camera():
  global current_cam, qpicamera2
  current_cam = 'B' if current_cam == 'A' else 'A'
  qpicamera2.set_camera(picam2a if current_cam == 'A' else picam2b)

app = QApplication([])
qpicamera2 = QGlPicamera2(picam2a, width=800, height=600, keep_ar=False)  # Start with camera A
button_capture = QPushButton("Click to capture JPEG")
button_switch = QPushButton("Switch camera")
window = QWidget()
qpicamera2.done_signal.connect(capture_done)
button_capture.clicked.connect(on_button_clicked)
button_switch.clicked.connect(switch_camera)
layout_v = QVBoxLayout()
layout_v.addWidget(qpicamera2)
layout_v.addWidget(button_capture)
layout_v.addWidget(button_switch)
window.setWindowTitle("PiCamera 2 Capture")
window.resize(640, 480)
window.setLayout(layout_v)
picam2a.start()
picam2b.start()
window.show()
app.exec()