import sys
import subprocess
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QTextEdit,
    QLabel, QWidget, QProgressBar, QHBoxLayout, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QDropEvent, QDragEnterEvent

# Selection window -----------------------------------------------------------------------------------------------------

class InitialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RACQUET")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel("Choose how you want to proceed:", self)

        self.button_group = QButtonGroup(self)
        self.option_a = QRadioButton("Deal with individual requirements", self)
        self.option_b = QRadioButton("Drag and drop whole files", self)
        self.button_group.addButton(self.option_a)
        self.button_group.addButton(self.option_b)

        self.proceed_button = QPushButton("Proceed", self)
        self.proceed_button.clicked.connect(self.proceed)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.option_a)
        self.layout.addWidget(self.option_b)
        self.layout.addWidget(self.proceed_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def proceed(self):
        if self.option_a.isChecked():
            self.main_window = MainWindow()
        elif self.option_b.isChecked():
            self.main_window = FileDropWindow()
        else:
            return

        self.main_window.show()
        self.close()

# Individual -----------------------------------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RACQUET")
        self.setGeometry(100, 100, 600, 600)

        self.layout = QVBoxLayout()

        # Direct the user to input text
        self.intro_label = QLabel("Please paste your requirement text into the following text box and then press submit.", self)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter requirement text here")

        self.submit_button_cpm = QPushButton("Submit to CPM", self)
        self.submit_button_cpm.clicked.connect(self.process_input_cpm)
        self.submit_button_ai_EARS = QPushButton("Submit to EARS AI Module", self)
        self.submit_button_ai_EARS.clicked.connect(self.process_input_ai_EARS)
        self.submit_button_ai_ECSS = QPushButton("Submit to ECSS AI Module", self)
        self.submit_button_ai_ECSS.clicked.connect(self.process_input_ai_ECSS)
        #self.submit_button_ai_ISO29148 = QPushButton("Submit to ISO 29148 AI Module", self)
        #self.submit_button_ai_ISO29148.clicked.connect(self.process_input_ai_ISO29148)

        self.loading_bar = QProgressBar(self)
        self.loading_bar.setRange(0, 0)  # Indeterminate state
        self.loading_bar.setVisible(False)

        self.result1_text = QTextEdit(self)
        self.result1_text.setReadOnly(True)
        self.result1_text.setPlaceholderText("Comparative parsing module text will be shown here")

        self.result2_text = QTextEdit(self)
        self.result2_text.setReadOnly(True)
        self.result2_text.setPlaceholderText("AI Module requirement rewrite will be shown here")

        self.layout.addWidget(self.intro_label)
        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.submit_button_cpm)
        self.layout.addWidget(self.submit_button_ai_EARS)
        self.layout.addWidget(self.submit_button_ai_ECSS)
        #self.layout.addWidget(self.submit_button_ai_ISO29148)                
        self.layout.addWidget(self.loading_bar)
        self.layout.addWidget(self.result1_text)
        self.layout.addWidget(self.result2_text)

        # Provide buttons to enable user to give feedback
        self.feedback_layout = QHBoxLayout()
        self.feedback_label = QLabel("Please provide feedback on this requirement:", self)

        self.good_requirement_button = QPushButton("Good requirement", self)
        self.good_requirement_button.setStyleSheet("background-color: green; color: white;")
        self.good_requirement_button.clicked.connect(self.log_good_feedback)

        self.bad_requirement_button = QPushButton("Bad requirement", self)
        self.bad_requirement_button.setStyleSheet("background-color: red; color: black;")
        self.bad_requirement_button.clicked.connect(self.log_bad_feedback)

        self.feedback_layout.addWidget(self.feedback_label)
        self.feedback_layout.addWidget(self.good_requirement_button)
        self.feedback_layout.addWidget(self.bad_requirement_button)

        self.layout.addLayout(self.feedback_layout)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def process_input_cpm(self):
        user_input = self.input_field.text()

        if not user_input:
            self.result1_text.setPlainText("No input provided")
            return

        self.loading_bar.setVisible(True)
        QTimer.singleShot(100, lambda: self.run_script_individual("CPM.py"))

    def process_input_ai_EARS(self):
        user_input = self.input_field.text()

        if not user_input:
            self.result2_text.setPlainText("No input provided")
            return

        self.loading_bar.setVisible(True)
        QTimer.singleShot(100, lambda: self.run_script_individual("AIModule_EARS.py"))
    
    def process_input_ai_ECSS(self):
        user_input = self.input_field.text()

        if not user_input:
            self.result2_text.setPlainText("No input provided")
            return

        self.loading_bar.setVisible(True)
        QTimer.singleShot(100, lambda: self.run_script_individual("AIModule_ECSS.py"))

    #def process_input_ai_ISO29148(self):
     #   user_input = self.input_field.text()

     #   if not user_input:
     #       self.result2_text.setPlainText("No input provided")
     #       return

     #   self.loading_bar.setVisible(True)
     #   QTimer.singleShot(100, lambda: self.run_script_individual("AIModule_ISO29148.py"))        

    def run_script_individual(self, script_name):
        user_input = self.input_field.text()

        result = subprocess.run([sys.executable, script_name, user_input], capture_output=True, text=True)

        if script_name == "CPM.py":
            self.result1_text.setPlainText(result.stdout.strip())
        elif script_name == "AIModule_EARS.py":
            self.result2_text.setPlainText(result.stdout.strip())
        elif script_name == "AIModule_ECSS.py":
            self.result2_text.setPlainText(result.stdout.strip())
        #elif script_name == "AIModule_ISO29148.py":
        #    self.result2_text.setPlainText(result.stdout.strip())

        self.loading_bar.setVisible(False)

    def log_good_feedback(self):
        feedback = self.result2_text.toPlainText()
        with open("Good Requirement Feedback.txt", "a") as file:
            file.write(feedback + "\n")

    def log_bad_feedback(self):
        feedback = self.result2_text.toPlainText()
        with open("Bad Requirement Feedback.txt", "a") as file:
            file.write(feedback + "\n")

# Drag and drop -----------------------------------------------------------------------------------------------------

class FileDropBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setPlaceholderText("Drag and drop here")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.setPlainText(file_path)


class FileDropWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RACQUET - Drag and Drop")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Direct the user to input text
        self.intro_label = QLabel("Please Drag and drop your requirements file (only .docx or .xlsx) below, and then press submit.", self)

        self.file_drop_box = FileDropBox(self)

        self.submit_button_cpm = QPushButton("Submit", self)
        self.submit_button_cpm.clicked.connect(self.process_drag_and_drop_input)

        self.loading_bar = QProgressBar(self)
        self.loading_bar.setRange(0, 0)  # Indeterminate state
        self.loading_bar.setVisible(False)

        self.result1_text = QTextEdit(self)
        self.result1_text.setReadOnly(True)

        self.layout.addWidget(self.intro_label)
        self.layout.addWidget(self.file_drop_box)
        self.layout.addWidget(self.submit_button_cpm)
        self.layout.addWidget(self.loading_bar)
        self.layout.addWidget(self.result1_text)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def process_drag_and_drop_input(self): # Update to the CSV file module
        user_input = self.file_drop_box.toPlainText()

        if not user_input:
            self.result1_text.setPlainText("No input provided")
            return

        self.loading_bar.setVisible(True)
        QTimer.singleShot(100, lambda: self.run_script_multi("Document_Capture.py"))


    def run_script_multi(self, script_name):
        user_input = self.file_drop_box.toPlainText()
        output_file = "C:/Users/Paulm/OneDrive/Documents/University/Surrey/Y4/output file.csv"  # You can set the output file path as needed
        output_excel_file = "C:/Users/Paulm/OneDrive/Documents/University/Surrey/Y4/output file.xlsx"  # You can set the output file path as needed

        #print(f"Running script: {script_name} with input: {user_input} and output file: {output_file}")

        result = subprocess.run([sys.executable, script_name, user_input, output_file], capture_output=True, text=True)
        
        QTimer.singleShot(100, lambda: self.run_script_multi("AIModule_multi.py"))
        #print(f"Script output: {result.stdout}")
        #print(f"Script errors: {result.stderr}")

        if result.returncode == 0:
            # Convert the CSV file to an Excel file
            try:
                df = pd.read_csv(output_file)
                df.to_excel(output_excel_file, index=False)
                self.result1_text.setPlainText(f"Script executed successfully. Output saved to {output_excel_file}")
            except FileNotFoundError as e:
                self.result1_text.setPlainText(f"CSV file not found: {output_file}. Error: {str(e)}")
            except Exception as e:
                self.result1_text.setPlainText(f"Error converting CSV to Excel: {str(e)}")
        else:
            self.result1_text.setPlainText(f"Error running script:\n{result.stderr.strip()}")

        self.loading_bar.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    initial_window = InitialWindow()
    initial_window.show()
    sys.exit(app.exec())
