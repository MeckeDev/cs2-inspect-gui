import os
import sys
import json
import subprocess
import pyperclip
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QFormLayout
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

with open("sticker_ids.json", "r", encoding="utf-8") as sticker_file:
    sticker_ids = json.load(sticker_file)

class SkinGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS:GO Skin Generator by Mecke_Dev")

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        self.setFixedWidth(600)
        self.setFixedHeight(1000)
        layout = QVBoxLayout()

        nametag_layout = QHBoxLayout()
        self.nametag_entry = QLineEdit()
        self.nametag_entry.setMaxLength(123)


        layout.addWidget(QLabel("Nametag:"))
        nametag_layout.addWidget(self.nametag_entry)

        layout.addLayout(nametag_layout)

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

        stattrak_count_layout = QHBoxLayout()
        self.stattrak_count_check = QCheckBox("StatTrak", self)
        self.stattrak_count_entry = QLineEdit()
        self.stattrak_count_entry.setFixedWidth(500)

        stattrak_count_layout.addWidget(self.stattrak_count_check)
        stattrak_count_layout.addWidget(self.stattrak_count_entry)

        layout.addLayout(stattrak_count_layout)

        paint_wear_layout = QHBoxLayout()
        paint_wear_label = QLabel("Float:")
        self.paint_wear_entry = QLineEdit()
        self.paint_wear_entry.setFixedWidth(500)

        paint_wear_layout.addWidget(paint_wear_label)
        paint_wear_layout.addWidget(self.paint_wear_entry)

        layout.addLayout(paint_wear_layout)

        # Add Sticker 4 elements
        self.sticker4_search_entry = QLineEdit(self)
        self.sticker4_combobox = QComboBox(self)
        self.sticker4_combobox.addItems(sticker_ids.values())
        self.sticker4_search_entry.textChanged.connect(self.update_sticker4_completion_list)

        layout.addWidget(QLabel("Sticker 1:"))
        layout.addWidget(self.sticker4_search_entry)
        layout.addWidget(self.sticker4_combobox)

        sticker4_slider_layout = QHBoxLayout()
        sticker4_slider_label = QLabel("Sticker 1 Wear:")
        self.sticker4_slider = QSlider(Qt.Horizontal)
        self.sticker4_slider.setRange(0, 100)  # Range from 0 to 100 (0 - 1 in 0.01 steps)
        self.sticker4_slider.setValue(0)  # Set default value to 0
        self.sticker4_slider.setSingleStep(1)  # Step of 1

        self.sticker4_slider_entry = QLineEdit()
        self.sticker4_slider_entry.setFixedWidth(100)  # Adjust the width as needed

        sticker4_slider_layout.addWidget(sticker4_slider_label)
        sticker4_slider_layout.addWidget(self.sticker4_slider)
        sticker4_slider_layout.addWidget(self.sticker4_slider_entry)

        layout.addLayout(sticker4_slider_layout)

        # Connect the slider's valueChanged signal to update the input box
        self.sticker4_slider.valueChanged.connect(self.update_slider4_input_box)

        

        # Add Sticker 3 elements
        self.sticker3_search_entry = QLineEdit(self)
        self.sticker3_combobox = QComboBox(self)
        self.sticker3_combobox.addItems(sticker_ids.values())
        self.sticker3_search_entry.textChanged.connect(self.update_sticker3_completion_list)

        layout.addWidget(QLabel("Sticker 2:"))
        layout.addWidget(self.sticker3_search_entry)
        layout.addWidget(self.sticker3_combobox)

        sticker3_slider_layout = QHBoxLayout()
        sticker3_slider_label = QLabel("Sticker 2 Wear:")
        self.sticker3_slider = QSlider(Qt.Horizontal)
        self.sticker3_slider.setRange(0, 100)  # Range from 0 to 100 (0 - 1 in 0.01 steps)
        self.sticker3_slider.setValue(0)  # Set default value to 0
        self.sticker3_slider.setSingleStep(1)  # Step of 1

        self.sticker3_slider_entry = QLineEdit()
        self.sticker3_slider_entry.setFixedWidth(100)  # Adjust the width as needed

        sticker3_slider_layout.addWidget(sticker3_slider_label)
        sticker3_slider_layout.addWidget(self.sticker3_slider)
        sticker3_slider_layout.addWidget(self.sticker3_slider_entry)

        layout.addLayout(sticker3_slider_layout)

        # Connect the slider's valueChanged signal to update the input box
        self.sticker3_slider.valueChanged.connect(self.update_slider3_input_box)

        # Add Sticker 2 elements
        self.sticker2_search_entry = QLineEdit(self)
        self.sticker2_combobox = QComboBox(self)
        self.sticker2_combobox.addItems(sticker_ids.values())
        self.sticker2_search_entry.textChanged.connect(self.update_sticker2_completion_list)

        layout.addWidget(QLabel("Sticker 3:"))
        layout.addWidget(self.sticker2_search_entry)
        layout.addWidget(self.sticker2_combobox)

        sticker2_slider_layout = QHBoxLayout()
        sticker2_slider_label = QLabel("Sticker 3 Wear:")
        self.sticker2_slider = QSlider(Qt.Horizontal)
        self.sticker2_slider.setRange(0, 100)  # Range from 0 to 100 (0 - 1 in 0.01 steps)
        self.sticker2_slider.setValue(0)  # Set default value to 0
        self.sticker2_slider.setSingleStep(1)  # Step of 1

        self.sticker2_slider_entry = QLineEdit()
        self.sticker2_slider_entry.setFixedWidth(100)  # Adjust the width as needed

        sticker2_slider_layout.addWidget(sticker2_slider_label)
        sticker2_slider_layout.addWidget(self.sticker2_slider)
        sticker2_slider_layout.addWidget(self.sticker2_slider_entry)

        layout.addLayout(sticker2_slider_layout)

        # Connect the slider's valueChanged signal to update the input box
        self.sticker2_slider.valueChanged.connect(self.update_slider2_input_box)

        # Add Sticker 1 elements
        self.sticker1_search_entry = QLineEdit(self)
        self.sticker1_combobox = QComboBox(self)
        self.sticker1_combobox.addItems(sticker_ids.values())
        self.sticker1_search_entry.textChanged.connect(self.update_sticker1_completion_list)

        layout.addWidget(QLabel("Sticker 4:"))
        layout.addWidget(self.sticker1_search_entry)
        layout.addWidget(self.sticker1_combobox)

        sticker1_slider_layout = QHBoxLayout()
        sticker1_slider_label = QLabel("Sticker 4 Wear:")
        self.sticker1_slider = QSlider(Qt.Horizontal)
        self.sticker1_slider.setRange(0, 100)  # Range from 0 to 100 (0 - 1 in 0.01 steps)
        self.sticker1_slider.setValue(0)  # Set default value to 0
        self.sticker1_slider.setSingleStep(1)  # Step of 1

        self.sticker1_slider_entry = QLineEdit()
        self.sticker1_slider_entry.setFixedWidth(100)  # Adjust the width as needed

        sticker1_slider_layout.addWidget(sticker1_slider_label)
        sticker1_slider_layout.addWidget(self.sticker1_slider)
        sticker1_slider_layout.addWidget(self.sticker1_slider_entry)

        layout.addLayout(sticker1_slider_layout)

        # Connect the slider's valueChanged signal to update the input box
        self.sticker1_slider.valueChanged.connect(self.update_slider1_input_box)

        self.result1_text = QTextEdit(self)
        self.result1_text.setReadOnly(True)
        self.result1_text.setFixedHeight(50)
        layout.addWidget(self.result1_text)

        self.result2_text = QTextEdit(self)
        self.result2_text.setReadOnly(True)
        self.result2_text.setFixedHeight(50)
        layout.addWidget(self.result2_text)

        self.result3_text = QTextEdit(self)
        self.result3_text.setReadOnly(True)
        self.result3_text.setFixedHeight(50)
        layout.addWidget(self.result3_text)

        generate_button = QPushButton("Generate", self)
        generate_button.clicked.connect(self.generate_inspect)
        layout.addWidget(generate_button)

        copy_button = QPushButton("Copy Command to Clipboard", self)
        copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(copy_button)

        copy_url_button = QPushButton("Copy URL to Clipboard", self)
        copy_url_button.clicked.connect(self.copy_url_to_clipboard)
        layout.addWidget(copy_url_button)

        copy_gen_button = QPushButton("Copy Gen to Clipboard", self)
        copy_gen_button.clicked.connect(self.copy_gen_to_clipboard)
        layout.addWidget(copy_gen_button)

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
        sticker1_name = self.sticker1_combobox.currentText()
        sticker2_name = self.sticker2_combobox.currentText()
        sticker3_name = self.sticker3_combobox.currentText()
        sticker4_name = self.sticker4_combobox.currentText()
        sticker1_wear = ""
        sticker2_wear = ""
        sticker3_wear = ""
        sticker4_wear = ""
        stattrak = "1"
        stattrak_count = "0"
        nametag = self.nametag_entry.text()

        if self.stattrak_count_check.checkState() == 2:
            stattrak = "0"
            stattrak_count = self.stattrak_count_entry.text()

        gun_id = next((key for key, value in gun_ids.items() if value == gun_name), None)
        skin_id = next((key for key, value in skin_ids.items() if value == skin_name), None)
        rarity_id = next((key for key, value in rarity_ids.items() if value == rarity_name), None)
        sticker1_id = next((key for key, value in sticker_ids.items() if value == sticker1_name), None)
        sticker2_id = next((key for key, value in sticker_ids.items() if value == sticker2_name), None)
        sticker3_id = next((key for key, value in sticker_ids.items() if value == sticker3_name), None)
        sticker4_id = next((key for key, value in sticker_ids.items() if value == sticker4_name), None)
                
        if sticker1_id != "":
            sticker1_wear = self.sticker1_slider.value() / 100.0   
     
        if sticker2_id != "":
            sticker2_wear = self.sticker2_slider.value() / 100.0
                
        if sticker3_id != "":
            sticker3_wear = self.sticker3_slider.value() / 100.0
                
        if sticker4_id != "":
            sticker4_wear = self.sticker4_slider.value() / 100.0

        print(rarity_id, gun_id, skin_id, pattern, str(paint_wear), sticker1_id, sticker1_wear, sticker2_id, sticker2_wear, sticker3_id, sticker3_wear, sticker4_id, sticker4_wear)

        command = [
            "python", "convert-gen.py",
            "genrarity", rarity_id, gun_id, skin_id, pattern, str(paint_wear), sticker1_id, str(sticker1_wear), sticker2_id, str(sticker2_wear), sticker3_id, str(sticker3_wear), sticker4_id, str(sticker4_wear), stattrak, stattrak_count, nametag
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        print("OUT: ", result.stdout)
        command, link, gen = result.stdout.split(" : ")
        self.command = command
        self.link = link
        self.gen = gen

        self.result1_text.setPlainText(self.command)        
        
        self.result2_text.setPlainText(self.link)        
        
        self.result3_text.setPlainText(self.gen)

    def copy_to_clipboard(self):
        result = self.command
        pyperclip.copy(result)
        
    def copy_url_to_clipboard(self):
        result = self.link
        pyperclip.copy(result)
        
    def copy_gen_to_clipboard(self):
        result = self.gen
        pyperclip.copy(result)

    def open_link(self):
        url = QUrl("https://steamcommunity.com/id/mecke_dev/")
        QDesktopServices.openUrl(url)

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

    def update_slider1_input_box(self, value):
        self.sticker1_slider_entry.setText(str(value / 100)) 

    def update_slider2_input_box(self, value):
        self.sticker2_slider_entry.setText(str(value / 100)) 

    def update_slider3_input_box(self, value):
        self.sticker3_slider_entry.setText(str(value / 100)) 

    def update_slider4_input_box(self, value):
        self.sticker4_slider_entry.setText(str(value / 100)) 

    def update_sticker1_completion_list(self, search_query):
        filtered_items = [item for item in sticker_ids.values() if search_query.lower() in item.lower()]
        self.sticker1_combobox.clear()
        self.sticker1_combobox.addItems(filtered_items)

    def update_sticker2_completion_list(self, search_query):
        filtered_items = [item for item in sticker_ids.values() if search_query.lower() in item.lower()]
        self.sticker2_combobox.clear()
        self.sticker2_combobox.addItems(filtered_items)

    def update_sticker3_completion_list(self, search_query):
        filtered_items = [item for item in sticker_ids.values() if search_query.lower() in item.lower()]
        self.sticker3_combobox.clear()
        self.sticker3_combobox.addItems(filtered_items)

    def update_sticker4_completion_list(self, search_query):
        filtered_items = [item for item in sticker_ids.values() if search_query.lower() in item.lower()]
        self.sticker4_combobox.clear()
        self.sticker4_combobox.addItems(filtered_items)

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
