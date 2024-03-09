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
            button.setStyleSheet("font-size: 22px; padding: 20px; background-color: #f0f0f0; color: black;")
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
        GPIO.setmode(GPIO.BOARD)
        self.button_pins = [11, 13, 15, 16, 18, 22, 29, 31]
        self.tts_button_pin = 33
        for pin in self.button_pins + [self.tts_button_pin]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.timer = QTimer()
        self.timer.timeout.connect(self.checkButtonPresses)
        self.timer.start(100)

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
        self.current_screen = screen  # Update current screen context
        screen_options = self.options[screen]

        # Update button labels and visibility based on the current screen's options
        for i, button in enumerate(self.buttons):
            if i < len(screen_options):
                button.setText(screen_options[i])
                button.setVisible(True)  # Show button with updated text
                button.setStyleSheet("font-size: 22px; padding: 20px; background-color: #f0f0f0; color: black;")
            else:
                button.setVisible(False)  # Hide buttons not used in the current screen

    def buttonClicked(self, button_index):
        """Handles actions triggered by button clicks."""
        selected_option = self.buttons[button_index].text()

        # Logic for handling selections in different screens
        if self.current_screen == "main_menu":
            if selected_option == "Exit":
                self.close()  # Exit application
            else:
                # Navigate to the selected option's screen
                self.updateScreen(selected_option)
        elif selected_option == "Back":
            # Return to the main menu from any sub-screen
            self.updateScreen("main_menu")
        else:
            # Placeholder for specific option actions in sub-screens
            print(f"{selected_option} selected in {self.current_screen}")
            # Implement specific functionalities for each option as required

    def checkButtonPresses(self):
        """Checks for physical button presses and triggers corresponding UI actions."""
        for i, pin in enumerate(self.button_pins):
            if GPIO.input(pin) == GPIO.LOW:
                self.buttonClicked(i)  # Simulate clicking the corresponding UI button
                time.sleep(0.2)  # Debounce delay

    def readOptionsAloud(self):
        """Uses Text-to-Speech to read out options for the current screen."""
        options_text = ", ".join(self.options.get(self.current_screen, []))
        self.tts_engine.say(options_text)
        self.tts_engine.runAndWait()
        time.sleep(0.2)  # Debounce delay


def main():
    app = QApplication(sys.argv)
    window = MedicationDispenser()
    window.show()
    sys.exit(app.exec_())


# if __name__ == "__main__":
main()
