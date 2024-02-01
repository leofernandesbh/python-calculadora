from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel
from consts.consts import SMALL_FONT_SIZE

class AccountInfo(QLabel):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.configStyle()
  
  def configStyle(self):
    font = self.font()
    font.setPixelSize(SMALL_FONT_SIZE)
    self.setFont(font)
    self.setAlignment(Qt.AlignRight)    