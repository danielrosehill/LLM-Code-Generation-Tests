# Model 

Meta Llama 3.1 70B-Instruct

# Access UI / Platform

[Hugging Chat](https://huggingface.co/chat) by Hugging Face

# Date

02-10-24 (Oct)

# Prompt

## Python GUI Application: Enhanced Prompt Runner

Create a robust and user-friendly Python GUI application with the following features and functionality:

### User Interface Elements

1. **Prompt Input**:
   - Multi-line text field for entering prompt text
   - Placeholder text: "Enter your prompt here..."
   - Character count display below the field

2. **Title Input**:
   - Single-line text field for prompt title
   - Placeholder text: "Enter a title for your prompt"

3. **Folder Configuration**:
   - Input fields with "Browse" buttons for:
     - Prompts storage folder
     - Outputs storage folder
     - **Configuration save path**
   - Tooltips explaining the purpose of each folder

4. **API Key Management**:
   - Field for entering OpenAI API key
   - "Test API Key" button for validation
   - Toggle to show/hide the API key

5. **Run Button**:
   - Prominent "Run Prompt" button
   - Loading animation during processing

6. **Terminal Output**:
   - Scrollable area for job progress and messages
   - Monospaced font for readability

### Visual Design

1. Modern, flat design with a cohesive color scheme
2. Proper spacing and alignment of UI elements
3. Subtle animations for button hovers and transitions
4. Appropriate icons (e.g., folder icon for browse buttons)
5. Custom logo displayed in the header
6. Visually appealing font for labels and headers

### Core Functionality

1. **Settings Persistence**:
   - Store and retrieve user settings between sessions
   - "Reset to Default" option for all settings
   - **Allow user to specify the configuration save path**

2. **Prompt Execution**:
   - Send prompt to OpenAI API using provided key
   - Display progress and status updates
   - Show progress bar during API calls

3. **File Operations**:
   - Save prompt and API output to respective folders
   - Implement file overwrite confirmation dialog

4. **UI Updates**:
   - Clear prompt input after execution
   - Display success message upon completion
   - Real-time character count update

### Additional Features

1. Comprehensive error handling with user-friendly messages
2. Responsive UI during API calls using threading
3. Input validation for all fields
4. Help menu with tooltips and user guide
5. Dark mode toggle

### Helper Text

Provide informative text throughout the application:
1. Brief explanations next to input fields
2. Tooltips for buttons and complex features
3. Status messages in the terminal output
4. Pop-up hints for first-time users
5. Contextual help for error messages

## Implementation Guidelines

1. Use a modern Python GUI framework (e.g., PyQt6 or wxPython)
2. Follow PEP 8 style guidelines
3. Include explanatory comments for complex logic
4. Implement modular, object-oriented design
5. Ensure cross-platform compatibility (Windows, macOS, Linux)

## Validation Checklist

Before submitting the code:
1. Verify all specified features are implemented
2. Ensure code compiles without errors
3. Check for proper error handling and edge cases
4. Confirm intuitive and user-friendly GUI layout
5. Validate adherence to Python best practices and PEP 8
6. Test application responsiveness and performance
7. Verify helper text and tooltips are informative and correctly displayed
8. **Confirm that the user can specify and use a custom configuration save path**

Provide the complete, executable Python code for this GUI application, including necessary import statements and brief usage instructions. Also, include a requirements.txt file listing all required dependencies.