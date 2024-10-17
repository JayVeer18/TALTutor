import sys
import os

# Add the absolute path to the project root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from TALTutor_Frontend.base_app import App

# Get the directory of the current script (where this Python file is located)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the file you want to access from the script location
relative_file_path = os.path.join(script_dir,"..", "files", "pythagoras.pdf")  # ".." goes up one directory

# Normalize the path to handle any redundant separators
file_path = os.path.normpath(relative_file_path)

app = App("### Lecture : Pythagorean", file_path, "https://youtu.be/d8EA5TxGzcY?si=FvbtXEZHu0fgCCQX", "Pythagorean")
app.run()