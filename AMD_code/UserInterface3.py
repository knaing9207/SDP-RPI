import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Example")
        self.setGeometry(0, 0, 800, 480)  # Set window dimensions
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(20)  # Set horizontal spacing between columns
        grid_layout.setVerticalSpacing(20)  # Set vertical spacing between rows
        grid_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0
        self.central_widget = QWidget()
        self.central_widget.setLayout(grid_layout)
        self.setCentralWidget(self.central_widget)

        button_labels = ["Button 1", "Button 2", "Button 3", "Button 4",
                         "Button 5", "Button 6", "Button 7", "Button 8"]

        row, col = 0, 0
        for label in button_labels:
            button = QPushButton(label)
            button.setFixedSize(300, 90)  # Set button size
            button.setStyleSheet("""
                QPushButton {
                    font-weight: bold;
                    font-size: 60px;
                    border: 4px solid black;
                    background-color: white;  /* Set normal background color */
                }
                QPushButton:pressed {
                    background-color: lightgrey;  /* Set pressed background color */
                }
            """)
            grid_layout.addWidget(button, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
