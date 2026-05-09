import os
import glob
import json

try:
    from docx import Document
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx", "PyPDF2"])
    from docx import Document

try:
    import PyPDF2
except ImportError:
    pass # Already installed above

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        text = ''
        for para in doc.paragraphs:
            text += para.text + '\n'
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {e}"

out = {}
files = glob.glob('*Proper M*.*')
for file in sorted(files):
    if file.endswith('.pdf'):
        out[file] = extract_text_from_pdf(file)
    elif file.endswith('.docx'):
        out[file] = extract_text_from_docx(file)

with open('extracted_texts.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2)

print("Extraction complete.")
