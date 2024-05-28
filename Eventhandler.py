import sys
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import(QApplication,
                              QWidget,
                              QLabel,
                              QMainWindow,
                              QVBoxLayout)
from PySide6.QtCore import Qt

class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Event Handling Ex")
        
        self.set_main_wd()
        self.sub_wnd = CW()
        self.show()
    
    def set_main_wd(self):
        label = QLabel("""<p>Press the <b>ESD </b> key
                       to quit this program.</p>""")
        self.setCentralWidget(label)
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            print('ESC key Pressed!')
            self.close()
            
        elif event.key() == Qt.Key.Key_A:
            print('A key Pressed!')
            self.sub_wnd.show()  
            
class CW(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 100, 300, 200)
        label = QLabel("""<p>Press the <b>Q </b> key
                       to quit this program.</p>""")
        lm = QVBoxLayout(label)
        lm.addWidget(label)
        self.setLayout(lm)
        
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Q:
            print('Q key Pressed!')
            self.hide()
        return super().keyPressEvent(event)

                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwd = MW()
    sys.exit(app.exec())