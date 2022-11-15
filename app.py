from flask import Flask, request
from flask_cors import CORS, cross_origin

import os
import json
import pickle
import numpy as np
import pandas as pd
from scipy import stats

app = Flask(__name__)

cors = CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

# Loading model pipelines
intent_rf_pipeline = pickle.load(
    open("model.pkl", "rb")
)


def convert(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def predict_customer_purchase_intent(input_data):

    prediction_data = {
        "rf_model_prediction": intent_rf_pipeline.predict(input_data),
        # "rf_model_probability": max(intent_rf_pipeline.predict_proba(input_data)[0])
        # * 100
    }
    print("prediction_data: ", prediction_data.rf_model_prediction)[0]
    return prediction_data


@app.route("/predict", methods=["GET", "POST"])
def predictintent():
    try:
        if request.method == "POST":
            form_values = request.form.to_dict()
            # print(form_values)
            column_names = ["Administrative", "Administrative_Duration","Informational","Informational_Duration", "ProductRelated",	"ProductRelated_Duration", "BounceRates", "ExitRates","PageValues", "SpecialDay", "Month", "OperatingSystems","Region", "TrafficType",	"VisitorType"]
            input_data = np.asarray([(form_values[i].strip()) for i in column_names]).reshape(
                1, -1
            )
            prediction_data = intent_rf_pipeline(pd.get_dummies(input_data))
            json_obj = json.dumps(prediction_data, default=convert)
            return json_obj
    except:
        return json.dumps({"error":"Hey Enter Valid Data"}, default=convert)

if __name__ == "__main__":
    app.run(debug=True)