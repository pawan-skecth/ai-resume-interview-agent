from pypdf import PdfReader
import re


def clean_resume_text(text):

    # Remove extra spaces between characters
    text = re.sub(r'(?<=\w)\s(?=\w)', '', text)

    # Replace multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)

    return text


def extract_text_from_pdf(uploaded_file):

    pdf_reader = PdfReader(uploaded_file)

    text = ""

    for page in pdf_reader.pages:

        extracted_text = page.extract_text()

        if extracted_text:

            text += extracted_text

    cleaned_text = clean_resume_text(text)

    return cleaned_text