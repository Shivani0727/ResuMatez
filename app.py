from flask import Flask, render_template, request
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_keywords(resume, jd):
    corpus = [resume, jd]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(corpus)
    features = vectorizer.get_feature_names_out()
    scores = tfidf.toarray()
    
    jd_top = [features[i] for i in scores[1].argsort()[-15:][::-1]]
    missing = [kw for kw in jd_top if kw not in resume.lower()]
    
    return jd_top, missing

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    resume = extract_text_from_pdf(request.files['resume'])
    jd = request.form['jd']
    keywords, suggestions = extract_keywords(resume, jd)
    return render_template('result.html', keywords=keywords, suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True)
