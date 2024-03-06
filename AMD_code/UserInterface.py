# Basic Idea for AMD UserInterface Using PyQt
# Options, pins, and such are for the most part placeholders to see how design looks,
# will change to final options when tests seem fine.

import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
import RPi.GPIO as GPIO
import pyttsx3


class MedicationDispenser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medication Dispenser')
        self.setGeometry(0, 0, 800, 480)  # Set geometry for 5-inch DSI display
        self.current_screen = "main_menu" 
        self.selected_button_index = None  # Track the selected button
        self.setupUI()  # Initialize user interface
        self.setupGPIO()  # Setup GPIO pins for button inputs
        self.tts_engine = pyttsx3.init()  # Initialize Text-to-Speech engine

    def setupUI(self):
        """Initializes the user interface components."""
        self.layout = QVBoxLayout()  # Use a vertical layout
        self.label = QLabel("Select an option:")  # Instruction label
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")  # Make label easily readable
        self.layout.addWidget(self.label)
        self.buttons = []

        # Create buttons with larger text and high contrast for better visibility
        for _ in range(8):
            button = QPushButton()
            button.setStyleSheet("font-size: 22px; padding: 20px; background-color: white; color: black;")
            button.clicked.connect(self.buttonClicked)  # Connect button click signal
            self.buttons.append(button)
            self.layout.addWidget(button)

        self.setLayout(self.layout)
        self.updateScreen()  # Update screen with initial options

    def setupGPIO(self):
        """Configures the GPIO pins for the buttons."""
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        # Define GPIO pins for 8 buttons
        self.button_pins = [11, 13, 15, 16, 18, 22, 29, 31]
        self.tts_button_pin = 33  # GPIO pin for Text-to-Speech function
        for pin in self.button_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pins as input with pull-up
        GPIO.setup(self.tts_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def updateScreen(self):
        """Updates the UI elements based on the current screen."""
        # Define options for each screen
        self.options = {
            "main_menu": [
                "Add Pill",
                "Medicine Information",
                "Set Reminder",
                "Check Schedule",
                "Emergency Contact",
                "Settings",
                "Help",
                "Exit"
            ],
            # Additional screens and options can be defined here
        }

        # Update label and buttons based on the current screen options
        for button, option in zip(self.buttons, self.options.get(self.current_screen, [])):
            button.setText(option)
            button.show()  # Ensure button is visible

    def buttonClicked(self):
        """Handles button click events and highlights the selected button."""
        sender = self.sender()  # Get the button that was clicked

        # Reset all buttons to the original style
        for button in self.buttons:
            button.setStyleSheet("font-size: 22px; padding: 20px; background-color: white; color: black;")

        # Highlight the selected button
        sender.setStyleSheet("font-size: 22px; padding: 20px; background-color: red; color: white;")
        self.selected_button_index = self.buttons.index(sender)  # Update the selected button index

        option_text = sender.text()
        if option_text == "Exit":
            self.close()  # Close the application
        elif option_text == "Return to Menu":
            self.current_screen = "main_menu"  # Go back to the main menu
            self.selected_button_index = None  # Reset selected button index
        else:
            # Logic to change the screen based on the button clicked
            print(f"Option '{option_text}' clicked")  # Placeholder print statement
        self.updateScreen()  # Refresh the screen to reflect any changes

    def checkButtonPress(self):
        """Checks if any of the hardware buttons have been pressed."""
        for i, pin in enumerate(self.button_pins):
            if GPIO.input(pin) == GPIO.LOW:  # Button press detected
                print(f"Hardware Button {i + 1} Pressed")  # Placeholder action
                # Simulate button click for corresponding button
                if self.buttons[i]:
                    self.buttons[i].click()
                time.sleep(0.3)  # Debounce delay

    def checkTTSButtonPress(self):
        """Checks if the TTS button has been pressed and reads options aloud."""
        if GPIO.input(self.tts_button_pin) == GPIO.LOW:
            options_text = ', '.join(self.options.get(self.current_screen, []))
            self.tts_engine.say(options_text)  # Say the options text
            self.tts_engine.runAndWait()  # Wait until speech is finished
            time.sleep(0.3)  # Debounce delay


def main():
    app = QApplication(sys.argv)
    window = MedicationDispenser()
    window.show()

    # Setup timers to periodically check for button presses
    timer = QTimer()
    timer.timeout.connect(window.checkButtonPress)
    timer.start(100)  # Check every 100 milliseconds

    tts_timer = QTimer()
    tts_timer.timeout.connect(window.checkTTSButtonPress)
    tts_timer.start(100)  # Check every 100 milliseconds

    sys.exit(app.exec_())


#if __name__ == "__main__":
main()
