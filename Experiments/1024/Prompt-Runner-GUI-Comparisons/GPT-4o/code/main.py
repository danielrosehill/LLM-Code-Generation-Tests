import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel,
    QPushButton, QFileDialog, QHBoxLayout, QCheckBox, QProgressBar,
    QMessageBox
)
from PyQt6.QtGui import QFont

class PromptRunnerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Enhanced Prompt Runner')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()

        # Title Input
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter a title for your prompt")
        layout.addWidget(QLabel("Prompt Title:"))
        layout.addWidget(self.title_input)

        # Prompt Input
        self.prompt_input = QTextEdit(self)
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        layout.addWidget(QLabel("Prompt Text:"))
        layout.addWidget(self.prompt_input)

        # Character Count
        self.char_count_label = QLabel("Character Count: 0", self)
        layout.addWidget(self.char_count_label)
        
        # Connect text change signal to character count update
        self.prompt_input.textChanged.connect(self.updateCharCount)

        # Folder Configuration
        folder_layout = QHBoxLayout()
        
        self.prompt_folder_btn = QPushButton('Browse Prompts Folder', self)
        self.output_folder_btn = QPushButton('Browse Outputs Folder', self)
        
        folder_layout.addWidget(self.prompt_folder_btn)
        folder_layout.addWidget(self.output_folder_btn)

        layout.addLayout(folder_layout)

        # API Key Management
        api_layout = QHBoxLayout()
        
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        api_layout.addWidget(QLabel("API Key:"))
        api_layout.addWidget(self.api_key_input)

        self.test_api_btn = QPushButton('Test API Key', self)
        
        api_layout.addWidget(self.test_api_btn)

        layout.addLayout(api_layout)

        # Run Button
        self.run_button = QPushButton('Run Prompt', self)
        
        layout.addWidget(self.run_button)

        # Terminal Output
        self.terminal_output = QTextEdit(self)
        
        self.terminal_output.setReadOnly(True)
        
        layout.addWidget(QLabel("Terminal Output:"))
        
        layout.addWidget(self.terminal_output)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        
        layout.addWidget(self.progress_bar)

        # Set main layout
        self.setLayout(layout)

    def updateCharCount(self):
        text_length = len(self.prompt_input.toPlainText())
        
        self.char_count_label.setText(f"Character Count: {text_length}")

def main():
    app = QApplication(sys.argv)
    window = PromptRunnerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
