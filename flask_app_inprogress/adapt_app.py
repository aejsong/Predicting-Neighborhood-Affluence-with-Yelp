# Flask App code and HTML borrowed from Mario Sanchez, Erin Hwang, and Jawaid Ismail

from flask import Flask, render_template, request, g, session, redirect, url_for
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import requests
import pickle

# Flask app
app = Flask(__name__)

# homepage
@app.route('/')
def index():
    return render_template('index.html')

# team page
@app.route('/team/')
def team():
    return render_template('team.html')


# prediction function used in process function below
def affluency_predictor(to_predict):
    # format the variable
    session_int = int(to_predict.strip())
    df = pd.read_csv("MARIO_MODEL_PCA.csv").drop(columns="Unnamed: 0")
    # create array from dataframe row
    predict_array = np.array(df[df['zip_code'] == session_int].drop(columns ='zip_code'))
    print(predict_array)
    # load trained model
    loaded_model = pickle.load(open("model_gb_mother.pkl", "rb"))
    # predict
    result = loaded_model.predict(predict_array)
    print(result)
    print('------------')
    return result[0]


# What happens after submitting a zipcode
@app.route('/process', methods=["POST"])
def process():
    if request.method == 'POST':

        results = affluency_predictor(request.form['rawtext'])

        # session variable
        session['text'] = request.form['rawtext']

        print(results)

        return render_template("index.html",results=np.round(results,2))
