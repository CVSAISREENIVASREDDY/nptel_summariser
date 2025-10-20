import fitz  # PyMuPDF
import os

def get_assignment_text(week_number):
    script_dir = os.path.dirname(__file__)
    assignment_filename = f"week{week_number}.pdf"
    assignment_path = os.path.join(script_dir, "assignments", assignment_filename)

    if not os.path.exists(assignment_path):
        return f"Assignment file not found: {assignment_path}"

    try:
        doc = fitz.open(assignment_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading assignment file: {e}"
