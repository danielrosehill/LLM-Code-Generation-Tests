import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QScrollArea, QTextBrowser, QCheckBox, QComboBox, QMenu, QMenuBar, QAction, QInputDialog
from PyQt6.QtGui import QFont, QPalette, QColor, QContextMenuEvent, QCloseEvent
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
import os
import json
import requests
import threading
from datetime import datetime

class PromptRunner(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enhanced Prompt Runner")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_widgets()
        self.layout_widgets()

        self.config = self.load_config()
        self.set_config_defaults()

        self.thread = QThread()
        self.thread.started.connect(self.run_prompt)

    def create_widgets(self):
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        self.prompt_input.setFixedHeight(200)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter a title for your prompt")

        self.folder_config_layout = QGridLayout()
        self.prompts_folder_input = QLineEdit()
        self.prompts_folder_browse_button = QPushButton("Browse")
        self.prompts_folder_browse_button.clicked.connect(self.browse_prompts_folder)
        self.outputs_folder_input = QLineEdit()
        self.outputs_folder_browse_button = QPushButton("Browse")
        self.outputs_folder_browse_button.clicked.connect(self.browse_outputs_folder)
        self.config_save_path_input = QLineEdit()
        self.config_save_path_browse_button = QPushButton("Browse")
        self.config_save_path_browse_button.clicked.connect(self.browse_config_save_path)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_toggle = QCheckBox()
        self.api_key_toggle.stateChanged.connect(self.toggle_api_key_visibility)
        self.api_key_test_button = QPushButton("Test API Key")
        self.api_key_test_button.clicked.connect(self.test_api_key)

        self.run_button = QPushButton("Run Prompt")
        self.run_button.clicked.connect(self.start_thread)

        self.terminal_output = QTextBrowser()
        self.terminal_output.setFixedHeight(200)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.menu_bar = QMenuBar()
        self.help_menu = QMenu("Help")
        self.about_action = QAction("About")
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)
        self.menu_bar.addMenu(self.help_menu)

    def layout_widgets(self):
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.prompt_input)

        self.folder_config_layout.addWidget(QLabel("Prompts Folder:"), 0, 0)
        self.folder_config_layout.addWidget(self.prompts_folder_input, 0, 1)
        self.folder_config_layout.addWidget(self.prompts_folder_browse_button, 0, 2)
        self.folder_config_layout.addWidget(QLabel("Outputs Folder:"), 1, 0)
        self.folder_config_layout.addWidget(self.outputs_folder_input, 1, 1)
        self.folder_config_layout.addWidget(self.outputs_folder_browse_button, 1, 2)
        self.folder_config_layout.addWidget(QLabel("Config Save Path:"), 2, 0)
        self.folder_config_layout.addWidget(self.config_save_path_input, 2, 1)
        self.folder_config_layout.addWidget(self.config_save_path_browse_button, 2, 2)

        self.layout.addLayout(self.folder_config_layout)

        self.layout.addWidget(self.api_key_input)
        self.layout.addWidget(self.api_key_toggle)
        self.layout.addWidget(self.api_key_test_button)

        self.layout.addWidget(self.run_button)

        self.layout.addWidget(self.terminal_output)

        self.layout.addWidget(self.progress_bar)

        self.layout.setMenuBar(self.menu_bar)

    def browse_prompts_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Prompts Folder")
        self.prompts_folder_input.setText(folder_path)

    def browse_outputs_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Outputs Folder")
        self.outputs_folder_input.setText(folder_path)

    def browse_config_save_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Config Save Path")
        self.config_save_path_input.setText(folder_path)

    def toggle_api_key_visibility(self):
        if self.api_key_toggle.isChecked():
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)

    def test_api_key(self):
        api_key = self.api_key_input.text()
        try:
            response = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {api_key}"})
            if response.status_code == 200:
                self.terminal_output.append("API Key is valid!")
            else:
                self.terminal_output.append("API Key is invalid!")
        except requests.exceptions.RequestException as e:
            self.terminal_output.append(f"Error: {e}")

    def start_thread(self):
        self.thread.start()

    @pyqtSlot()
    def run_prompt(self):
        prompt_text = self.prompt_input.toPlainText()
        title = self.title_input.text()
        prompts_folder = self.prompts_folder_input.text()
        outputs_folder = self.outputs_folder_input.text()
        config_save_path = self.config_save_path_input.text()
        api_key = self.api_key_input.text()

        self.terminal_output.append("Running prompt...")

        try:
            response = requests.post("https://api.openai.com/v1/completions", headers={"Authorization": f"Bearer {api_key}"}, json={"prompt": prompt_text, "max_tokens": 2048})
            response.raise_for_status()
            output = response.json()["choices"][0]["text"]
            with open(os.path.join(outputs_folder, f"{title}.txt"), "w") as f:
                f.write(output)
            self.terminal_output.append("Output saved!")
        except requests.exceptions.RequestException as e:
            self.terminal_output.append(f"Error: {e}")

        self.terminal_output.append("Prompt completed!")

    def load_config(self):
        config_path = os.path.join(os.path.expanduser("~"), ".prompt_runner_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        else:
            return {}

    def set_config_defaults(self):
        if not self.config:
            self.config = {
                "prompts_folder": os.path.join(os.path.expanduser("~"), "Documents", "Prompts"),
                "outputs_folder": os.path.join(os.path.expanduser("~"), "Documents", "Outputs"),
                "config_save_path": os.path.join(os.path.expanduser("~"), ".prompt_runner_config.json"),
                "api_key": ""
            }
            with open(os.path.join(os.path.expanduser("~"), ".prompt_runner_config.json"), "w") as f:
                json.dump(self.config, f)

    def show_about(self):
        about_text = "Enhanced Prompt Runner\n\n Developed by [Your Name]"
        QInputDialog.show(self, "About", about_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    runner = PromptRunner()
    runner.show()
    sys.exit(app.exec())