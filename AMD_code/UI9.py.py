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
        self.setGeometry(0, 0, 800, 480)  # Geometry for a standard display
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
            # Style changes here for high contrast and larger size
            button.setStyleSheet("font-size: 28px; padding: 30px; background-color: yellow; color: black;")
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
        GPIO.setmode(GPIO.BCM)  # Use Broadcom SOC channel numbers
        self.button_pins = [0, 1, 22, 23, 5, 6, 16, 26]  # Update to your specific GPIO pin setup
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.timer = QTimer()
        self.timer.timeout.connect(self.checkButtonPresses)
        self.timer.start(100)

    # def checkButtonPresses(self):
    #     """Checks for physical button presses and triggers corresponding UI actions."""
    #     for i, pin in enumerate(self.button_pins):
    #         if not GPIO.input(pin):  # Button is pressed (GPIO pin is low)
    #             # Execute in the GUI thread to ensure thread safety
    #             QTimer.singleShot(0, lambda b=i: self.physicalButtonPressed(b))
        
    def checkButtonPresses(self):
        """Checks GPIO pins for button presses and triggers corresponding UI actions."""
        for i, pin in enumerate(self.button_pins):
            if GPIO.input(pin) == GPIO.LOW:
                self.buttonClicked(i)
                time.sleep(0.2)  # Debounce delay

    def physicalButtonPressed(self, button_index):
        """Handles the GUI update when a physical button is pressed."""
        self.buttons[button_index].setStyleSheet("font-size: 28px; padding: 30px; background-color: red; color: white;")
        QTimer.singleShot(1000, lambda b=button_index: self.resetButtonStyle(b))  # Reset style after 1 second

    def resetButtonStyle(self, button_index):
        """Resets the button style after it has been pressed."""
        self.buttons[button_index].setStyleSheet("font-size: 28px; padding: 30px; background-color: yellow; color: black;")

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
        }
        self.current_screen = screen
        screen_options = self.options[screen]

        for i, button in enumerate(self.buttons):
            if i < len(screen_options):
                button.setText(screen_options[i])
                button.setVisible(True)
            else:
                button.setVisible(False)

    def buttonClicked(self, button_index):
        """Handles actions triggered by button clicks."""
        selected_option = self.buttons[button_index].text()
        if selected_option in self.options:
            self.updateScreen(selected_option)
        elif selected_option == "Back":
            self.updateScreen("main_menu")
        else:
            print(f"{selected_option} selected")  # Placeholder for actual functionality

def main():
    app = QApplication(sys.argv)
    window = MedicationDispenser()
    window.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
main()
