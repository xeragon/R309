import sys
from time import sleep
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket

class Worker(QRunnable):
    def __init__(self,client_socket,path,uploads_list : QListWidget):
        super().__init__()
        self.client_socket = client_socket
        self.path = path
        self.uploads_list = uploads_list
        


    @pyqtSlot()
    def run(self):
        
        filename_splited = self.path.split('/')
        filename = filename_splited[len(filename_splited)-1]
        file_extension = filename.split('.')[len(filename.split('.'))-1]
        
        uploadedWidget = QListWidgetItem(f"{filename} uploading...",self.uploads_list)
        uploadedWidget.setBackground(QColor("lightorange")) 
       
        if file_extension not in ["py","txt"]:
            print("FileFormat not supported")
            uploadedWidget.setText(f"{filename} failed : file format not supported")
            uploadedWidget.setBackground(QColor("red")) 
            return
        

        try: 
            fi = open(self.path, "r")
            if not fi:
                print("no fi")
                return
            self.client_socket.send(("post").encode())
            data = fi.read() 
            while data: 
                self.client_socket.send(str(data).encode()) 
                data = fi.read() 
            fi.close() 
            self.client_socket.send(("end").encode())
            answer = self.client_socket.recv(1024).decode()
            # self.upload_label.setText(answer)
            print(f"received from server : {answer}")
            uploadedWidget.setText(f"{filename} uploaded")
            uploadedWidget.setBackground(QColor("lightgreen")) 


                
        except Exception as e:
            print(f"error : {e}")
            uploadedWidget.setText(f"{filename} failed")
            uploadedWidget.setBackground(QColor("lightred")) 
            return
    


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.setWindowTitle("My App")
        self.threadpool = QThreadPool()

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


        upload_layout = QVBoxLayout()
        
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        self.upload_label = QLabel("")
        upload_layout.addWidget(self.upload_btn)
        upload_layout.addWidget(self.upload_label)
            
            
        self.uploads_list = QListWidget()
        
        
        main_layout.addWidget(self.status)
        main_layout.addLayout(inputs_layout)
        main_layout.addLayout(connection_layout)
        main_layout.addLayout(upload_layout)
        main_layout.addWidget(self.uploads_list)


        widget = QWidget()
        widget.setLayout(main_layout)
        self.setFixedSize(QSize(800,600))
        self.setCentralWidget(widget)
    
    def connect_to_main_serv(self):  
        
        if not self.client_socket:
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
            self.upload_btn.setEnabled(True)
            self.connect_btn.setText("Disconnect")
            
        else:
            self.client_socket.send(("close").encode())
            self.client_socket.close()
            self.client_socket = None
            self.upload_btn.setEnabled(False)
            self.status.setText("disconnected")
            self.connect_btn.setText("Connect")
        
        
    def status_text_changed(self):
        if self.status.text() == "connected":
            self.status.setStyleSheet("color: green")
        elif self.status.text() == "connecting":
            self.status.setStyleSheet("color: orange") 
        elif self.status.text() == "disconnected":
            self.status.setStyleSheet("color: red") 
        else:
            self.status.setStyleSheet("color: black") 



    def upload_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        path = fname[0]
        worker = Worker(self.client_socket,path,self.uploads_list)
        if path != "":
            self.threadpool.start(worker)
      
    
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()