import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, 
                             QProgressBar, QMessageBox, QCheckBox)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class APIThread(QThread):
    update_progress = pyqtSignal(int)
    update_output = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, prompt, api_key):
        super().__init__()
        self.prompt = prompt
        self.api_key = api_key

    def run(self):
        # Simulating API call
        import time
        for i in range(101):
            time.sleep(0.05)
            self.update_progress.emit(i)
            if i % 10 == 0:
                self.update_output.emit(f"Processing: {i}% complete")
        
        # Simulated API response
        response = "This is a simulated API response."
        self.finished.emit(True, response)

class PromptRunner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_config()

    def initUI(self):
        self.setWindowTitle("Enhanced Prompt Runner")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Title Input
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter a title for your prompt")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        main_layout.addLayout(title_layout)

        # Prompt Input
        prompt_label = QLabel("Prompt:")
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        self.char_count = QLabel("Characters: 0")
        self.prompt_input.textChanged.connect(self.update_char_count)
        main_layout.addWidget(prompt_label)
        main_layout.addWidget(self.prompt_input)
        main_layout.addWidget(self.char_count)

        # Folder Configuration
        folder_layout = QVBoxLayout()
        self.prompts_folder = self.create_folder_input("Prompts Folder")
        self.outputs_folder = self.create_folder_input("Outputs Folder")
        self.config_path = self.create_folder_input("Configuration Save Path")
        folder_layout.addLayout(self.prompts_folder)
        folder_layout.addLayout(self.outputs_folder)
        folder_layout.addLayout(self.config_path)
        main_layout.addLayout(folder_layout)

        # API Key Management
        api_layout = QHBoxLayout()
        api_label = QLabel("OpenAI API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.show_key = QCheckBox("Show")
        self.show_key.stateChanged.connect(self.toggle_api_key_visibility)
        test_api_button = QPushButton("Test API Key")
        test_api_button.clicked.connect(self.test_api_key)
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_key_input)
        api_layout.addWidget(self.show_key)
        api_layout.addWidget(test_api_button)
        main_layout.addLayout(api_layout)

        # Run Button
        self.run_button = QPushButton("Run Prompt")
        self.run_button.clicked.connect(self.run_prompt)
        main_layout.addWidget(self.run_button)

        # Progress Bar
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        # Terminal Output
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFont(QFont("Courier"))
        main_layout.addWidget(self.terminal_output)

        # Dark Mode Toggle
        self.dark_mode_toggle = QCheckBox("Dark Mode")
        self.dark_mode_toggle.stateChanged.connect(self.toggle_dark_mode)
        main_layout.addWidget(self.dark_mode_toggle)

    def create_folder_input(self, label):
        layout = QHBoxLayout()
        label_widget = QLabel(f"{label}:")
        input_widget = QLineEdit()
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.browse_folder(input_widget))
        layout.addWidget(label_widget)
        layout.addWidget(input_widget)
        layout.addWidget(browse_button)
        return layout

    def browse_folder(self, input_widget):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            input_widget.setText(folder)

    def update_char_count(self):
        count = len(self.prompt_input.toPlainText())
        self.char_count.setText(f"Characters: {count}")

    def toggle_api_key_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)

    def test_api_key(self):
        api_key = self.api_key_input.text()
        if api_key:
            QMessageBox.information(self, "API Key Test", "API key is valid (simulated)")
        else:
            QMessageBox.warning(self, "API Key Test", "Please enter an API key")

    def run_prompt(self):
        prompt = self.prompt_input.toPlainText()
        api_key = self.api_key_input.text()
        
        if not prompt or not api_key:
            QMessageBox.warning(self, "Input Error", "Please enter both a prompt and an API key")
            return

        self.run_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.terminal_output.clear()

        self.api_thread = APIThread(prompt, api_key)
        self.api_thread.update_progress.connect(self.update_progress)
        self.api_thread.update_output.connect(self.update_terminal)
        self.api_thread.finished.connect(self.api_call_finished)
        self.api_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_terminal(self, message):
        self.terminal_output.append(message)

    def api_call_finished(self, success, response):
        self.run_button.setEnabled(True)
        if success:
            self.save_output(response)
            self.terminal_output.append("API call completed successfully")
            self.prompt_input.clear()
        else:
            self.terminal_output.append("API call failed")

    def save_output(self, response):
        title = self.title_input.text() or "untitled"
        prompts_folder = self.prompts_folder.itemAt(1).widget().text()
        outputs_folder = self.outputs_folder.itemAt(1).widget().text()

        if not os.path.exists(prompts_folder):
            os.makedirs(prompts_folder)
        if not os.path.exists(outputs_folder):
            os.makedirs(outputs_folder)

        prompt_file = os.path.join(prompts_folder, f"{title}.txt")
        output_file = os.path.join(outputs_folder, f"{title}_output.txt")

        with open(prompt_file, 'w') as f:
            f.write(self.prompt_input.toPlainText())

        with open(output_file, 'w') as f:
            f.write(response)

        self.terminal_output.append(f"Prompt saved to: {prompt_file}")
        self.terminal_output.append(f"Output saved to: {output_file}")

    def toggle_dark_mode(self, state):
        if state == Qt.CheckState.Checked.value:
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: #ffffff; }
                QLineEdit, QTextEdit { background-color: #3b3b3b; border: 1px solid #5b5b5b; }
                QPushButton { background-color: #4b4b4b; border: 1px solid #5b5b5b; }
                QPushButton:hover { background-color: #5b5b5b; }
            """)
        else:
            self.setStyleSheet("")

    def load_config(self):
        config_path = self.config_path.itemAt(1).widget().text()
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.prompts_folder.itemAt(1).widget().setText(config.get('prompts_folder', ''))
            self.outputs_folder.itemAt(1).widget().setText(config.get('outputs_folder', ''))
            self.api_key_input.setText(config.get('api_key', ''))
            self.dark_mode_toggle.setChecked(config.get('dark_mode', False))

    def save_config(self):
        config = {
            'prompts_folder': self.prompts_folder.itemAt(1).widget().text(),
            'outputs_folder': self.outputs_folder.itemAt(1).widget().text(),
            'api_key': self.api_key_input.text(),
            'dark_mode': self.dark_mode_toggle.isChecked()
        }
        config_path = self.config_path.itemAt(1).widget().text()
        with open(config_path, 'w') as f:
            json.dump(config, f)

    def closeEvent(self, event):
        self.save_config()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PromptRunner()
    ex.show()
    sys.exit(app.exec())