import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel,
    QVBoxLayout, QWidget, QStatusBar, QHBoxLayout, QFileDialog, QMessageBox
)
import matplotlib.pyplot as plt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.image import imread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Directory Tree and Image Viewer")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        main_widget.setLayout(layout)

        self.tree_view = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(''))
        self.tree_view.clicked.connect(self.load_image_from_tree)

        layout.addWidget(self.tree_view)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.axis('off')
        layout.addWidget(self.canvas)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        menubar.setNativeMenuBar(False)

        open_action = QAction("Open Directory", self)
        open_action.triggered.connect(self.open_directory)
        file_menu.addAction(open_action)

        self.dragging = False
        self.rect = None
        self.start_point = (0, 0)
        self.click_count = 0
        self.image = None

        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.canvas.mpl_connect('button_release_event', self.on_release)

    def open_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.tree_view.setRootIndex(self.model.index(dir_path))

    def load_image_from_tree(self, index):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.load_image(file_path)

    def load_image(self, file_path):
        self.image = imread(file_path)
        self.ax.clear()
        self.ax.imshow(self.image)
        self.ax.axis('on')
        self.canvas.draw()

    def on_click(self, event):
        if self.image is None:
            return
        if event.button == 3:
            self.on_right_click(event)
        else:
            if event.inaxes != self.ax:
                return
            self.dragging = True
            self.start_point = (event.xdata, event.ydata)
            self.rect = self.ax.add_patch(
                plt.Rectangle(self.start_point, 0, 0, 
                              fill=False, color='red')
            )
            self.canvas.draw()

    def on_right_click(self, event):
        if self.image is None:
            return
        if event.dblclick:
            self.ax.add_patch(
                plt.Circle((event.xdata, event.ydata), 
                           10, color='blue', fill=True)
            )
            self.canvas.draw()

    def on_drag(self, event):
        if self.image is None:
            return
        if not self.dragging or not event.inaxes:
            return
        x0, y0 = self.start_point
        x1, y1 = event.xdata, event.ydata
        self.rect.set_width(x1 - x0)
        self.rect.set_height(y1 - y0)
        self.rect.set_xy((min(x0, x1), min(y0, y1)))
        self.canvas.draw()

    def on_release(self, event):
        if self.image is None:
            return
        if event.button == 3:
            return
        if self.dragging:
            self.dragging = False
            response = QMessageBox.question(self, 'Confirm', 'Keep the rectangle?', QMessageBox.Yes | QMessageBox.No)
            if response == QMessageBox.No:
                self.rect.remove()
            self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
