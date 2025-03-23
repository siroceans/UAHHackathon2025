import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QMessageBox, QWidget, QTabWidget, \
    QVBoxLayout, QMenuBar, QAction, QMenu, QLabel
from PyQt5.QtGui import QFont, QColor, QMovie
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#from (jorges script) import (function)
from plane import UAV_mapper

# Colors
black = QColor(44, 42, 41)      # a dark greyish black
green = QColor(50, 205, 50)     # lime green
UAV_mapper('UAV_Rotation')

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lequipe du Citron")

        self.setStyleSheet("""
            QMainWindow {
                background-color: green;
            }
        """)

        self.setCentralWidget(MyTableWidget(self))
        self.showMaximized()


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a layout object and assign it before adding widgets
        self.layout = QVBoxLayout(self)

        # Tabs setup
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab1.setObjectName("tab1")
        self.tab2 = QWidget()
        self.tab2.setObjectName("tab2")
        self.tabs.addTab(self.tab1, "UAV Orientation")
        self.tabs.addTab(self.tab2, "Satellite Plots")

        self.init_tab1()
        self.init_tab2()

        self.tabs.setStyleSheet("""
        QTabWidget::pane {
            border: none;
            background-color: green;
        }
    
        QTabBar::tab {
           background: white;
            color: black;
            padding: 10px;
            border: 1px solid black;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
    
        QTabBar::tab:selected {
            background: black;
            color: white;
        }
    
        QWidget#tab1, QWidget#tab2 {
         background: black;
        }
    """)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def init_tab1(self):
        # No layout — we’ll position widgets manually
        self.textbox = QLineEdit(self.tab1)
        self.textbox.setAlignment(Qt.AlignCenter)

        self.gif_label = QLabel(self.tab1)

        self.movie = QMovie("./gifs/UAV_Rotation.gif")  # Use the correct path to your gif
        self.gif_label.setMovie(self.movie)
        self.gif_label.move(100, 200)

        self.movie.start()
        # Initial layout
        self.update_layout_tab1()

    def init_tab2(self):
        layout = QVBoxLayout()

        # Create a matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plot something
        ax = self.figure.add_subplot(111)
        ax.plot([0, 1, 2, 3], [10, 20, 15, 30])
        ax.set_title("Sample Plot")

        # Add canvas to layout
        layout.addWidget(self.canvas)

        self.tab2.setLayout(layout)


    def resizeEvent(self, event):
        self.update_layout_tab1()
        return super().resizeEvent(event)

    def update_layout_tab1(self):
        # Dynamic width and height
        width = self.width()
        height = self.height()

        # Position and sizing
        x_siz = int(width * 0.2)
        y_siz = int(height * 0.05)

        x_pos = int(width*0.4)
        y_pos = int(height*0.05)

        font_size = int(y_siz * 0.25)

        font = QFont("Times", font_size)

        self.textbox.setFont(font)

        self.textbox.resize(x_siz, y_siz)
        self.textbox.move(x_pos, y_pos)

        # Optional: Style
        self.textbox.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 4px solid black;
                border-radius: 8px;
                padding: 5px;
            }
        """)

        self.gif_label.move(-50, int(height*0.1))

        #self.button.setStyleSheet("""
        #    QPushButton {
        #        background-color: white;
        #        border: 4px solid black;
        #        border-radius: 8px;
        #        padding: 5px;
        #    }
        #""")

    @pyqtSlot()
    def on_click(self):
        text = self.textbox.text()
        QMessageBox.information(self, "Text Entered", f"You typed: {text}")
        self.textbox.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())