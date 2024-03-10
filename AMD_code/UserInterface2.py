import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog
from PyQt5.QtCore import QTimer
import RPi.GPIO as GPIO
import pyttsx3

class MedicationDispenser(QWidget):
    
    # Define the options available in each screen
    options = {
            "main_menu": ["Add Pill", "Medicine Info", "Set Reminder", "Check Schedule", "Emergency", "Settings", "Help", ""],
            "Add Pill": ["OCR","","","Back"],
            "Settings": ["Change Name", "Volume Control", "Screen Brightness", "Back"],
            # Add additional options for each submenu here...
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medication Dispenser')
        self.setGeometry(0, 0, 800, 480)  # Geometry for a 5-inch DSI display
        self.userName = self.loadUserName()  # Load or ask for the user name
        self.current_screen = "main_menu"
        self.setupUI()
        self.setupGPIO()
        self.tts_engine = pyttsx3.init()

    def loadUserName(self):
        """Loads the user's name from a file, or prompts for it if not found."""
        try:
            with open("username.txt", "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            name, ok = QInputDialog.getText(self, "User Name", "Enter your name:")
            if ok and name:
                with open("username.txt", "w") as file:
                    file.write(name)
                return name
            return "User"  # Default name if none provided

    def setupUI(self):
        """Initializes the user interface components."""
        self.layout = QVBoxLayout()
        self.label = QLabel(f"Hello, {self.userName}!")
        self.label.setStyleSheet("font-size: 30px; font-weight: bold; color: black; margin-bottom: 20px;")
        self.layout.addWidget(self.label)

        # Layouts for button arrangement
        centralLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # Style and size settings for the buttons
        buttonStyle = "QPushButton { font-size: 22px; padding: 20px; background-color: #f0f0f0; color: black; margin: 5px; }"
        self.buttons = []
        for i in range(8):
            button = QPushButton()
            button.setStyleSheet(buttonStyle)
            button.setFixedSize(300, 80)  # Ensuring buttons are not oversized
            button.clicked.connect(lambda _, b=i: self.buttonClicked(b))
            self.buttons.append(button)
            if i < 4:
                leftLayout.addWidget(button)
            else:
                rightLayout.addWidget(button)

        # Adding layouts to the central layout
        centralLayout.addLayout(leftLayout)
        centralLayout.addStretch(1)  # Space between button columns
        centralLayout.addLayout(rightLayout)

        self.layout.addLayout(centralLayout)
        self.setLayout(self.layout)
        self.updateScreen("main_menu")

    def setupGPIO(self):
        """Configures GPIO pins for button inputs."""
        GPIO.setmode(GPIO.BCM)
        self.button_pins = [0, 1, 22, 23, 5, 6, 16, 26]
        self.tts_button_pin = 26
        for pin in self.button_pins + [self.tts_button_pin]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Timer to periodically check button presses
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkButtonPresses)
        self.timer.start(100)

    def updateScreen(self, screen):
        """Updates the displayed options based on the current screen context."""
        self.current_screen = screen
        screen_options = self.options.get(screen, ["Back"])  # Default to 'Back' option if screen not defined

        for i, button in enumerate(self.buttons):
            if i < len(screen_options):
                button.setText(screen_options[i])
                button.setVisible(True)
            else:
                button.setVisible(False)  # Hide buttons not needed for the current screen

    def buttonClicked(self, button_index):
        """Handles button click events for navigation and actions."""
        selected_option = self.buttons[button_index].text()
        if selected_option == "Change Name" and self.current_screen == "Settings":
            self.changeUserName()
        elif selected_option == "Back":
            self.updateScreen("main_menu")
        else:
            # For main menu options, navigate to the corresponding screen
            if self.current_screen == "main_menu":
                self.updateScreen(selected_option)
            else:
                # Placeholder for implementing specific functionality
                print(f"{selected_option} selected in {self.current_screen}")

    def changeUserName(self):
        """Allows the user to change their name via a dialog."""
        newName, ok = QInputDialog.getText(self, "Change Name", "Enter your new name:")
        if ok and newName:
            self.userName = newName
            with open("username.txt", "w") as file:
                file.write(newName)
            self.label.setText(f"Hello, {self.userName}!")  # Update greeting

    def checkButtonPresses(self):
        """Checks GPIO pins for button presses and triggers corresponding UI actions."""
        for i, pin in enumerate(self.button_pins):
            if GPIO.input(pin) == GPIO.LOW:
                self.buttonClicked(i)
                time.sleep(0.2)  # Debounce delay

        if GPIO.input(self.tts_button_pin) == GPIO.LOW:
            self.readOptionsAloud()

    def readOptionsAloud(self):
        """Uses Text-to-Speech to read out the current screen's options."""
        options_text = ", ".join(self.options.get(self.current_screen, []))
        self.tts_engine.say(options_text)
        self.tts_engine.runAndWait()
        time.sleep(0.2)  # Prevent rapid re-triggering

def main():
    app = QApplication(sys.argv)
    window = MedicationDispenser()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
