import sys
from time import sleep
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket



class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aide")
        layout = QVBoxLayout()
        message = QLabel("Permet de convertire une température")
        layout.addWidget(message)
        self.setLayout(layout)
        
class BadInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aide")
        layout = QVBoxLayout()
        message = QLabel("La température entrée doit être un nombre")
        layout.addWidget(message)
        self.setLayout(layout)
        
class ZeroAbsoluDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aide")
        layout = QVBoxLayout()
        message = QLabel("La température entrée doit êtres supérieur à -273,15 °C ou 0K")
        layout.addWidget(message)
        self.setLayout(layout)





class MainWindow(QMainWindow):
    def __init__(self):
    
        super().__init__()
        self.setWindowTitle("Conversion de température")

        main_layout = QVBoxLayout()


        self.temperature_label = QLabel("Température")
        self.temperature_input = QLineEdit("")
        self.temp_system_in = QLabel("°C")
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.temperature_label)
        input_layout.addWidget(self.temperature_input)
        input_layout.addWidget(self.temp_system_in)

        main_layout.addLayout(input_layout)

    
        self.convert_btn = QPushButton("Convertir")
        self.convert_btn.clicked.connect(self.convert_pressed)
        
        self.select_conversion_direction = QComboBox()
        self.select_conversion_direction.addItems(["°C -> K","K -> °C"])
        self.select_conversion_direction.currentIndexChanged.connect(self.convert_direction_changed)

        convert_layout = QHBoxLayout()
        convert_layout.addWidget(self.convert_btn)
        convert_layout.addWidget(self.select_conversion_direction)

        main_layout.addLayout(convert_layout)



        self.conversion_label = QLabel("Température")
        self.conversion_result = QLineEdit("")
        self.conversion_result.setEnabled(False)
        self.temp_system_out = QLabel("K")
        
        temperature_layout = QHBoxLayout()
        temperature_layout.addWidget(self.conversion_label)
        temperature_layout.addWidget(self.conversion_result)
        temperature_layout.addWidget(self.temp_system_out)
        main_layout.addLayout(temperature_layout)
        
        self.help_btn = QPushButton("?")
        self.help_btn.clicked.connect(self.help_clicked)
        
        self.help_btn.setFixedSize(QSize(20,20))
        
        
        main_layout.addWidget(self.help_btn)



        widget = QWidget()
        widget.setLayout(main_layout)
        self.setFixedSize(QSize(600,400))
        self.setCentralWidget(widget)

    
    def convert_pressed(self):
        conversion_direction = self.select_conversion_direction.currentIndex()
        temp = 0
        try:
            temp = int(self.temperature_input.text())
        except:
            dlg = BadInputDialog()
            dlg.exec()
            return

        match conversion_direction:
            case 0:
                if(temp < -273.15):
                    dlg = ZeroAbsoluDialog()
                    dlg.exec()
                else:
                  self.conversion_result.setText(f"{temp+273.15}")
            case 1:
                if(temp < 0):
                    dlg = ZeroAbsoluDialog()
                    dlg.exec()
                else:
                  self.conversion_result.setText(f"{temp-273.15}")    
    
    def convert_direction_changed(self,i):
        match i:
            case 0:
                self.temp_system_in.setText("°C")
                self.temp_system_out.setText("K")
            case 1:
                self.temp_system_in.setText("K")
                self.temp_system_out.setText("°C")
                
                
    def help_clicked(self):
        dlg = HelpDialog()
        dlg.exec()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()