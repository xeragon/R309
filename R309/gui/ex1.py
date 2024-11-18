import sys
from time import sleep
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Une première fenetre")

        main_layout = QVBoxLayout()
        

        self.input = QLineEdit("")

        self.ok_btn = QPushButton("ok")
        self.label = QLabel("")
        self.ok_btn.clicked.connect(self.ok_pressed)
        
        self.quit_btn = QPushButton("quitter")
        self.quit_btn.clicked.connect(self.quit_pressed)
        
        self.input.setFixedSize(QSize(280,30))
        self.label.setFixedSize(QSize(280,30))
        self.ok_btn.setFixedSize(QSize(280,30))
        self.quit_btn.setFixedSize(QSize(280,30))

        main_layout.addWidget(self.input)
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.ok_btn)
        main_layout.addWidget(self.quit_btn)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setFixedSize(QSize(300,200))
        self.setCentralWidget(widget)

    
    def ok_pressed(self):
        self.label.setText(f"Bonjour {self.input.text()}")
        
    def quit_pressed(self):
        self.close()
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()