import math
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout
from PySide6.QtCore import Slot
from consts.consts import MEDIUM_FONT_SIZE
from utils.util import formatNumber, isNumOrDot, isEmpty, isValidNumber

from typing import TYPE_CHECKING

# Desta forma, evita erro de circular import (neste caso não era necessário, 
# somente para lembrar)
if TYPE_CHECKING:  
  from components.main_window import MainWindow
  from components.display import Display
  from components.account_info import AccountInfo

class Button(QPushButton):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configStyle()
    
  def configStyle(self):
    # self.setStyleSheet(f"font-size: {MEDIUM_FONT_SIZE}px;")
    font = self.font()
    font.setPixelSize(MEDIUM_FONT_SIZE)
    self.setFont(font)
    self.setMinimumSize(60, 60)   
    
class ButtonsGrid(QGridLayout):
  def __init__(self, display: 'Display', info: 'AccountInfo', window: 'MainWindow',  *args, **kwargs):
    super().__init__(*args, **kwargs)    
    self._gridMask = [
        ['C', '◀', '^', '/'],
        ['7', '8', '9', 'x'],
        ['4', '5', '6', '-'],
        ['1', '2', '3', '+'],
        ['',  '0', '.', '='],
    ]
    self.window = window
    # self.window.keyPressEvent = self.keyPressEvent
    self._display = display
    # self._display.clear = self.clearDisplay
    self._info = info
    self._equation = ''
    self._emptyEquationText = 'Sua conta'
    self._left = None
    self._right = None
    self._operator = None    
    self.display.clear()
    self.equation = self._emptyEquationText
    self._makeGrid()
    
  @property
  def display(self):
    return self._display
  
  @display.setter
  def display(self, value):
    self._display = value
    
  @property
  def equation(self):
    return self._equation
    
  @equation.setter
  def equation(self, value):
    self._equation = value
    self._info.setText(value)
    
  def addWidgetToGrid(self, widget: QWidget, row: int = 0, column: int = 0, rowSpan: int = 1, columnSpan: int = 1):
    self.addWidget(widget, row, column, rowSpan, columnSpan)
    
  def _makeGrid(self):
    self.window.equalSignal.connect(self._equalButtonClick)
    self.window.backspaceSignal.connect(self.display.backspace)
    self.window.clearSignal.connect(self._clear)
    self.window.numberOrDotSignal.connect(self._buttonClick)
    self.window.operatorSignal.connect(self._operatorClick)
    
    for rowIndex, row in enumerate(self._gridMask):
      columnIndexDecrement = 0
      for columnIndex, column in enumerate(row):
        if isEmpty(column):
          columnIndexDecrement = 1
          continue
        
        span = 2 if column == '0' else 1
        
        if (rowIndex != len(self._gridMask) - 1 or column != '0'):
          adjustedColumnIndex = columnIndex
        else:
          adjustedColumnIndex = columnIndex - columnIndexDecrement
          
        button = Button(column)
        
        if not isNumOrDot(column):
          button.setProperty("cssClass", "specialButton")
          self._configSpecialButton(button)
                    
        self.addWidgetToGrid(button, rowIndex, adjustedColumnIndex, 1, span)
        
        buttonSlot = self._makeButtonSlot(self._buttonClick, button.text())
        self._connectButtonClick(button, buttonSlot)
        
  def _connectButtonClick(self, button: Button, slot):
    button.clicked.connect(slot)
    
  def _configSpecialButton(self, button: Button):
    buttonText = button.text()    
    
    if buttonText == 'C':
      # button.clicked.connect(self.display.clear)
      self._connectButtonClick(button, self._clear)
      return
    
    if buttonText in '+-x/^':
      buttonSlot = self._makeButtonSlot(self._operatorClick, buttonText)
      self._connectButtonClick(button, buttonSlot)
      return
      
    if buttonText == '=':
      self._connectButtonClick(button, self._equalButtonClick)
      return
    
    if buttonText == '◀':
      self._connectButtonClick(button, self.display.backspace)
      return
        
  @Slot()
  def _makeButtonSlot(self, func, *args, **kwargs):
    @Slot(bool)
    def buttonSlot(_):
      func(*args, **kwargs)
    return buttonSlot
  
  @Slot()
  def _buttonClick(self, buttonText):
    # teste: str = 'um valor'    
    # teste = 1
    newDisplayText = self.display.text() + buttonText
    
    isValid, strNumber = isValidNumber(newDisplayText)
    
    if not isValid:
      return    
    
    self.display.setText(strNumber)
    
  @Slot()
  def _operatorClick(self, buttonText):
    displayText = self.display.text()
    self.display.clear()
    
    isValid, _ = isValidNumber(displayText)
    
    if not isValid and self._left is None:
      return
    
    self._operator = buttonText
    
    if isValid:
      if self._left is None:
        self._left = formatNumber(displayText)
      else:
        self._right = formatNumber(displayText)     
    
    if not self._right is None:
      self.equation = f'{self._left} {self._operator} {self._right}'
    else:
      self.equation = f'{self._left} {self._operator}'
      
  @Slot()
  def _equalButtonClick(self):
    if self._left is None or self._operator is None:
      return
    
    displayText = self.display.text()
    
    isValid, _ = isValidNumber(displayText)
    
    if not isValid:
      return
    
    self._right = formatNumber(displayText)
    self.equation = f'{self._left} {self._operator} {self._right}'
    
    # result = eval(f'{self._left} {self._operator} {self._right}')
    result = self._calculate()
    
    if result is None:
      return
    
    if (result == 'error'):
      errorText = f'{self._left} {self._operator} {self._right} = Error'
      self._clear()
      self._info.setText(errorText)      
      return
    
    self._info.setText(f'{self.equation} = {result}')        
    self._left = result
    self._right = None
    self.display.clear()
    
  @Slot()
  def _clear(self):
    self._left = None
    self._right = None
    self._operator = None
    self.display.clear()
    self.equation = self._emptyEquationText
    
  def clearDisplay(self):
    if self._left is None:
      self._display.setText('0')        
    else:
      self._display.setText(None)
    
  @Slot()
  def _calculate(self):
    if not isinstance(self._left, (int,float)) or not isinstance(self._right, (int,float)):
      return None
    try:
      if self._operator == '+':
        return self._left + self._right
      elif self._operator == '-':
        return self._left - self._right
      elif self._operator == 'x':
        return self._left * self._right
      elif self._operator == '/':
        return self._left / self._right
      elif self._operator == '^':
        # return self._left ** self._right
        return math.pow(self._left, self._right)
      return None
    except OverflowError:
      self._showError('Esta conta não pode ser realizada')
      return 'error' 
    except ZeroDivisionError:
      self._showError('Divisão por zero')
      return int(0)
    except:      
      return None
    
  def _showError(self, text):
    messageBox = self.window.messageBox()
    messageBox.setIcon(messageBox.Icon.Critical)
    messageBox.setText(text)
    
    messageBox.exec()
    
    # messageBox.setInformativeText(
    #   "A divisão por zero ocorre quando tentamos dividir qualquer número por zero. "
    #   "Não há um resultado válido para essa situação, levando a uma indeterminação."
    #   "Em muitos contextos, é tratada como indefinida, exigindo precauções ao lidar com equações e problemas numéricos."
    # )
    
    # messageBox.setStandardButtons(
    #   messageBox.StandardButton.Ok |
    #   messageBox.StandardButton.Cancel
    # )
    
    # messageBox.button(messageBox.StandardButton.Ok).setText('OK')
    
    # result = messageBox.exec()    
    
    # if result == messageBox.StandardButton.Ok:
    #   ...