import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QInputDialog
from PyQt5.QtCore import Qt, QTimer
import RPi.GPIO as GPIO
import pyttsx3

class MedicationDispenser(QWidget):

    # Define the options available in each screen
    options = {
            "main_menu": ["Add Med.", "Med. Info", "Reminder", "Schedule", "Settings", None, None, None],
            "Add Medication": ["OCR", None, None, "Back"],
            "Medication Info": [None, None, None, "Back", None, None, None, None],
            "Set Reminder": [None, None, None, "Back", None, None, None, None],
            "Check Schedule": [None, None, None, "Back", None, None, None, None],
            "Settings": [None, "Volume Control", "Screen Brightness", "Back", None, None, None, None],
            # Add additional options for each submenu here...
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medication Dispenser')
        self.setGeometry(0, 0, 800, 480)  # Geometry for a 5-inch DSI display
        self.current_screen = "main_menu"
        self.setupUI()
        self.setupGPIO()
        self.tts_engine = pyttsx3.init()

    def update_time(self):
        time_str = time.strftime("%I:%M %p")
        self.time_label.setText(time_str)
        self.time_label.setAlignment(Qt.AlignCenter)

    def setupUI(self):
        """Initializes the user interface components."""
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setStyleSheet("font-size: 30px; font-weight: bold; color: black; margin-bottom: 20px;")
        self.layout.addWidget(self.label)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.layout.addWidget(self.time_label)

        # Layouts for button arrangement
        centralLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # Style and size settings for the buttons
        buttonStyle = "QPushButton { font-size: 28px; padding: 30px; background-color: #f0f0f0; color: black; margin: 5px; }"
        self.buttons = []
        for i in range(8):
            button = QPushButton()
            button.setStyleSheet(buttonStyle)
            button.setFixedSize(300, 90)  # Ensuring buttons are not oversized
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
        self.timer.timeout.connect(self.update_time)
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
        if selected_option == "Back":
            self.updateScreen("main_menu")
        else:
            # For main menu options, navigate to the corresponding screen
            if self.current_screen == "main_menu":
                self.updateScreen(selected_option)
            else:
                # Placeholder for implementing specific functionality
                print(f"{selected_option} selected in {self.current_screen}")

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
