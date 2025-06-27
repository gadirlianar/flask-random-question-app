from flask import Flask, request, render_template
import fitz  # PyMuPDF
import random

app = Flask(__name__)

def extract_questions(pdf_bytes, start_page, end_page):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    questions = []
    for page_num in range(start_page - 1, end_page):
        text = doc.load_page(page_num).get_text()
        for line in text.split("\n"):
            if line.strip().startswith(tuple(str(i) + '.' for i in range(1, 1000))):
                questions.append(line.strip())
    return questions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        start_page = int(request.form['start_page'])
        end_page = int(request.form['end_page'])
        question_count = int(request.form['question_count'])

        pdf_bytes = pdf_file.read()
        questions = extract_questions(pdf_bytes, start_page, end_page)

        selected = random.sample(questions, min(question_count, len(questions)))
        return render_template('result.html', questions=selected)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
