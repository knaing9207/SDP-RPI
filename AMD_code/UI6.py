import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
import pyttsx3
from functools import partial
import RPi.GPIO as GPIO

class TextToSpeechManager:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        """Speaks the provided text."""
        self.engine.say(text)
        self.engine.runAndWait()

class ScreenManager:
    def __init__(self):
        self.screens = {
            "main_menu": ["Add Pill", "Pill Info", "Set Reminder", "Schedule Overview", "Emergency", "System Settings",
                          "Help", "Exit"],
            "Add Pill": ["Enter Pill Name", "Dosage", "Frequency", "Confirm", "Back"],
            "Pill Info": ["Search by Name", "View All", "Back"],
            "Set Reminder": ["Add New", "View Existing", "Back"],
            "Schedule Overview": ["Today", "This Week", "Back"],
            "Emergency": ["Contact Doctor", "Contact Pharmacy", "Back"],
            "System Settings": ["Volume Control", "Screen Brightness", "Back"],
        }

    def getOptionsForScreen(self, screen_name):
        """Returns the list of options for the specified screen."""
        return self.screens.get(screen_name, ["Back"])

class GPIOHandler(QObject):
    buttonPressed = pyqtSignal(int)

    def __init__(self, pins):
        super().__init__()
        self.pins = pins
        self.setupGPIO()

    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            try:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.gpioCallback, bouncetime=200)
            except ValueError:
                print("Pin is not valid")
                continue
            except RuntimeError as e:
                print("RUntime Error")
                continue


    def gpioCallback(self, pin):
        button_index = self.pins.index(pin)
        self.buttonPressed.emit(button_index)

class MedicationDispenserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medication Dispenser')
        self.setGeometry(0, 0, 800, 480)  # Set for 5-inch DSI display
        self.current_screen = "main_menu"
        self.screen_manager = ScreenManager()
        self.tts_manager = TextToSpeechManager()
        self.buttons = []
        self.setupUI()

        # Define GPIO pins for the buttons
        pins = [0,1,22,23,5,6,16,26]  # GPIO pins for buttons 1-8
        self.gpio_handler = GPIOHandler(pins)
        self.gpio_handler.buttonPressed.connect(self.handleButtonPress)

    def setupUI(self):
        self.layout = QVBoxLayout(self)

        self.button_layout = QHBoxLayout()
        self.left_button_layout = QVBoxLayout()
        self.right_button_layout = QVBoxLayout()

        self.button_layout.addLayout(self.left_button_layout)
        self.button_layout.addStretch()
        self.button_layout.addLayout(self.right_button_layout)
        self.layout.addLayout(self.button_layout)

        self.updateScreen(self.current_screen)

    def updateScreen(self, screen_name):
        for button in self.buttons:
            button.deleteLater()
        self.buttons.clear()

        self.current_screen = screen_name
        options = self.screen_manager.getOptionsForScreen(screen_name)

        # Add or remove options to ensure there are always 8 buttons (including placeholders)
        options += [""] * (8 - len(options))

        for i, option in enumerate(options):
            button = QPushButton(option)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    font-weight: bold;
                    background-color: #FFFF00;
                    color: #000000;
                    padding: 20px;
                }
                QPushButton:pressed {
                    background-color: #FF0000;
                    color: #FFFFFF;
                }
                QPushButton:disabled {
                    background-color: #F0F0F0;
                    color: #C0C0C0;
                }
            """)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if i < 4:
                self.left_button_layout.addWidget(button)
            else:
                self.right_button_layout.addWidget(button)

            if option:
                button.clicked.connect(partial(self.buttonAction, option))
            else:
                button.setDisabled(True)

            self.buttons.append(button)

    @pyqtSlot(int)
    def handleButtonPress(self, button_index):
        if 0 <= button_index < len(self.buttons) and self.buttons[button_index].isEnabled():
            self.buttonAction(self.buttons[button_index].text())

    def buttonAction(self, option):
        self.tts_manager.speak(option)
        if option in self.screen_manager.screens:
            self.updateScreen(option)
        elif option == "Back":
            self.updateScreen("main_menu")

    def closeEvent(self, event):
        GPIO.cleanup()  # Clean up GPIO when the window is closed
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = MedicationDispenserApp()
    window.show()
    sys.exit(app.exec_())

# if __name__ == "__main__":
main()
