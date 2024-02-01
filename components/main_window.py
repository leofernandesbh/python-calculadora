from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QMessageBox

class MainWindow(QMainWindow):
  def __init__(self, parent: QWidget | None = None, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    
    self.setWindowTitle("LFSoftwares® - Calculadora")        
    
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