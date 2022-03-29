from flask import Flask, jsonify
from os import environ
import os
import pandas as pd

from data_loading import *

## Get Parameters
SECRET_KEY = environ.get("SECRET_KEY")
print("SECRET KEY", SECRET_KEY)

## Load data
mcc_list=[1,2]

# Directions for locating file at TACC
file_url_root ='https://api.a2cps.org/files/v2/download/public/system/a2cps.storage.community/reports'

current_folder = os.path.dirname(__file__)
data_folder  ='data'

# URLS
subjects_raw_url = load_report_data(file_url_root, 'subjects', mcc_list)

# Local files
subjects_raw = load_raw_subjects_files(current_folder, data_folder, mcc_list)

subjects = {}
weekly_data = pd.DataFrame()

for mcc in subjects_raw.keys():
    mcc_data = pd.DataFrame.from_dict(subjects_raw[mcc], orient = 'index')
    mcc_data['mcc'] = mcc
    if weekly_data.empty:
        weekly_data = mcc_data
    else:
        weekly_data = pd.concat([weekly_data, mcc_data])

weekly_data.reset_index(inplace=True)
if 'index' in weekly_data.columns:
    weekly_data.rename(columns={"index": "record_id"}, inplace=True)

subjects['weekly'] = weekly_data.to_dict('index')

# local_data_store = load_data(file_url_root, reports, mcc_list)


app = Flask(__name__)

@app.route("/api")
def api():
    datafeeds = {
        "weekly": {"date" : "today", "data" : 'tbd'},
        "consort": {"date" : "today", "data" : 'tbd'},
        "blood": {"date" : "today", "data" : 'tbd'},
    }
    return jsonify(datafeeds)

@app.route("/subjects")
def api_weekly():

    return jsonify(subjects)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
