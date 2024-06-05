import os
from docx import Document  # pip install python-docx
from fpdf import FPDF  # pip install fpdf
import spacy  # pip install spacy

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Method to extract the sentences in sequence for each paragraph
def summarize_paragraph(text, reduction_ratio=8/10):
    doc = nlp(text)
    sentences = list(doc.sents)
    num_sentences_to_select = max(1, int(len(sentences) * reduction_ratio))
    selected_sentences = sentences[:num_sentences_to_select]
    return ' '.join([str(sentence) for sentence in selected_sentences])

# Method to extract and summarize the text from the docx file
def extract_and_summarize_text_from_docx(docx_path, reduction_ratio=8/10):
    doc = Document(docx_path)
    summarized_text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():  # Check if the paragraph is not empty
            summarized_paragraph = summarize_paragraph(paragraph.text, reduction_ratio)
            summarized_text += summarized_paragraph + "\n"
    return summarized_text

# Folder containing DOCX files
docx_folder = input("Enter folder path containing DOCX files: ")

# Output folder for summarized PDFs
output_folder = input("Enter output folder path: ")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Creating the summarized PDFs
for filename in os.listdir(docx_folder):
    if filename.endswith(".docx"):
        docx_path = os.path.join(docx_folder, filename)
        summarized_text = extract_and_summarize_text_from_docx(docx_path)

        pdf = FPDF()

        # Add the Unicode font
        pdf.add_font('DejaVu', '', '/run/media/ashwinhimanshu11/New Volume/Work/Work/pdf_summarizer/font/DejaVuSans.ttf', uni=True)

        # Set the font to DejaVu for content
        pdf.set_font('DejaVu', '', 10)

        pdf.add_page()
        pdf.multi_cell(0, 5, summarized_text)

        output_path = os.path.join(output_folder, f"summarized_{filename[:-5]}.pdf")
        pdf.output(output_path)

print("Summarized PDFs saved in the output folder.")
