from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files or 'jd' not in request.form:
        return "Missing file or JD", 400

    resume = request.files['resume']
    jd = request.form['jd']

    if resume.filename == '':
        return "No selected file", 400

    # Save file (optional)
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    resume.save(resume_path)

    # Simulated keyword extraction
    keywords = ["Python", "Data Analysis", "Leadership", "Communication", "Time Management", "Teamwork"]

    return render_template('result.html', keywords=keywords)

@app.route('/result')
def result():
    return render_template('result.html', keywords=[])

if __name__ == '__main__':
    app.run(debug=True)
