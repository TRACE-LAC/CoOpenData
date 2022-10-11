import sys
import os.path
from tqdm import tqdm
import os
import csv
import pandas as pd
# import config as cf
from webscrapping.SivigilaWebScrap import SivigilaWebScrap
from utils import data_utils
# assert cf

def download_sivigila_data(years, events):
    '''
    Downloads data from Sivigila website and saves it in a csv file in the data folder.
    '''
    scrapper = SivigilaWebScrap()
    scrapper.get_data(years, events)
    return scrapper


def exit_server(scrapper):
    '''
    TODO Exits the server.
    '''
    scrapper.close_driver()


def preprocess_sivigila_data(years, events, data_path):
    '''
    Preprocesses the data downloaded from Sivigila website.
    '''
    # Files are saved with event code and year as name (but names differ).
    file_by_format = {}   # {code_year: file_name}
    dl_files_lst = os.listdir(data_path)
    for file in dl_files_lst:
        name, ext = os.path.splitext(file)
        if ext == '.csv':
            code_file = sorted(name.split('_'),key=len)[0]
            year_file = sorted(name.split('_'),key=len)[1]
            file_by_format[code_file + '_' + year_file] = file

    # Get columms names to save
    cols_save = data_utils.sivigila_data_cols()
    age_dict = data_utils.age_sivigila_to_real()

    # Read files and merge them
    df_lst = []
    for year in tqdm(years, total=len(years), desc= 'Preprocessing data', leave=True):
        # Get columns to save
        # print('Preprocessing year {}'.format(year))
        cols_save_year = data_utils.sivigila_cols_per_year(year)
        cols_save_year_k = list(cols_save_year.keys())
        
        for event in tqdm(events, total=len(events), desc= f'Year: {year} ', leave=False):
            event_code = data_utils.event_to_code(event)
            file_name_i = file_by_format[event_code + '_' + year]
            # Read file
            print('\nReading file: ', file_name_i)
            df = data_utils.read_sivigila_csv(data_path, file_name_i, 
                                        cols_to_read=cols_save_year_k, cols_rename=cols_save_year,
                                        age_dict=age_dict)

            if len(years) > 1 or len(events) > 1:   # If there are more than one year or event
                df_lst.append(df)
            else:
                continue
    if len(years) > 1 or len(events) > 1:
        df_out = pd.concat(df_lst)
    else:
        df_out = df

    # Generate save name
    save_name = ''
    for event in events:
        save_name += data_utils.event_to_code(event) + '_'
    year_save = years if len(years) < 1 else years[0] + '-' + years[-1]
    save_name = save_name + '(' + year_save + ')' + '.csv'

    return df_out, save_name


def preprocess_cesus_household(data_path, save_path, save=True):
    ''' Preprocesses the data downloaded from CESUS website.
    '''
        
    # Social status
    viviendas2018_estrato = pd.read_excel(os.path.join(data_path, 'VIVIENDAS_Cuadros_CNPV_2018.XLSX'), skiprows=1, sheet_name=['10V_MPIO'])
    viviendas2018_estrato = viviendas2018_estrato['10V_MPIO'].fillna(method='ffill')
    viviendas2018_estrato = viviendas2018_estrato.ffill(axis = 1)
    if save is True:
        viviendas2018_estrato.to_csv(os.path.join(save_path,'estrato_energia.csv'),index=False)

    # Sanitary services
    viviendas2018_sanitarios = pd.read_excel(os.path.join(data_path, 'VIVIENDAS_Cuadros_CNPV_2018.XLSX'), skiprows=9, sheet_name=['9V_MPIO'])
    viviendas2018_sanitarios = viviendas2018_sanitarios['9V_MPIO'].fillna(method='ffill')
    viviendas2018_sanitarios = viviendas2018_sanitarios.ffill(axis = 1)
    if save is True:
        viviendas2018_sanitarios.to_csv(os.path.join(save_path,'servicios_sanitarios.csv'),index=False)

    # Public services
    viviendas2018_spublicos = pd.read_excel(os.path.join(data_path, 'VIVIENDAS_Cuadros_CNPV_2018.XLSX'), skiprows=10, sheet_name=['8V_MPIO'])
    viviendas2018_spublicos = viviendas2018_spublicos['8V_MPIO'].fillna(method='ffill')
    viviendas2018_spublicos = viviendas2018_spublicos.ffill(axis = 1)
    if save is True:
        viviendas2018_spublicos.to_csv(os.path.join(save_path,'servicios_publicos.csv'),index=False)

    # Floor construction materials
    viviendas2018_floormat = pd.read_excel(os.path.join(data_path, 'VIVIENDAS_Cuadros_CNPV_2018.XLSX'), skiprows=10, sheet_name=['7V_MPIO'])
    viviendas2018_floormat = viviendas2018_floormat['7V_MPIO'].fillna(method='ffill')
    viviendas2018_floormat = viviendas2018_floormat.ffill(axis = 1)
    if save is True:
        viviendas2018_floormat.to_csv(os.path.join(save_path,'materiales_pisos_hogares.csv'),index=False)

    # Wall construction materials
    areas_wallmat = {
    'total' : 'A:M',
    'cabecera' : 'A:C,N:W',
    'centro_poblado' : 'A:C,X:AG',
    'rural_disperso' : 'A:C,AH:AQ'
    }
    for a in areas_wallmat:
        viviendas2018_wallmat = pd.read_excel(os.path.join(data_path, 'VIVIENDAS_Cuadros_CNPV_2018.XLSX'), 
                                            skiprows=11, 
                                            sheet_name=['6V_MPIO'],
                                            usecols = areas_wallmat[a]
                                            )
        viviendas2018_wallmat = viviendas2018_wallmat['6V_MPIO'].fillna(method='ffill')
        viviendas2018_wallmat = viviendas2018_wallmat.ffill(axis = 1)
        viviendas2018_wallmat.to_csv(os.path.join(save_path,'materiales_paredes_hogares_{}.csv'.format(a)),
                                    index=False)

    # Household size
    viviendas2018_floormat = pd.read_excel(os.path.join(data_path, 'VIVIENDAS_Cuadros_CNPV_2018.XLSX'), skiprows=10, sheet_name=['5V_MPIO'])
    viviendas2018_floormat = viviendas2018_floormat['5V_MPIO'].fillna(method='ffill')
    viviendas2018_floormat = viviendas2018_floormat.ffill(axis = 1)
    viviendas2018_floormat.to_csv(os.path.join(save_path,'tamano_hogares.csv'),index=False)

    return None


def preprocess_cesus_demographic(data_path, save_path, save=True):
    ''' Preprocesses the data downloaded from CESUS website.
    '''

    # Gender distribution
    areas_sexo = {
    'total' : 'A:G',
    'cabecera' : 'A:D,H:J',
    'centro_poblado' : 'A:D,K:M',
    'rural_disperso' : 'A:D,N:P'
    }
    for a in areas_sexo:
        demografico2018_sexo = pd.read_excel(os.path.join(data_path, 'PERSONAS_DEMOGRAFICO_Cuadros_CNPV_2018.xlsx'), 
                                            skiprows=10, 
                                            sheet_name=['3PM'],
                                            usecols = areas_sexo[a]
                                            )
        demografico2018_sexo = demografico2018_sexo['3PM'].fillna(method='ffill')
        demografico2018_sexo = demografico2018_sexo.ffill(axis = 1)
        demografico2018_sexo.to_csv(os.path.join(save_path,'distribucion_edades_municipal_area_{}.csv'.format(a)),
                                    index=False)

    # Household size distribution
    viviendas2018_floormat = pd.read_excel(os.path.join(data_path, 'VIVIENDAS_Cuadros_CNPV_2018.XLSX'), skiprows=10, sheet_name=['5V_MPIO'])
    viviendas2018_floormat = viviendas2018_floormat['5V_MPIO'].fillna(method='ffill')
    viviendas2018_floormat = viviendas2018_floormat.ffill(axis = 1)
    viviendas2018_floormat.to_csv(os.path.join(save_path,'tamano_hogares.csv'),index=False)

    return None


def preprocess_cesus_social():
    return None