import fitz


def extract_resume_text(uploaded_file):
    """
    Extract text from an uploaded PDF resume.
    """

    pdf_bytes = uploaded_file.read()
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    return text.strip()