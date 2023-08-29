import os
import sys
import json
import subprocess
import pyperclip
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QFormLayout
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

def install_dependencies():
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install dependencies.")

# Load JSON data
with open("gun_ids.json", "r", encoding="utf-8") as gun_file:
    gun_ids = json.load(gun_file)

with open("skin_ids.json", "r", encoding="utf-8") as skin_file:
    skin_ids = json.load(skin_file)

with open("rarity_ids.json", "r", encoding="utf-8") as rarity_file:
    rarity_ids = json.load(rarity_file)

class SkinGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS:GO Skin Generator by Mecke_Dev")

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        self.setFixedWidth(400)
        layout = QVBoxLayout()

        self.gun_search_entry = QLineEdit(self)
        self.gun_combobox = QComboBox(self)
        self.gun_combobox.addItems(gun_ids.values())
        self.gun_search_entry.textChanged.connect(self.update_gun_completion_list)
        
        layout.addWidget(QLabel("Select Gun:"))
        layout.addWidget(self.gun_search_entry)
        layout.addWidget(self.gun_combobox)

        self.skin_search_entry = QLineEdit(self)
        self.skin_combobox = QComboBox(self)
        self.skin_combobox.addItems(skin_ids.values())
        self.skin_search_entry.textChanged.connect(self.update_skin_completion_list)

        layout.addWidget(QLabel("Select Skin:"))
        layout.addWidget(self.skin_search_entry)
        layout.addWidget(self.skin_combobox)

        self.rarity_search_entry = QLineEdit(self)
        self.rarity_combobox = QComboBox(self)
        self.rarity_combobox.addItems(rarity_ids.values())
        self.rarity_search_entry.textChanged.connect(self.update_rarity_completion_list)

        layout.addWidget(QLabel("Select Rarity:"))
        layout.addWidget(self.rarity_search_entry)
        layout.addWidget(self.rarity_combobox)

        self.pattern_entry = QLineEdit(self)
        self.pattern_entry.setText("1")
        layout.addWidget(QLabel("Pattern:"))
        layout.addWidget(self.pattern_entry)

        paint_wear_layout = QVBoxLayout()
        paint_wear_label = QLabel("Float:")

        self.paint_wear_entry = QLineEdit()
        self.paint_wear_entry.setFixedWidth(300)
        self.paint_wear_entry.setMaxLength(16)
        
        paint_wear_layout.addWidget(paint_wear_label)
        paint_wear_layout.addWidget(self.paint_wear_entry)
        

        layout.addLayout(paint_wear_layout)

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        generate_button = QPushButton("Generate", self)
        generate_button.clicked.connect(self.generate_inspect)
        layout.addWidget(generate_button)

        copy_button = QPushButton("Copy to Clipboard", self)
        copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(copy_button)

        # Create clickable link labels
        link_label_mecke = QLabel('<a href="https://steamcommunity.com/id/mecke_dev/">Visit me on Steam</a> <a href="https://github.com/dr3fty/cs2-inspect-gen">Credits to dr3fty</a></div>')
        link_label_mecke.setOpenExternalLinks(True)  # This makes the link open in the default web browser
        layout.addWidget(link_label_mecke)


        main_widget.setLayout(layout)

    def generate_inspect(self):
        gun_name = self.gun_combobox.currentText()
        skin_name = self.skin_combobox.currentText()
        rarity_name = self.rarity_combobox.currentText()
        pattern = self.pattern_entry.text()
        paint_wear = self.paint_wear_entry.text()

        gun_id = next((key for key, value in gun_ids.items() if value == gun_name), None)
        skin_id = next((key for key, value in skin_ids.items() if value == skin_name), None)
        rarity_id = next((key for key, value in rarity_ids.items() if value == rarity_name), None)

        command = [
            "python", "convert-gen.py",
            "genrarity", rarity_id, gun_id, skin_id, pattern, str(paint_wear)
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        self.result_text.setPlainText(result.stdout)
        pyperclip.copy(result.stdout)

    def copy_to_clipboard(self):
        result = self.result_text.toPlainText()
        pyperclip.copy(result)

    def update_gun_completion_list(self, search_query):
        filtered_items = [item for item in gun_ids.values() if search_query.lower() in item.lower()]
        self.gun_combobox.clear()
        self.gun_combobox.addItems(filtered_items)

    def update_skin_completion_list(self, search_query):
        filtered_items = [item for item in skin_ids.values() if search_query.lower() in item.lower()]
        self.skin_combobox.clear()
        self.skin_combobox.addItems(filtered_items)

    def update_rarity_completion_list(self, search_query):
        filtered_items = [item for item in rarity_ids.values() if search_query.lower() in item.lower()]
        self.rarity_combobox.clear()
        self.rarity_combobox.addItems(filtered_items)

if __name__ == "__main__":
    # Check if a file marker exists indicating dependencies are already installed
    if not os.path.exists("dependencies_installed.marker"):
        install_dependencies()
        # Create a marker file to avoid repeated installation
        with open("dependencies_installed.marker", "w") as marker_file:
            marker_file.write("Dependencies installed")

    app = QApplication(sys.argv)
    window = SkinGeneratorApp()
    window.show()
    sys.exit(app.exec_())
