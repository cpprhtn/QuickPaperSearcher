from flask import Flask, render_template, request
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

app = Flask(__name__)
url = ""

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

#loaded_model = load_model('best_model.h5')


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
        print("[{}]는 읽어보기에 괜찮은 논문입니다.\n".format(title))
    elif(score > 0.5):
        print("[{}]는 읽어보심을 추천합니다.\n".format(title))
    elif(score > 0.3):
        print("[{}]는 읽어보심을 추천하지만, 다른 논문을 먼저 읽어보심을 추천합니다.\n".format(title))
    else:
        print("[{}]는 읽어보심을 추천하지 않습니다.\n".format(title))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 사용자가 입력한 텍스트를 가져옵니다.
        url = request.form['url']
        
        # 여기에서 검색 텍스트를 변수로 활용할 수 있습니다.
        # 이 예시에서는 간단히 콘솔에 출력합니다.
        print(f'Search Text: {url}')
        url = input("What paper do you want to search? ")

        response = requests.get(url)
        html_content = response.text

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(html_content, 'html.parser')
        
        arxiv_title = soup.find('h1', class_='title mathjax').get_text(strip=True)
        print(arxiv_title[6:])
        arxiv_abs = soup.find('blockquote', class_='abstract mathjax').get_text(strip=True)
        print(arxiv_abs[9:])
        
        predict(arxiv_title, arxiv_abs[9:])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
