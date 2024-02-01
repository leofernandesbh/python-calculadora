import sys

from theme.styles import setupTheme
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from consts.consts import WINDOW_ICON_PATH
from components.main_window import MainWindow
from components.account_info import AccountInfo
from components.display import Display
from components.buttons import Button, ButtonsGrid

if __name__ == "__main__":
  app = QApplication(sys.argv)
  setupTheme()
  window = MainWindow()  
  
  icon = QIcon(str(WINDOW_ICON_PATH))
  app.setWindowIcon(icon)
  window.setWindowIcon(icon)
  
  # Display Header
  accountInfo = AccountInfo()
  window.addWidgetToMainLayout(accountInfo)
  
  # Display
  display = Display()
  window.addWidgetToMainLayout(display)  
  
  # Buttons Grid
  buttonsGrid = ButtonsGrid(display, accountInfo, window)
  window.addLayoutToMainLayout(buttonsGrid)
  
  window.adjustFixedSize()
  window.show()    
  app.exec()