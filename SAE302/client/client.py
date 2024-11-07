import sys
from time import sleep
from PyQt5.QtCore import QSize, Qt

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton,QLineEdit,QLabel,QHBoxLayout,QVBoxLayout ; 
import socket

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        

        main_layout = QVBoxLayout()
        

        self.status = QLineEdit("disconnected")
        self.status.setEnabled(False)
        self.status.setFixedSize(QSize(80,20))
        self.status.setStyleSheet("color: red") 
        self.status.textChanged.connect(self.status_text_changed)
        
        inputs_layout = QHBoxLayout()
    
        host_inputs_layout = QHBoxLayout()
        ports_inputs_layout = QHBoxLayout()
        
        host_lbl = QLabel("Host : ")
        self.host_input = QLineEdit("localhost")
        
        port_lbl = QLabel("Port : ")
        self.port_input = QLineEdit("8080")

        host_inputs_layout.addWidget(host_lbl)
        host_inputs_layout.addWidget(self.host_input)
        ports_inputs_layout.addWidget(port_lbl)
        ports_inputs_layout.addWidget(self.port_input)

        inputs_layout.addLayout(host_inputs_layout)
        inputs_layout.addLayout(ports_inputs_layout)
        
        
        connection_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("Connect to server")
        self.connect_btn.setFixedSize(QSize(100,30))
        self.connect_btn.clicked.connect(self.connect_to_main_serv)

        self.connect_label = QLabel("")
        connection_layout.addWidget(self.connect_btn)
        connection_layout.addWidget(self.connect_label)
        
        main_layout.addWidget(self.status)
        main_layout.addLayout(inputs_layout)
        main_layout.addLayout(connection_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setFixedSize(QSize(800,600))
        self.setCentralWidget(widget)
    
    def connect_to_main_serv(self):  
        
        print(f"values {self.host_input.text(),self.port_input.text()}")
        
        self.connect_btn.setEnabled(False)
        self.connect_btn.setText("Connecting...")
        self.status.setText("connecting")

        try:
            self.client_socket = socket.socket()
            self.client_socket.connect((self.host_input.text(),int(self.port_input.text())))
            self.connect_label.setText(f"successfuly connected")
            self.status.setText("connected")
        except Exception as e:
            errmsg = f'an error occured while trying to connect to server : {e}'
            self.connect_label.setText(errmsg)
            print(errmsg)
        
        self.connect_btn.setEnabled(True)
        self.connect_btn.setText("Connect to server")
        
        
        
    def status_text_changed(self):
        if self.status.text() == "connected":
            self.status.setStyleSheet("color: green")
        elif self.status.text() == "connecting":
            self.status.setStyleSheet("color: orange") 
        elif self.status.text() == "disconnected":
            self.status.setStyleSheet("color: red") 
        else:
            self.status.setStyleSheet("color: black") 

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

