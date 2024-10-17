import streamlit as st
import os

# st.sidebar.title("Navigation")
# st.sidebar.info("Choose a section from the sidebar")

# Image URL
image_url = 'https://play-lh.googleusercontent.com/TJ5FL4km1GSK_MvO8Yy9Ad0GezFLYhSk4eUFGCWhaj_07iKjhW6Zp2hS33Rtb3TokVTU=s64-rw'

st.markdown("# Drona, your Learning Companion welcomes you")
st.markdown(
            f"""
    <div style='text-align: center; padding-top: 20px;'>
        <img src="{image_url}" alt="Logo" style="width: 50px;">
    </div>
    """,
    unsafe_allow_html=True)

# st.sidebar.header('NSF')
st.sidebar.markdown("# Welcome to Drona, the TALTutor App")

# Add multiple empty strings to create space above the footer
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Footer with an image and text
st.sidebar.markdown(
    f"""
    <div style='text-align: center; padding-top: 20px;'>
        <img src="{image_url}" alt="Logo" style="width: 50px;">
        <p>Powered by <b>TOUCH-A-LIFE Foundation</b></p>
    </div>
    """,
    unsafe_allow_html=True
)
# st.sidebar.caption('Powered by TOUCH-A-LIFE Foundation')


# Define where to save the uploaded files
UPLOAD_FILES_FOLDER = "files"
CREATE_PYTHON_FILE_FOLDER = "pages"

# Ensure folders exists
if not os.path.exists(UPLOAD_FILES_FOLDER):
    os.makedirs(UPLOAD_FILES_FOLDER)

if not os.path.exists(CREATE_PYTHON_FILE_FOLDER):
    os.makedirs(CREATE_PYTHON_FILE_FOLDER)

st.markdown("### !!! As an Instructor, you can upload Video Url and transcripts pdf to create a new section!!!")

section_name = st.text_input("Enter the Section/Module Name")

# Input field for video URL
video_url = st.text_input("Enter the video URL")

# File uploader for PDF
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Submit button
if st.button("Submit"):
    if video_url and pdf_file and section_name:
        # Save the PDF file to the UPLOAD_FILES_FOLDER
        pdf_file_path = os.path.join(UPLOAD_FILES_FOLDER, f"{section_name}.pdf")
        with open(pdf_file_path, "wb") as f:
            f.write(pdf_file.read())

        # Path to the new Python file to be created
        new_python_file = os.path.join(CREATE_PYTHON_FILE_FOLDER, f"{section_name}.py")

        # Create the new Python file with the video URL and PDF path
        with open(new_python_file, "w") as py_file:
            py_file.write(f"import sys\n")
            py_file.write(f"import os\n\n")
            py_file.write(f"# Add the absolute path to the project root directory\n")
            py_file.write(f"sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))\n\n")
            py_file.write(f"from TALTutor_Frontend.base_app import App\n\n")
            py_file.write(f"# Get the directory of the current script (where this Python file is located)\n")
            py_file.write(f"script_dir = os.path.dirname(os.path.abspath(__file__))\n\n")
            py_file.write(f"# Define the relative path to the file you want to access from the script location\n")
            py_file.write(f'relative_file_path = os.path.join(script_dir,"..", "{UPLOAD_FILES_FOLDER}", "{section_name}.pdf")  # ".." goes up one directory\n\n')
            py_file.write(f"# Normalize the path to handle any redundant separators\n")
            py_file.write(f"file_path = os.path.normpath(relative_file_path)\n\n")

            py_file.write(f'app = App("### Lecture : {section_name}", file_path, "{video_url}", "{section_name}")\n')
            py_file.write(f"app.run()\n")

        # Show success message
        st.success(f"New Module:{section_name} is Created Successfully.")
        st.code(open(new_python_file).read())  # Display the generated Python file content
    else:
        st.error("Please provide both a video URL and a PDF file along with Section/Module Name.")
