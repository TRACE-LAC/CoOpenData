import sys
import os
import os.path

# import config as cf
import model
# assert cf



def download_sivigila_data(years, events):
    '''
    Downloads data from Sivigila website and saves it in a csv file in the data folder.
    '''
    scrapper = model.download_sivigila_data(years, events)


def exit_server(scrapper):
    '''
    TODO Exits the server.
    '''
    model.exit_server(scrapper)


def preprocess_sivigila_data(years, events, years_save, save=True, data_path='data/Multicity/Data', save_path='data/Census_2017-2018/Raw/DEMOGRAFICO'):
    '''
    Preprocesses the data downloaded from Sivigila website.
    '''
    raw_data_path = os.path.join(os.path.abspath(os.getcwd())
                                        , data_path, 'Raw_data')
    data_clean, save_name = model.preprocess_sivigila_data(years, events, raw_data_path)
    if save:
        # Create folder for clean data
        clean_data_path = os.path.join(os.path.abspath(os.getcwd())
                                        , data_path, 'Clean_data')
        this_folder_events = ''
        for event in events:
            if ' ' in event:
                event = event.replace(' ', '-')
            this_folder_events += event + '_'
        save_dir = this_folder_events + '(' + str(years_save) + ')'
        if not os.path.isdir(os.path.join(clean_data_path, save_dir)):
            os.makedirs(os.path.join(clean_data_path, save_dir))
        # Save data as csv
        data_clean.to_csv(os.path.join(clean_data_path, save_dir, save_name), index=False)
    
    return data_clean, save_name


def preprocess_cesus_household( save=True, data_path='data/Census_2017-2018/Raw', save_path='data/Census_2017-2018/Clean_data/VIVIENDAS', save_data=True):
    '''
    Preprocesses the data downloaded from CENSUS website.
    '''
    raw_data_path = os.path.join(os.path.abspath(os.getcwd())
                                        , data_path)
    save = False
    if save_data is True:
        save = True
    if save is True:
        # Create folder for clean data
        clean_data_path = os.path.join(os.path.abspath(os.getcwd())
                                        , save_path, 'Clean_data')
        if not os.path.isdir(os.path.join(clean_data_path, clean_data_path)):
            os.makedirs(os.path.join(clean_data_path, clean_data_path))
    
    model.preprocess_cesus_household(raw_data_path, save_path, save=True)
    
    return save_path


def preprocess_cesus_demographic( save=True, data_path='data/Census_2017-2018/Raw', save_path='data/Census_2017-2018/Clean_data/DEMOGRAFICO', save_data=True):
    '''
    Preprocesses the data downloaded from CENSUS website.
    '''
    raw_data_path = os.path.join(os.path.abspath(os.getcwd())
                                        , data_path)
    save = False
    if save_data is True:
        save = True
    if save is True:
        # Create folder for clean data
        clean_data_path = os.path.join(os.path.abspath(os.getcwd())
                                        , save_path, 'Clean_data')
        if not os.path.isdir(os.path.join(clean_data_path, clean_data_path)):
            os.makedirs(os.path.join(clean_data_path, clean_data_path))
    
    model.preprocess_cesus_household(raw_data_path, save_path, save=True)
    
    return save_path