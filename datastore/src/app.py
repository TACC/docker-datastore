from flask import Flask, jsonify
from os import environ
import os
import pandas as pd

from data_loading import *

## Get Parameters
SECRET_KEY = environ.get("SECRET_KEY")
print("SECRET KEY", SECRET_KEY)

# ----------------------------------------------------------------------------
# DATA PARAMETERS
# ----------------------------------------------------------------------------

# Directions for locating file at TACC
file_url_root ='https://api.a2cps.org/files/v2/download/public/system/a2cps.storage.community/reports'

current_folder = os.path.dirname(__file__)
DATA_PATH = os.path.join(current_folder,'data')
ASSETS_PATH = os.path.join(current_folder,'assets')

# Parameters
display_terms_file = 'A2CPS_display_terms.csv'
mcc_list=[1,2]

# ----------------------------------------------------------------------------
# LOAD ASSETS FILES
# ----------------------------------------------------------------------------

display_terms, display_terms_dict, display_terms_dict_multi = load_display_terms(ASSETS_PATH, display_terms_file)

# ----------------------------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------------------------
# full_subjects = get_subjects_data_from_local_file(DATA_PATH,  [1,2])
#
# # Clean subjects
# subjects_df = clean_subjects_data(full_subjects, display_terms_dict)
# subjects_columns = list(subjects_df.columns)
# subjects_data = subjects_df.reset_index(drop=True).to_dict('records')
# subjects_dict_index = subjects_df.reset_index(drop=True).to_dict('index')
# adverse_effects = extract_adverse_effects_data(subjects)

# IMAGING RELATED FILES
imaging_df = pd.read_csv(os.path.join(DATA_PATH,'imaging','imaging-log-latest.csv')).reset_index(drop=True)
imaging_columns = list(imaging_df.columns)
imaging_data = imaging_df.reset_index(drop=True).to_dict('records')

qc_df = pd.read_csv(os.path.join(DATA_PATH,'imaging','qc-log-latest.csv')).reset_index(drop=True)
qc_columns = list(qc_df.columns)
qc_data = qc_df.reset_index(drop=True).to_dict('records')

# ----------------------------------------------------------------------------
# APIS
# ----------------------------------------------------------------------------

app = Flask(__name__)

@app.route("/api")
def api():
    datafeeds = {'date': {'weekly': 'today', 'consort': 'today', 'blood': 'today'},
                'data': {'weekly': 'tbd', 'consort': 'tbd', 'blood': 'tbd'}}
    return jsonify(datafeeds)

# @app.route("/subjects")
# def api_subjects():
#     # if not subjects_df:
#     datafeeds = {'date': {'weekly': 'today', 'consort': 'today', 'blood': 'today'},
#                 'data': {'weekly': 'tbd', 'consort': 'tbd', 'blood': 'tbd'}}
#     subjects_dict = pd.DataFrame(datafeeds).to_dict('records')
#     # else:
#     #     subjects_dict = subjects_df.to_dict('records')
#     # subjects_dict={'columns': subjects_columns, 'data': subjects_data}
#     return jsonify(subjects_dict)


@app.route("/imaging")
def api_imaging():
    imaging_dict = imaging_df.to_dict('records')
    # imaging_dict={'columns': imaging_columns, 'data': imaging_data}
    return jsonify(imaging_dict)

@app.route("/qc")
def api_qc():
    qc_dict = qc_df.to_dict('records')
    # imaging_dict={'columns': imaging_columns, 'data': imaging_data}
    return jsonify(qc_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
