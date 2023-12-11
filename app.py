from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
from tensorflow.keras.models import load_model
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from PyPDF2 import PdfReader
import logging
import sys
import aspose.words as aw
import time
import subprocess

app = Flask(__name__)
url = ""

logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO")
    )
logging.getLogger().setLevel(logging.INFO)

data = pd.read_csv('concat.csv')

X_data = data['Abstract']
y_data = data['recommand']
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0, stratify=y_data)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)
X_train_encoded = tokenizer.texts_to_sequences(X_train)
print(X_train_encoded[:5])
word_to_index = tokenizer.word_index
max_len = 627

loaded_model = load_model('best_model.h5')

def download_arxiv_pdf(arxiv_id, download_dir='pdf_downloads'):
    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)

    # Construct the arXiv URL
    arxiv_url = f'https://arxiv.org/abs/{arxiv_id}'

    # Send an HTTP request to get the HTML content of the arXiv page
    response = requests.get(arxiv_url)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the link to the PDF file on the arXiv page
        pdf_link = soup.find('meta', {'name': 'citation_pdf_url'})
        if pdf_link and pdf_link.get('content'):
            # Construct the absolute URL of the PDF file
            pdf_url = pdf_link.get('content')

            # Send an HTTP request to download the PDF file
            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200:
                # Save the PDF file to the download directory
                pdf_filename = f'{arxiv_id}.pdf'
                pdf_filepath = os.path.join(download_dir, pdf_filename)
                with open(pdf_filepath, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                
                return f'Downloaded PDF: {pdf_filepath}'
            else:
                return f'Failed to download PDF. Status code: {pdf_response.status_code}'
        else:
            return 'PDF link not found in the meta tags on the arXiv page.'
    else:
        return f'Failed to fetch arXiv page. Status code: {response.status_code}'

def predict(title, text):
    text = re.sub('[^0-9a-zA-Z]', ' ', text).lower()
    encoded = []

    for word in text.split():
        try:
            if word_to_index[word] <= 10000:
                encoded.append(word_to_index[word]+3)
            else:
                encoded.append(2)
        except KeyError:
            encoded.append(2)

    pad_new = pad_sequences([encoded], maxlen = max_len)
    score = float(loaded_model.predict(pad_new))

    if(score > 0.7):
        return "[{}]는 읽어보기에 괜찮은 논문입니다.\n".format(title), score
    elif(score > 0.5):
        return "[{}]는 읽어보심을 추천합니다.\n".format(title), score
    elif(score > 0.3):
        return "[{}]는 읽어보심을 추천하지만, 다른 논문을 먼저 읽어보심을 추천합니다.\n".format(title), score
    else:
        return "[{}]는 읽어보심을 추천하지 않습니다.\n".format(title), score

@app.route('/', methods=['GET', 'POST'])
def index():
    output_text = None
    if request.method == 'POST':
        # 사용자가 입력한 텍스트를 가져옵니다.
        url = request.form['search_text']

        response = requests.get(url)
        html_content = response.text

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(html_content, 'html.parser')
        
        arxiv_title = soup.find('h1', class_='title mathjax').get_text(strip=True)
        print(arxiv_title[6:])
        arxiv_abs = soup.find('blockquote', class_='abstract mathjax').get_text(strip=True)
        print(arxiv_abs[9:])
        
        output_text, score = predict(arxiv_title, arxiv_abs[9:])

        if score > 0.5:
            arxiv_id = url.split('/')[-1]
            print(arxiv_id)
            time.sleep(3)
            output_text = download_arxiv_pdf(arxiv_id)
            print(output_text)

            reader = PdfReader(f"./pdf_downloads/{arxiv_id}.pdf")
            pages = reader.pages
            text = ""
            for page in pages:
                sub = page.extract_text()
                text += sub
            with open("./factorsum/Output.txt", "w", encoding='utf8') as text_file:
                text_file.write(text)

            command = "python ./factorsum/test.py"
            result = subprocess.check_output(command, shell=True, universal_newlines=True)
            sentences = re.findall(r"'(.*?)'", result)

            # 각 문장에 개행 추가
            formatted_text = "\n".join(sentences)

            # 결과 출력
            print(formatted_text)
            
            return render_template('summary_pdf.html', result=formatted_text+str(score))

    return render_template('index.html', output_text=output_text+str(score))

@app.route('/summary_pdf')
def summary_pdf():
    output_text = "PDF 파일을 다운로드 받았습니다."
    return render_template('summary_pdf.html', output_text=output_text)

if __name__ == '__main__':
    app.run(debug=True)
