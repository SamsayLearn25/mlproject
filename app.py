from flask import Flask, render_template, request

import numpy as np
import pandas as pd
import os, sys

from sklearn.preprocessing import StandardScaler
from src.components.prediction import CustomData, PredictionPipeline
from src.exception import CustomException

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods = ["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("home.html")
    
    if request.method == "POST":

        try:
            data = CustomData(
                gender=request.form.get("gender"),
                race_ethnicity=request.form.get("ethnicity"),
                parental_level_of_education=request.form.get("parental_level_of_education"),
                lunch=request.form.get("lunch"),
                test_preparation_course=request.form.get("test_preparation_course"),
                reading_score=request.form.get("reading_score"),
                writing_score=request.form.get("writing_score")

            )
        except Exception as e:
            raise CustomException(e, sys)

        pred_df = data.get_data_as_dataframe()
        #print("Data Prepared: ", pred_df)
        predict_pipeline = PredictionPipeline()
        results = predict_pipeline.predict(pred_df)

        return render_template("home.html", results = results[0])
    

if __name__ == "__main__":
    app.run(host="0.0.0.0")


