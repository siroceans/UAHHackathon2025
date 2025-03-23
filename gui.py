import sys
from PyQt5 import QtCore
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

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lequipe du Citron")

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {black.name()};
            }}
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
        self.tab3 = QWidget()
        self.tab3.setObjectName("tab3")
        self.tabs.addTab(self.tab1, "Home Page")
        self.tabs.addTab(self.tab2, "UAV Orientation")
        self.tabs.addTab(self.tab3, "Satellite Plots")

        self.init_tab1()
        self.init_tab2()
        self.init_tab3()

        self.tabs.setStyleSheet(f"""
        QTabWidget::pane {{
            border: none;
            background-color: {green.name()};
        }}
    
        QTabBar::tab {{
            background: {black.name()};
            color: {green.name()};
            padding: 10px;
            border: 1px solid black;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}
    
        QTabBar::tab:selected {{
            background: {green.name()};
            color: {black.name()};
        }}
    
        QWidget#tab1, QWidget#tab2 {{
         background: {black.name()};
        }}
    """)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
    def init_tab1(self):

        self.button12 = QPushButton("Button 1", self.tab1)
        self.button12.setGeometry(100, 50, 120, 40)  # x, y, width, height
        self.button12.clicked.connect(lambda: self.tabs.setCurrentIndex(1))


        self.button13 = QPushButton("Button 2", self.tab1)
        self.button13.setGeometry(250, 50, 120, 40)
        self.button13.clicked.connect(lambda: self.tabs.setCurrentIndex(2))


        self.gif_label11 = QLabel(self.tab1)
        self.movie11 = QMovie("./gifs/UAV_Rotation.gif")  # Use the correct path to your gif
        self.gif_label11.setMovie(self.movie11)
        self.movie11.start()
        self.gif_label11.setGeometry(1920//2,50,1000,300)
        

        self.gif_label12 = QLabel(self.tab1)
        self.movie12 = QMovie("./gifs/UAV_Rotation.gif")  # Use the correct path to your gif
        self.gif_label12.setMovie(self.movie12)
        self.movie12.start()
        self.gif_label12.setGeometry(100, 50, 120, 40)    


        self.gif_label13 = QLabel(self.tab1)
        self.movie13 = QMovie("./gifs/UAV_Rotation.gif")  # Use the correct path to your gif
        self.gif_label13.setMovie(self.movie13)
        self.movie13.start()
        self.gif_label13.setGeometry(250, 50, 120, 40)


        self.gif_label14 = QLabel(self.tab1)
        self.movie14 = QMovie("./gifs/UAV_Rotation.gif")  # Use the correct path to your gif
        self.gif_label14.setMovie(self.movie14)
        self.movie14.start()
        self.gif_label14.setGeometry(250, 50, 120, 40)


        self.update_layout_tab1()


    def init_tab2(self):
        # No layout — we’ll position widgets manually
        self.textbox = QLineEdit(self.tab1)
        self.textbox.setAlignment(Qt.AlignCenter)

        self.gif_label = QLabel(self.tab2)

        self.movie = QMovie("./gifs/UAV_Rotation.gif")  # Use the correct path to your gif
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        # Initial layout
        self.update_layout_tab2()

    def init_tab3(self):
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

        self.tab3.setLayout(layout)

    def resizeEvent(self, event):

        current_index = self.tabs.currentIndex()

        if current_index == 0:
            self.update_layout_tab1()
        elif current_index == 1:
            self.update_layout_tab2()
        elif current_index == 2:
            self.update_layout_tab3()

        return super().resizeEvent(event)

    def update_layout_tab1(self):
        width = self.width()
        height = self.height()

        # --------- GIF 11 (Center at 50% width, 25% height) ---------
        x_siz1 = int(width * 0.5)
        y_siz1 = int(height * 0.5)
        x_center1 = int(width * 0.5)
        y_center1 = int(height * 0.15)
        x_pos1 = x_center1 - (x_siz1 // 2)
        y_pos1 = y_center1 - (y_siz1 // 2)

        self.gif_label11.setGeometry(x_pos1, y_pos1, x_siz1, y_siz1)
        self.movie11.setScaledSize(QtCore.QSize(x_siz1, y_siz1))

        # --------- GIF 12 ---------
        x_siz2 = int(width * 0.2)
        y_siz2 = int(height * 0.2)
        x_center2 = int(width * 0.3)
        y_center2 = int(height * 0.6)
        x_pos2 = x_center2 - (x_siz2 // 2)
        y_pos2 = y_center2 - (y_siz2 // 2)

        self.gif_label12.setGeometry(x_pos2, y_pos2, x_siz2, y_siz2)
        self.movie12.setScaledSize(QtCore.QSize(x_siz2, y_siz2))

        self.button12.setGeometry(x_pos2, y_pos2, x_siz2, y_siz2)
        self.button12.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgba(0, 0, 0, 0);
            }
        """)
        self.button12.raise_()

        # --------- GIF 13 ---------
        x_siz3 = int(width * 0.2)
        y_siz3 = int(height * 0.2)
        x_center3 = int(width * 0.7)
        y_center3 = int(height * 0.6)
        x_pos3 = x_center3 - (x_siz3 // 2)
        y_pos3 = y_center3 - (y_siz3 // 2)

        self.gif_label13.setGeometry(x_pos3, y_pos3, x_siz3, y_siz3)
        self.movie13.setScaledSize(QtCore.QSize(x_siz3, y_siz3))

        self.button13.setGeometry(x_pos3, y_pos3, x_siz3, y_siz3)
        self.button13.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: rgba(0, 0, 0, 0);
            }
        """)
        self.button13.raise_()

        # --------- GIF 14 (Bottom Right Margin) ---------
        margin4 = int(width * 0.05)
        x_siz4 = int(width * 0.2)
        y_siz4 = int(height * 0.2)
        x_pos4 = width - x_siz4 - margin4
        y_pos4 = height - y_siz4 - margin4

        self.gif_label14.setGeometry(x_pos4, y_pos4, x_siz4, y_siz4)
        self.movie14.setScaledSize(QtCore.QSize(x_siz4, y_siz4))


    def update_layout_tab2(self):
        # Dynamic width and height
        width = self.width()
        height = self.height()

        # Position and sizing
        x_siz = int(width * 0.2)
        y_siz = int(height * 0.05)

        x_pos = int(width*0.7)
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

        self.gif_label.move(-200, int(height*0.1))

        #self.button.setGeometry(int(width * 0.1), int(height * 0.2), 200, 50)
        #self.button.setStyleSheet("""
        #    QPushButton {
        #        background-color: white;
        #        border: 4px solid black;
        #        border-radius: 8px;
        #        padding: 5px;
        #    }
        #""")

    def update_layout_tab3(self):
        # Dynamic width and height
        width = self.width()
        height = self.height()

        # Position and sizing
        x_siz = int(width * 0.2)
        y_siz = int(height * 0.05)

        x_pos = int(width*0.7)
        y_pos = int(height*0.05)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())