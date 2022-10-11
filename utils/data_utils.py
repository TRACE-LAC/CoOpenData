import os
import config as cf
import pandas as pd
import numpy as np
# from config_root.config import ROOT_DIR
import json
assert cf

def convert_sivigila_to_csv(list_years, path_to_read, path_to_save):
    ''' This function turns the multi-sheets sivigila files
        saved as .xslx to a single sheet as .csv
    '''
    for year in list_years:
        file_name = 'sivigila_' + str(year) + '.xlsx'
        file_save = 'sivigila_' + str(year) + '.csv'
        # Get las sheet
        xl = pd.ExcelFile(os.path.join(path_to_read,file_name))
        if year == 2018:
            sheet_save = 'Metadatos'
        else:
            sheet_save = xl.sheet_names[-1]

        # Read xlsx
        df = pd.read_excel(os.path.join(path_to_read,file_name),
                           sheet_save,
                           index_col=None,
                           na_values=['NA'])
        # Save as csv
        df.to_csv(os.path.join(path_to_save,file_save))


def read_sivigila_csv(data_path, file_name, cols_to_read, cols_rename, age_dict):
    ''' Read the sivigila csv file and return a dataframe.
    '''
    df = pd.read_csv(os.path.join(data_path, file_name),
                     sep=None,
                     usecols=cols_to_read,
                     engine='python',
                     parse_dates=True,
                     encoding='latin-1')
    df.rename(columns=cols_rename, inplace=True)
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)    # Replace empty values with NaN
    df = date_cols_to_datetime(df)   # Convert date columns to datetime
    df = int_cols_to_int(df)         # Convert int columns to int
    df = convert_sivigila_age_to_float(df, age_dict) # Convert age to float
    df = conver_municipality_codes_to_complete(df)   # Convert municipality codes to complete codes

    return df


def read_clean_sivigila(data_path, file_name, cols_to_read):
    ''' Read Sivigila clean files and return a dataframe.
    '''
    df = pd.read_csv(os.path.join(data_path, file_name))
    return df


def get_clean_file_name(events,years):
    ''' Get clean file name given the event(s) and year(s)
    '''
    file_name = ''
    for event in events:
        event_code = event_to_code(event) # Get event code
        file_name += event_code + '_'
    year_read = years if len(years) < 1 else years[0] + '-' + years[-1]
    file_name = file_name + '(' + year_read + ')' + '.csv'
    return file_name


def get_clean_dir_name(events,years):
    ''' Get clean dir name given the event(s) and year(s)
    '''
    this_dir_events = ''
    for event in events:
        if ' ' in event:
            event = event.replace(' ', '-')
        this_dir_events += event + '_'
    year_read = years if len(years) < 1 else years[0] + '-' + years[-1]
    dir_name = this_dir_events + '(' + str(year_read) + ')'
    return dir_name


def conver_municipality_codes_to_complete(df):
    ''' Convert the municipality codes to complete codes.
    '''
    # Iterate over the rows
    df_cod_muns_c = pd.DataFrame()
    muns_c_lst = []
    for index, row in df.iterrows():
        mun_c_i = str(row['COD_MUN_O'])
        if len(mun_c_i) == 1:
            mun_c = '00' + mun_c_i
        elif len(mun_c_i) == 2:
            mun_c = '0' + mun_c_i
        else:
            mun_c = mun_c_i
        muns_c_lst.append(mun_c)
    df_cod_muns_c['COD_MUN_O_C'] = muns_c_lst
    df = pd.concat([df, df_cod_muns_c], axis=1)
    return df


def convert_sivigila_age_to_float(df, age_dict):
    ''' Convert age format in sivigila database as a float number
    '''
    # Iterate over the rows
    df_age = pd.DataFrame()
    age_lst = []
    for index, row in df.iterrows():
        age = row['EDAD']
        format_unit = row['UNI_MED']
        if age_dict[str(format_unit)]["value"] == "NA":
            real_age = np.nan
        else:
            real_age = age / int(age_dict[str(format_unit)]["value"])
        age_lst.append(real_age)
    # Drop the UNI_EDA column
    df_age['EDAD_REAL'] = age_lst
    df = pd.concat([df, df_age], axis=1)
    df.drop(columns=['UNI_MED'], inplace=True)
    return df


def date_cols_to_datetime(df,
            date_cols=["FEC_NOT","FECHA_NTO","FEC_CON","INI_SIN","FEC_HOS","FEC_DEF"]):
    ''' Convert the date columns to datetime.
    '''
    for col in date_cols:
    #     if df['ANO'][0] == 2020:
    #         df[col] = pd.to_datetime(df[col]).dt.strftime('%d/%m/%Y')
    #     else:
    #         pd.to_datetime(df[col])
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
    return df


def int_cols_to_int(df, 
            cols=["COD_EVE","SEMANA","EDAD","UNI_MED","ANO","AREA","TIP_CAS","PAC_HOS","CON_FIN","AJUSTE"]):
    ''' Convert the columns to int.
    '''

    df[cols] = df[cols].apply(pd.to_numeric)
    # pd.to_numeric(df[cols],downcast='integer')

    # for col in cols:
    #     df[col] = pd.to_numeric(df[col], downcast='integer')
        # df[col].replace(np.str, np.int64, inplace=True)
        # df[col].replace(np.int64, np.str, inplace=True)
        # df[col] = df[col].astype(int) #,errors='ignore')
        # df[col] = df[col].astype(str) #,errors='ignore')
        
    return df


def sivigila_cols_per_year(year, path_formats='/data/Multicity/Data/Formats'):
    ''' Search for the cols to pick depending on the year.
    '''
    # TODO Correct to use ROOT DIR
    cols_file = open(os.path.join(os.path.abspath(os.getcwd()) + path_formats, 
                                'sivigila_cols.json'), 'r')
    years_cols_dict = json.load(cols_file)
    # print(year)
    year_selected_dict = years_cols_dict[year]
    return year_selected_dict


def sivigila_data_cols(path_formats='/data/Multicity/Data/Formats'):
    ''' Get columns standart names (Defined as the 2020 cols).
    '''
    # TODO Correct to use ROOT DIR
    cols_file = open(os.path.join(os.path.abspath(os.getcwd()) + path_formats, 
                                'sivigila_cols.json'), 'r')
    years_cols_dict = json.load(cols_file)
    year_selected_dict = years_cols_dict['2020']
    standard_cols = list(year_selected_dict.keys())
    return standard_cols


def code_to_event(code, path_formats='/data/Multicity/Data/Formats'):
    ''' Search for the event code in the formats file and return the event name.
    '''
    # TODO Correct to use ROOT DIR
    code_to_event_file = open(os.path.join(os.path.abspath(os.getcwd()) + path_formats, 
                                'event_codes_clean.json'), 'r')
    code_to_event_dict = json.load(code_to_event_file)
    get_event = code_to_event_dict[code]
    return get_event


def event_to_code(event, path_formats='/data/Multicity/Data/Formats'):
    ''' Search for the event name in the formats file and return the event code.
    '''
    # TODO Correct to use ROOT DIR
    event_to_code_file = open(os.path.join(os.path.abspath(os.getcwd()) + path_formats, 
                                'codes_event_clean.json'), 'r')
    event_to_code_dict = json.load(event_to_code_file)
    get_code = event_to_code_dict[event]
    return get_code

def age_sivigila_to_real(path_formats='/data/Multicity/Data/Formats'):
    ''' Convert Sivigila age to real age.
    '''
    # TODO Correct to use ROOT DIR
    age_file = open(os.path.join(os.path.abspath(os.getcwd()) + path_formats, 
                                'age_classification.json'), 'r')
    age_dict = json.load(age_file)
    return age_dict