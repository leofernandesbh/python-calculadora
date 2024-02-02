from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QMessageBox

from utils.util import isEmpty, isNumOrDot

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
  
  def keyPressEvent(self, event: QKeyEvent) -> None:
    text = event.text().strip().upper()
    key = event.key()
    
    isEqual = text == '=' or key in [Qt.Key_Return, Qt.Key_Enter] # type: ignore
    isBackspace = key in [Qt.Key_Backspace, Qt.Key_Delete] # type: ignore
    isClear = text == 'C' or key == Qt.Key_Escape # type: ignore
    isNumberOrDot = isNumOrDot(text)
    isOperator = text in '+-*/=E'
    
    if isEqual:
      self.equalSignal.emit()
      return event.ignore()
    
    if isBackspace:
      self.backspaceSignal.emit()
      return event.ignore()
    
    if isClear:
      self.clearSignal.emit()
      return event.ignore()
    
    if isEmpty(text):
      return event.ignore()
    
    if isNumberOrDot:
      self.numberOrDotSignal.emit(text)
      return event.ignore()
    
    if isOperator:
      if text == 'E':
        text = '^'
      self.operatorSignal.emit(text)
      return event.ignore()