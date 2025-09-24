import sys
import os
import torch
from transformers import pipeline
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QTextEdit, QPushButton, QScrollArea
)
from PySide6.QtCore import QThread, Signal

# Optimal thread configuration for CPU inference
num_physical_cores = os.cpu_count()  # Logical cores (hyperthreading included)
torch.set_num_threads(num_physical_cores)  # Maximize parallelism
torch.set_num_interop_threads(1)  # Reduce inter-op parallelism overhead

model_id = "Qwen/Qwen3-0.6B"
pipe = pipeline(
    "text-generation",
    model=model_id,
    device="cpu",  # Explicitly use CPU
    dtype=torch.float32,  # Native CPU precision (faster than bfloat16)
    trust_remote_code=True,  # Required for Qwen models
)

# System message to direct the chatbot
system_message = "You are a pirate chatbot who always responds in pirate speak! /no_think"

def extract_assistant_text(generated_data):
    """
    Extracts assistant's response from generated data.
    If data is a list, searches for 'assistant' role and returns content.
    Replaces newlines with spaces for cleaner display.
    """
    if isinstance(generated_data, list):
        for item in generated_data:
            if item.get("role") == "assistant":
                return item["content"].replace("\n", " ")
        return ""
    else:
        return str(generated_data)

class GenerationThread(QThread):
    """Worker thread for text generation to prevent UI freezing"""
    finished = Signal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": self.prompt},
        ]

        try:
            outputs = pipe(messages, max_new_tokens=256)
            raw_output = outputs[0]["generated_text"]
            generated = extract_assistant_text(raw_output)
        except Exception as e:
            generated = f"Error: {e}"

        self.finished.emit(generated)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pirate Chatbot Generator")
        self.setGeometry(100, 100, 600, 500)  # x, y, width, height

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Prompt input section
        self.prompt_label = QLabel("Enter your prompt:")
        layout.addWidget(self.prompt_label)

        self.prompt_entry = QTextEdit()
        self.prompt_entry.setPlaceholderText("Type your message here...")
        self.prompt_entry.setMinimumHeight(100)
        layout.addWidget(self.prompt_entry)

        # Generate button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.on_generate)
        layout.addWidget(self.generate_button)

        # Output section
        self.output_label = QLabel("Generated Text:")
        layout.addWidget(self.output_label)

        # Create scrollable text area for output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(150)

        # Add scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.output_text)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Add stretch to push everything to the top
        layout.addStretch()

    def on_generate(self):
        # Disable button during generation
        self.generate_button.setEnabled(False)

        # Get prompt text
        prompt = self.prompt_entry.toPlainText().strip()

        # Create and start worker thread
        self.worker = GenerationThread(prompt)
        self.worker.finished.connect(self.handle_generation_result)
        self.worker.start()

    def handle_generation_result(self, result):
        # Update UI with results
        self.output_text.setPlainText(result)
        self.generate_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
