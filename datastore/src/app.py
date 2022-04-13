from flask import Flask, jsonify
from os import environ
import os
import pandas as pd
import json

from data_loading import *

## Get Parameters
SECRET_KEY = environ.get("SECRET_KEY")
print("SECRET KEY", SECRET_KEY)

# ----------------------------------------------------------------------------
# DATA PARAMETERS
# ----------------------------------------------------------------------------
current_folder = os.path.dirname(__file__)
DATA_PATH = os.path.join(current_folder,'data')
ASSETS_PATH = os.path.join(current_folder,'assets')


# Path to Report files at TACC
api_root = 'https://api.a2cps.org/files/v2/download/public/system/a2cps.storage.community/reports'


# ----------------------------------------------------------------------------
# LOAD ASSETS FILES
# ----------------------------------------------------------------------------
asset_files_dict = {
    'screening_sites': 'screening_sites.csv',
    'display_terms': 'A2CPS_display_terms.csv',
}

display_terms, display_terms_dict, display_terms_dict_multi = load_display_terms(ASSETS_PATH, asset_files_dict['display_terms'])

screening_sites = pd.read_csv(os.path.join(ASSETS_PATH,asset_files_dict['screening_sites']))

# ----------------------------------------------------------------------------
# LOAD INITAL DATA FROM FILES
# ----------------------------------------------------------------------------
local_data = {}
local_data['date'] = '2022-04-13'
local_data['subjects'] = get_local_subjects(DATA_PATH)
local_data['imaging'] = get_local_imaging(DATA_PATH)
local_data['blood'] = get_local_blood(DATA_PATH)
# ----------------------------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------------------------

# try:
#     subjects_data = get_api_subjects()
#     if subjects_data:
#         subjects_data = subjects_data
#     else:
#         subjects_data = {'flipping':'hell'}
#
# except Exception as e:
#     traceback.print_exc()
#     subjects_data = {'status':'bad'}
#
#
# try:
#     imaging_data = get_api_imaging()
# except Exception as e:
#     traceback.print_exc()
#     imaging_data = {'status':'bad'}
#
# try:
#     blood_data = get_api_blood()
# except Exception as e:
#     traceback.print_exc()
#     blood_data = {'status':'bad'}
# available_data = get_data_from_api(screening_sites, display_terms_dict, display_terms_dict_multi)


# ----------------------------------------------------------------------------
# APIS
# ----------------------------------------------------------------------------

app = Flask(__name__)

# APIS: try to load new data, if doesn't work, get most recent
@app.route("/api/imaging")
def api_imaging():
    return jsonify(local_data['imaging'] )

@app.route("/api/subjects")
def api_subjects():
    return jsonify(local_data['subjects'] )

@app.route("/api/blood")
def api_blood():
    return jsonify(local_data['blood'] )

@app.route("/api/full")
def api_full():
    datafeeds = {'date': {'weekly': 'today', 'consort': 'today', 'blood': 'today'},
                'data': {'weekly': 'tbd', 'consort': 'tbd', 'blood': 'tbd'}}
    return jsonify(datafeeds)

# @app.route("/api/subjects")
# def api_subjects():
#     return json.dumps(subjects_data)
#
# @app.route("/api/imaging")
# def api_imaging():
#     return jsonify(imaging_data)
#
# @app.route("/api/blood")
# def api_blood():
#     return jsonify(blood_data)



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


# @app.route("/imaging")
# def api_imaging():
#     imaging_dict = imaging_df.to_dict('records')
#     # imaging_dict={'columns': imaging_columns, 'data': imaging_data}
#     return jsonify(imaging_dict)
#
# @app.route("/qc")
# def api_qc():
#     qc_dict = qc_df.to_dict('records')
#     # imaging_dict={'columns': imaging_columns, 'data': imaging_data}
#     return jsonify(qc_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
