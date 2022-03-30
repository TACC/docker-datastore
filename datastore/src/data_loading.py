import traceback

import os
import numpy as np
import pandas as pd


# ----------------------------------------------------------------------------
# DATA DISPLAY DICTIONARIES
# ----------------------------------------------------------------------------
def load_display_terms(ASSETS_PATH, display_terms_file):
    try:
        display_terms = pd.read_csv(os.path.join(ASSETS_PATH, display_terms_file))

        # Get display terms dictionary for one-to-one records
        display_terms_uni = display_terms[display_terms.multi == 0]
        display_terms_dict = get_display_dictionary(display_terms_uni, 'api_field', 'api_value', 'display_text')

        # Get display terms dictionary for one-to-many records
        display_terms_multi = display_terms[display_terms.multi == 1]
        display_terms_dict_multi = get_display_dictionary(display_terms_multi, 'api_field', 'api_value', 'display_text')

        return display_terms, display_terms_dict, display_terms_dict_multi
    except Exception as e:
        traceback.print_exc()
        return None

def get_display_dictionary(display_terms, api_field, api_value, display_col):
    '''from a dataframe with the table display information, create a dictionary by field to match the database
    value to a value for use in the UI '''
    try:
        display_terms_list = display_terms[api_field].unique() # List of fields with matching display terms

        # Create a dictionary using the field as the key, and the dataframe to map database values to display text as the value
        display_terms_dict = {}
        for i in display_terms_list:
            term_df = display_terms[display_terms.api_field == i]
            term_df = term_df[[api_value,display_col]]
            term_df = term_df.rename(columns={api_value: i, display_col: i + '_display'})
            term_df = term_df.apply(pd.to_numeric, errors='ignore')
            display_terms_dict[i] = term_df
        return display_terms_dict

    except Exception as e:
        traceback.print_exc()
        return None


# ----------------------------------------------------------------------------
# SUBJECTS API DATA
# ----------------------------------------------------------------------------
def get_subjects_data_from_local_file(DATA_PATH, mcc_list):
    '''Read subjects json files, iteratthing through MCC in list as data is stored in separate files.
    Concatenate into single dataframe'''
    subjects_data = pd.DataFrame()
    for mcc in mcc_list:
        try:
            mcc_file = ''.join(['subjects-',str(mcc),'-latest.json'])
            mcc_filepath = os.path.join(DATA_PATH,'subjects', mcc_file)
            mcc_data = pd.read_json(mcc_filepath, orient='index').reset_index()
            mcc_data['mcc'] = mcc
            if subjects_data.empty:
                subjects_data = mcc_data
            else:
                subjects_data = pd.concat([subjects_data, mcc_data])
        except Exception as e:
            traceback.print_exc()
            subjects_data = subjects_data
    return subjects_data


def extract_adverse_effects_data(subjects_data):
    '''Extract data with multiple values (stored as 'adverse effects' column) from the subjects data.
    Adverse effects data is stored in a nested dictionary format - this function unpacks that.'''
    index_cols = ['index','main_record_id', 'mcc']
    # reset index using index_cols
    subjects_data = subjects_data.set_index(index_cols)
    # Extract multi data values
    multi_df = subjects_data[['adverse_effects']].dropna()
    # Convert from data frame back to dict
    multi_dict = multi_df.to_dict('index')
    # Turn dict into df with multi=index and reset_index
    multi = pd.DataFrame.from_dict({(i,k): multi_dict[i][j][k]
                               for i in multi_dict.keys()
                               for j in multi_dict[i].keys()
                               for k in multi_dict[i][j].keys()
                           },
                           orient='index')
    # Replace empty strings with NaN
    multi = multi.replace(r'^\s*$', np.nan, regex=True)
    multi = multi.reset_index()
    multi[index_cols] = pd.DataFrame(multi['level_0'].tolist(), index=multi.index)
    multi['instance'] = multi['level_1']
    multi.drop(['level_0', 'level_1'], axis=1, inplace=True)
    # Move index columns to start of dataframe
    multi = multi[index_cols + list(extract_adverse_effects_data(multi).columns.drop(index_cols))]
    return multi


# ----------------------------------------------------------------------------
# CLEAN THE SUBJECTS DATA FRAME
# ----------------------------------------------------------------------------

def clean_subjects_data(subjects_data, display_terms_dict, drop_cols_list =['adverse_effects']):
    '''Take the raw subjects data frame and clean it up'''
    # Drop adverse events column
    subjects_data = subjects_data.drop(columns=drop_cols_list)
    # Convert all string 'N/A' values to nan values
    subjects_data = subjects_data.replace('N/A', np.nan)

    # Handle 1-many dem_race, take multi-select values and convert to 8
    if not np.issubdtype(subjects_data['dem_race'].dtype, np.number):
        subjects_data['dem_race_original'] = subjects_data['dem_race']
        subjects_data.loc[(subjects_data.dem_race.str.contains('|', regex=False, na=False)),'dem_race']='8'

    # Coerce numeric values to enable merge
    subjects_data = subjects_data.apply(pd.to_numeric, errors='ignore')

    # Merge columns on the display terms dictionary to convert from database terminology to user terminology
    for i in display_terms_dict.keys():
        if i in subjects_data.columns: # Merge columns if the column exists in the dataframe
            display_terms = display_terms_dict[i]
            if subjects_data[i].dtype == np.float64:
                # for display columns where data is numeric, merge on display dictionary, treating cols as floats to handle nas
                display_terms[i] = display_terms[i].astype('float64')
            subjects_data = subjects_data.merge(display_terms, how='left', on=i)

    # convert date columns from object --> datetime datatypes as appropriate
    datetime_cols_list = ['date_of_contact','date_and_time','obtain_date','ewdateterm','sp_surg_date','sp_v1_preop_date','sp_v2_6wk_date','sp_v3_3mo_date'] #erep_local_dtime also dates, but currently an array
    subjects_data[datetime_cols_list] = subjects_data[datetime_cols_list].apply(pd.to_datetime, errors='coerce')

    return subjects_data
