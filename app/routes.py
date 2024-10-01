from flask import render_template, request, jsonify
from app import app
from app.pdf_utils import extract_text_from_pdf, get_pdf_metadata
import os

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.lower().endswith('.pdf'):
        try:
            file_content = file.read()
            file.seek(0)  # Reset file pointer
            
            if len(file_content) == 0:
                return jsonify({"error": "File is empty"}), 400
            
            text = extract_text_from_pdf(file)
            file.seek(0)  # Reset file pointer
            metadata = get_pdf_metadata(file)
            
            return jsonify({
                "text": text,
                "metadata": metadata
            })
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Please upload a PDF."}), 400