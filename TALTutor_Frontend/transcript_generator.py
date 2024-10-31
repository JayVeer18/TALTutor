import whisper
from tqdm import tqdm  # For showing progress
from fpdf import FPDF  # For creating PDF files

# Step 1: Download video from URL
video_url = 'https://baps.app.box.com/s/e6jpn4d5uzky5xeufhin1kd13o2ag9aw'
video_path = r'BAPS Executive Forum Oct 5 2024 Dr Prasad Kaipa Lecture.mp4'

# Load Whisper model
model = whisper.load_model("large") # You can use "small", "medium", or "large" for more accuracy

print("Starting transcription...")

# Split the audio and transcribe in parts (simulates progress)
result = model.transcribe(video_path,language="en", verbose=True)
print("Transcription complete!")

# Extract the transcript text
transcript_text = result["text"]

# Save transcript as a PDF
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

# Add text to PDF, line by line
for line in transcript_text.split("\n"):
    pdf.multi_cell(0, 10, line)

# Save the PDF file
pdf_file_path = "transcription.pdf"
pdf.output(pdf_file_path)
print(f"Transcript saved as PDF at: {pdf_file_path}")
