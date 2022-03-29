import requests
import json
import os
import pandas as pd
import sqlite3
import datetime
from datetime import datetime, timedelta

def load_report_data(file_url_root, report, mcc_list):
    report_data = {}
    for mcc in mcc_list:
        mcc=str(mcc)
        report_suffix = report + '-' + str(mcc) + '-latest.json'
        file_url = '/'.join([file_url_root, report, report_suffix])
        report_data[mcc] = {}
        r = requests.get(file_url)
        report_data[mcc]['r_status'] = r.status_code
        if r.status_code == 200:
            mcc_json = r.json()
        else:
            mcc_json = None
        report_data[mcc]['raw_data'] = mcc_json
    return report_data

def load_raw_subjects_files(current_folder, data_folder, mcc_list):
    file_report = {}
    filename = 'subjects-[mcc]-latest.json'
    for mcc in mcc_list:
        filename_mcc = filename.replace('[mcc]',str(mcc))
        filepath = os.path.join(current_folder, data_folder, filename_mcc)
        with open(filepath , 'r') as json_file:
            file_report[str(mcc)] = json.loads(json_file.read())
    return file_report


def load_data(file_url_root, reports, mcc_list):
    local_data_store = {}
    for report in reports:
        local_data_store[report] = load_report_data(file_url_root, report, mcc_list)
    return local_data_store
