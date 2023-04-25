import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from joblib import load
from nltk.tokenize import TweetTokenizer
from flask_cors import CORS, cross_origin
import pandas as pd
import pickle
import numpy as np
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize.treebank import TreebankWordDetokenizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.feature_extraction.text import TfidfVectorizer 
import nltk
nltk.download('punkt')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/analisis', methods=['GET', 'POST'])
def analisis():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('analisis.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('info.html')

svm_model = pickle.load(open('model\\svm.pkl','rb'))
nb_model = pickle.load(open('model\\nb.pkl','rb'))
tree_model = pickle.load(open('model\\tree.pkl','rb'))

stop_factory = StopWordRemoverFactory()
data_stopword = stop_factory.get_stop_words()
stopword = stop_factory.create_stop_word_remover()
stemming = StemmerFactory().create_stemmer()

def tokenize(text):
    tokenizer = TweetTokenizer()
    return tokenizer.tokenize(text)

def stop_list(row):
    my_list = row
    stop_list = [stopword.remove(i) for i in my_list]
    return (stop_list)

def stem_list(row):
    my_list = row
    stemmed_list = [stemming.stem(i) for i in my_list]
    return (stemmed_list)

def remove_number(text):
    return re.sub("[^a-zA-Z]", " ",str(text))

def identify_tokens(row):
    text = row
    tokens = nltk.word_tokenize(text)
    token_words = [w for w in tokens if w.isalpha()]
    return token_words

vectorizer = pickle.load(open('model\\vectorizer.pickle',  'rb'))

model_m = "svm"

@app.route("/getmodel", methods=['GET', 'POST'])
def getmodel():
    global model_m
    if request.method == "POST":
        value = request.form.getlist('options')
        if value[0] == 'option1':
            model_m = 'svm'
        if value[0] == 'option2':
            model_m = 'nb'
        if value[0] =='option3':
            model_m = 'tree'
        print(model_m)
    return render_template('analisis.html')

if model_m == 'svm':
    model = svm_model
if model_m == 'nb':
    model = nb_model
if model_m == 'tree':
    model = tree_model

# model = svm_model
                                                                                                                                                                                                                                                                                                                          
@app.route("/predict", methods=['GET', 'POST'])
def predict_function():
    # if request.method == "POST":
    #     value = request.args.get('model_name')
    #     print(value)
    if request.method == "POST":
        # value1 = request.json["inputs2"]
        # value2 = request.json["inputs3"]
        # value3 = request.json["inputs4"]
        # print(value1)

        print("space on")
        processed_text = request.json["inputs"]
        print(processed_text)
        processed_text = pd.DataFrame(processed_text)[0].str.replace('http\S+|www.\S+', '', case=False)
        processed_text = processed_text.str.replace('@[^\s]+','', case=False)
        processed_text = processed_text.str.replace('[^\w\s]','')
        processed_text = processed_text.apply(remove_number)
        processed_text = processed_text.apply(lambda x: " ".join(x.lower() for x in x.split()))
        processed_text = processed_text.apply(identify_tokens)
        processed_text = processed_text.apply(stop_list)
        processed_text = processed_text.apply(stem_list)
        input_payloads = " ".join(processed_text[0])
        input_payloads = vectorizer.transform([input_payloads])
        predictions = model.predict(input_payloads)
        json_result = pd.Series(predictions).to_json(orient="values")
        return json_result


if __name__ == "__main__":
    print("running service")
    app.run(debug=True)
