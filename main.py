import os
import random
import PyPDF2 # pip install pypdf2
from fpdf import FPDF # pip install fpdf
import spacy # pip install spacy

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# method to extract the sentences
def extract_random_sentences(text):
    doc = nlp(text)
    sentences = list(doc.sents)
    selected_sentences = random.sample(sentences, int(len(sentences) * 2 / 3))
    return ' '.join([str(sentence) for sentence in selected_sentences])

# method to extract the text from the pdf file
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

# Folder containing PDF files
pdf_folder = input("Enter folder path containing PDFs: ")

# Output folder for summarized PDFs
output_folder = input("Enter output folder path: ")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# creating the summarized pdfs 
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        text = extract_text_from_pdf(pdf_path)
        result = extract_random_sentences(text)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        pdf.multi_cell(0, 5, result)

        output_path = os.path.join(output_folder, f"summarized_{filename}")
        pdf.output(output_path)

print("Summarized PDFs saved in the output folder.")
