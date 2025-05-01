from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx
import nltk
from nltk.corpus import stopwords

# Initialize the Flask application
app = Flask(__name__)

# File upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text

# Function to extract keywords from text
def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = text.split()
    keywords = [word.lower() for word in words if word.lower() not in stop_words and len(word) > 2]
    return keywords

# Function to handle allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        resume = request.files.get('resume')
        job_desc = request.files.get('job_desc')

        if resume and allowed_file(resume.filename) and job_desc and allowed_file(job_desc.filename):
            resume_filename = secure_filename(resume.filename)
            job_desc_filename = secure_filename(job_desc.filename)

            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resumes', resume_filename)
            job_desc_path = os.path.join(app.config['UPLOAD_FOLDER'], 'job_descriptions', job_desc_filename)

            resume.save(resume_path)
            job_desc.save(job_desc_path)

            # Extract text from the files
            if resume_filename.endswith('.pdf'):
                resume_text = extract_text_from_pdf(resume_path)
            elif resume_filename.endswith('.docx'):
                resume_text = extract_text_from_docx(resume_path)

            if job_desc_filename.endswith('.pdf'):
                job_desc_text = extract_text_from_pdf(job_desc_path)
            elif job_desc_filename.endswith('.docx'):
                job_desc_text = extract_text_from_docx(job_desc_path)

            # Extract keywords from resume and job description
            resume_keywords = extract_keywords(resume_text)
            job_desc_keywords = extract_keywords(job_desc_text)

            return render_template('result.html', resume_keywords=resume_keywords, job_desc_keywords=job_desc_keywords)

    return render_template('upload.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
