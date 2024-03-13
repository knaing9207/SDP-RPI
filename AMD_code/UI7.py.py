import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSpacerItem, \
    QSizePolicy
from PyQt5.QtCore import Qt, QTimer
import RPi.GPIO as GPIO
import pyttsx3

class MedicationDispenser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medication Dispenser')
        self.setGeometry(0, 0, 800, 480)  # Geometry for 5-inch DSI display
        self.current_screen = "main_menu"
        self.setupUI()
        self.setupGPIO()
        self.tts_engine = pyttsx3.init()

    def setupUI(self):
        """Initializes the user interface components."""
        self.layout = QVBoxLayout()
        self.label = QLabel("Select an option:")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.layout.addWidget(self.label)

        # Central layout for two columns of buttons
        centralLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # Spacers for central alignment
        leftSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        rightSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttons = []
        for i in range(8):
            button = QPushButton()
            # Updated styles for high contrast: yellow background and black text
            button.setStyleSheet("font-size: 22px; padding: 20px; background-color: yellow; color: black;")
            button.clicked.connect(lambda _, b=i: self.buttonClicked(b))
            self.buttons.append(button)
            if i < 4:
                leftLayout.addWidget(button)
            else:
                rightLayout.addWidget(button)

        centralLayout.addItem(leftSpacer)
        centralLayout.addLayout(leftLayout)
        centralLayout.addLayout(rightLayout)
        centralLayout.addItem(rightSpacer)

        self.layout.addLayout(centralLayout)
        self.setLayout(self.layout)
        self.updateScreen("main_menu")

    def setupGPIO(self):
        """Configures the GPIO pins for the Raspberry Pi."""
        GPIO.setmode(GPIO.BCM)
        self.button_pins = [0, 1, 22, 23, 5, 6, 16, 26]  # Adjust these pin numbers according to your setup
        self.tts_button_pin = 26  # Example pin for text-to-speech functionality
        for pin in self.button_pins + [self.tts_button_pin]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.timer = QTimer()
        self.timer.timeout.connect(self.checkButtonPresses)
        self.timer.start(100)

    def checkButtonPresses(self):
        """Checks for physical button presses and triggers corresponding UI actions."""
        for i, pin in enumerate(self.button_pins):
            if GPIO.input(pin) == GPIO.LOW:
                # Temporarily change the button's color to red to indicate it's being pressed
                self.buttons[i].setStyleSheet("font-size: 22px; padding: 20px; background-color: red; color: white;")
                QTimer.singleShot(1000, lambda b=i: self.resetButtonStyle(b))  # Reset style after 1 second
                self.buttonClicked(i)  # Simulate clicking the corresponding UI button
                time.sleep(0.2)  # Debounce delay

    def resetButtonStyle(self, button_index):
        """Resets the button style after it has been pressed."""
        self.buttons[button_index].setStyleSheet("font-size: 22px; padding: 20px; background-color: yellow; color: black;")

    def updateScreen(self, screen):
        """Dynamically updates the screen based on the user's selection."""
        self.options = {
            "main_menu": ["Add Pill", "Medicine Info", "Set Reminder", "Check Schedule", "Emergency", "Settings",
                          "Help", "Exit"],
            "Add Pill": ["Enter Pill Name", "Dosage", "Frequency", "Confirm", "Back"],
            "Medicine Info": ["Search by Name", "View All", "Back"],
            "Set Reminder": ["Add New", "View Existing", "Back"],
            "Check Schedule": ["Today", "This Week", "Back"],
            "Emergency": ["Contact Doctor", "Contact Pharmacy", "Back"],
            "Settings": ["Volume Control", "Screen Brightness", "Back"],
            "Help": ["User Guide", "FAQ", "Back"]
            # Add other screens and options as needed
        }
        self.current_screen = screen  # Update current screen context
        screen_options = self.options[screen]

        # Update button labels and visibility based on the current screen's options
        for i, button in enumerate(self.buttons):
            if i < len(screen_options):
                button.setText(screen_options[i])
                button.setVisible(True)  # Show button with updated text
                # Ensure the button color is reset to yellow and black
                button.setStyleSheet("font-size: 22px; padding: 20px; background-color: yellow; color: black;")
            else:
                button.setVisible(False)  # Hide buttons not used in the current screen

    def buttonClicked(self, button_index):
        """Handles actions triggered by button clicks."""
        selected_option = self.buttons[button_index].text()
        # Implement navigation or functionality based on the selected option
        print(f"{selected_option} selected")  # Placeholder for actual functionality

    # Implement other methods as needed...

def main():
    app = QApplication(sys.argv)
    window = MedicationDispenser()
    window.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
main()
