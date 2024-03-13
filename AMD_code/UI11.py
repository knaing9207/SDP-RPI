import sys
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout
import RPi.GPIO as GPIO

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Example")
        self.setGeometry(0, 0, 800, 480)  # Set window dimensions

        # Define button screen mappings
        self.button_mappings = {
            "1": "screen_2",
            "2": "screen_3",
            "3": "screen_4",
            "4": "screen_5",
            "5": "screen_6",
            "6": "screen_7",
            "7": "screen_8",
            "8": "screen_9"
            # Add mappings for other buttons here...
        }

        self.initUI()
        self.setupGPIO()

    def initUI(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(20)  # Set horizontal spacing between columns
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
        for label, screen, button_pin in button_labels:
            if label is None:
                empty_widget = QWidget()  # Create an empty widget
                self.grid_layout.addWidget(empty_widget, row, col)
            else:
                button = QPushButton(label)
                button.setFixedSize(300, 90)  # Set button size
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
                button.clicked.connect(lambda _, screen=screen: self.updateScreen(screen))
                self.grid_layout.addWidget(button, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

    def getButtonLabels(self, screen):
        if screen == "main_menu":
            return [("1", "screen_2", 0),
                    ("2", "screen_3", 1),
                    ("3", "screen_4", 22),
                    ("4", "screen_5", 23),
                    ("5", "screen_6", 5),
                    ("6", "screen_7", 6),
                    ("7", "screen_8", 16),
                    ("8", "screen_9", 26)]
        elif screen == "screen_2":
            return [("9", "main_menu", None)]  # Example of back button
        # Define button labels for other screens here...
        else:
            return [("1", "main_menu", None)]  # Default to "Back" button for unknown screens

    def clearLayout(self, layout):
        """Remove all widgets from the layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def setupGPIO(self):
        """Configures the GPIO pins for the Raspberry Pi."""
        GPIO.setmode(GPIO.BCM)  # Use Broadcom SOC channel numbers
        self.button_pins = [0, 1, 22, 23, 5, 6, 16, 26]  # Update to your specific GPIO pin setup
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.timer = QTimer()
        self.timer.timeout.connect(self.checkButtonPresses)
        self.timer.start(100)

    def checkButtonPresses(self):
        """Checks GPIO pins for button presses and triggers corresponding UI actions."""
        for i, pin in enumerate(self.button_pins):
            if GPIO.input(pin) == GPIO.LOW:
                self.buttonClicked(i)
                time.sleep(0.2)  # Debounce delay

    def buttonClicked(self, index):
        """Function to handle button click."""
        if index < len(self.button_pins):
            pin = self.button_pins[index]
            if pin in range(8):  # Assuming there are 8 buttons
                button_label = str(index + 1)
                if button_label in self.button_mappings:
                    screen = self.button_mappings[button_label]
                    self.updateScreen(screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
