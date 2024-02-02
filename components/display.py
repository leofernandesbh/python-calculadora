from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLineEdit
from consts.consts import BIG_FONT_SIZE, MINIMUM_DISPLAY_WIDTH, TEXT_MARGIN

class Display(QLineEdit):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configStyle()    
    
  def configStyle(self):
    self.setReadOnly(True)    
    font = self.font()
    font.setPixelSize(BIG_FONT_SIZE)
    self.setFont(font)
    self.setFixedHeight(BIG_FONT_SIZE * 1.5)
    self.setMinimumWidth(MINIMUM_DISPLAY_WIDTH)
    self.setAlignment(Qt.AlignRight)
    self.setTextMargins(TEXT_MARGIN, 0, TEXT_MARGIN, 0)