from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QMessageBox

class MainWindow(QMainWindow):
  equalSignal = Signal() 
  backspaceSignal = Signal()
  clearSignal = Signal()
  numberOrDotSignal = Signal(str)
  operatorSignal = Signal(str)
  
  def __init__(self, parent: QWidget | None = None, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    
    self.setWindowTitle("LFSoftwares® - Calculadora")            
    
    self.menu_bar = self.menuBar()
    self.file_menu = self.menu_bar.addMenu("Calculadora")
    # self.file_menu.showMaximized()
    
    self.exit_action = self.file_menu.addAction("Sair")
    self.exit_action.triggered.connect(self.close)
    
    self.vLayout = QVBoxLayout()
    self.widget = QWidget()
    self.widget.setLayout(self.vLayout)    
    self.setCentralWidget(self.widget)
    
  def adjustFixedSize(self):
    self.adjustSize()
    self.setFixedSize(self.size())   
    
  def addWidgetToMainLayout(self, widget: QWidget):
    self.vLayout.addWidget(widget)
    
  def addLayoutToMainLayout(self, layout: QVBoxLayout | QGridLayout):
    self.vLayout.addLayout(layout)
    
  def messageBox(self):
    return QMessageBox(self)