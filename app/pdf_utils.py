import io
import pikepdf
from pdfminer.high_level import extract_text as pdfminer_extract_text

def extract_text_from_pdf(pdf_file):
    pdf_content = pdf_file.read()
    pdf_file_obj = io.BytesIO(pdf_content)
    
    # Try pikepdf first
    try:
        with pikepdf.Pdf.open(pdf_file_obj) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"pikepdf extraction failed: {str(e)}")

    # If pikepdf fails, try pdfminer
    try:
        pdf_file_obj.seek(0)  # Reset file pointer
        text = pdfminer_extract_text(pdf_file_obj)
        return text
    except Exception as e:
        print(f"pdfminer extraction failed: {str(e)}")

    # If both fail, try a raw text extraction
    try:
        pdf_file_obj.seek(0)  # Reset file pointer
        text = pdf_file_obj.read().decode('utf-8', errors='ignore')
        return text
    except Exception as e:
        print(f"Raw text extraction failed: {str(e)}")

    return "Text extraction failed for this PDF."

def get_pdf_metadata(pdf_file):
    pdf_content = pdf_file.read()
    pdf_file_obj = io.BytesIO(pdf_content)
    
    try:
        with pikepdf.Pdf.open(pdf_file_obj) as pdf:
            return {
                "page_count": len(pdf.pages),
                "version": pdf.pdf_version,
                "is_encrypted": pdf.is_encrypted,
            }
    except Exception as e:
        print(f"Metadata extraction failed: {str(e)}")
        return {"error": "Unable to extract metadata"}