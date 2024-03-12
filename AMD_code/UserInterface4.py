import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
import pyttsx3
from functools import partial


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
            "Help": ["User Guide", "FAQ", "Back"]
        }

    def getOptionsForScreen(self, screen_name):
        """Returns the list of options for the specified screen."""
        return self.screens.get(screen_name, ["Back"])


class MedicationDispenserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Medication Dispenser')
        self.setGeometry(0, 0, 800, 480)
        self.current_screen = "main_menu"
        self.screen_manager = ScreenManager()
        self.tts_manager = TextToSpeechManager()
        self.setupUI()

    def setupUI(self):
        self.layout = QVBoxLayout(self)

        self.button_layout = QHBoxLayout()
        self.left_button_layout = QVBoxLayout()
        self.right_button_layout = QVBoxLayout()
        self.button_layout.addLayout(self.left_button_layout)
        self.button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        self.button_layout.addLayout(self.right_button_layout)
        self.layout.addLayout(self.button_layout)

        self.updateScreen(self.current_screen)

    def updateScreen(self, screen_name):
        for layout in [self.left_button_layout, self.right_button_layout]:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        self.current_screen = screen_name
        options = self.screen_manager.getOptionsForScreen(screen_name)

        for i, option in enumerate(options):
            button = QPushButton(option)
            # Adjusting font size and padding to increase button size
            button.setStyleSheet("""
                QPushButton {
                    font-size: 30px; 
                    font-weight: bold; 
                    background-color: #FFFF00; 
                    color: #000000; 
                    padding: 30px; /* Increased padding */
                }
                QPushButton:pressed {
                    background-color: #FF0000; 
                    color: #FFFFFF;
                }
            """)
            button.clicked.connect(partial(self.buttonClicked, button, option))
            if i < 4:
                self.left_button_layout.addWidget(button)
            else:
                self.right_button_layout.addWidget(button)

    def buttonClicked(self, button, option):
        # The button's style for the pressed state is now handled within the style sheet.

        # Speak the option
        self.tts_manager.speak(option)

        # Change screen after speaking, if necessary
        if option == "Back":
            self.updateScreen("main_menu")
        elif option in self.screen_manager.screens:
            self.updateScreen(option)


def main():
    app = QApplication(sys.argv)
    window = MedicationDispenserApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()