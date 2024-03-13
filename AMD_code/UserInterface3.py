import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Example")
        self.setGeometry(0, 0, 800, 480)  # Set window dimensions
        
        # Define button screen mappings
        self.button_mappings = {
            "Add Med": "screen_1",
            "Delete Med": "screen_2",
            "Med Info": "screen_3",
            "Sound": "screen_4",
            "Home": "main_menu"  # Added mapping for the "Back" button to return to main menu
            # Add mappings for other buttons here...
        }

        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(200)  # Set horizontal spacing between columns
        self.grid_layout.setVerticalSpacing(20)  # Set vertical spacing between rows
        self.grid_layout.setContentsMargins(20, 20, 20, 20)  # Set margins to 20
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.central_widget)

        self.updateScreen("main_menu")

    def updateScreen(self, screen):
        """Updates the displayed options based on the current screen context."""
        self.clearLayout(self.grid_layout)
        button_labels = self.getButtonLabels(screen)
        row, col = 0, 0
        for label in button_labels:
            if label is None:
                empty_widget = QWidget()  # Create an empty widget
                self.grid_layout.addWidget(empty_widget, row, col)
            else:
                button = QPushButton(label)
                button.setFixedSize(250, 90)  # Set button size
                button.setStyleSheet("""
                    QPushButton {
                        font-weight: bold;
                        font-size: 40px;
                        border: 4px solid black;
                        background-color: white;  /* Set normal background color */
                    }
                    QPushButton:pressed {
                        background-color: lightgrey;  /* Set pressed background color */
                    }
                """)
                if label == "Add Med":  # Check if the label is "1"
                    icon_path = os.path.join(os.path.dirname(__file__), "icon1.png")
                    pixmap = QPixmap(icon_path)
                    pixmap_resized = pixmap.scaled(25, 25)  # Resize the icon
                    icon = QIcon(pixmap_resized)
                    button.setIcon(icon)
                    button.setIconSize(pixmap_resized.size())  # Set icon size to match pixmap size
                if label in self.button_mappings:
                    button.clicked.connect(self.onButtonClick)
                    button.screen = self.button_mappings[label]
                self.grid_layout.addWidget(button, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

    def getButtonLabels(self, screen):
        if screen == "main_menu":
            return ["Add Med", "Med Info", None, None, None, None, "Delete Med", "Sound"]
        elif screen == "screen_1":
            return ["1", None, None, None, None, None, "Home", "Ok"]
        elif screen == "screen_2":
            return ["1", None, None, None, None, None, "Home", "ok"]
        elif screen == "screen_3":
            return ["1", None, None, None, None, None, "Home", None]
        # Define button labels for other screens here...
        else:
            return ["These are the instructions for this page","Back"]  # Default to "Back" button for unknown screens

    def clearLayout(self, layout):
        """Remove all widgets from the layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def onButtonClick(self):
        sender = self.sender()
        self.updateScreen(sender.screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())