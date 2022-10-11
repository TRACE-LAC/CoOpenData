
from selenium import webdriver

EMAIL_ADD = 's.torresf@uninades.edu.co'    # Change this to your email address
PURPOSE_MSG = 'Data adquisition for TRACE-LAC project'    # Change this to your purpose message
DRIVER_PATH = '/Users/samueltorres/Documents/Projects/TRACE_LATAM/app/model/webscrapping/chromedriver'

URL = 'http://portalsivigila.ins.gov.co/Paginas/Buscador.aspx'

def extract_sivigila_data(years, events):
    '''
    Downloads data from Sivigila website and saves it in a csv file in the data folder.
    '''
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    prefs = {"download.default_directory" : "/Users/samueltorres/Documents/Projects/TRACE_LATAM/data/Multicity/Data/Raw_data",
             "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(URL)

    # Check if multiple years and events are selected
    one_search_years = True
    one_search_event = True

    if len(years) > 1:
        one_search_years = False
    if len(events) > 1:
        one_search_event = False
    
    if one_search_event is True and one_search_years is True:
        # Select event type and year
        event = driver.find_element_by_xpath('//*[@id="lstEvento"]').send_keys(events[0])
        year = driver.find_element_by_xpath('//*[@id="lstYear"]').send_keys(years[0])
        search = driver.find_element_by_xpath('//*[@id="DeltaPlaceHolderMain"]/div[1]/div[1]/div/div[2]/div/a').click()
        results = driver.find_element_by_xpath('//*[@id="documentos"]')
        results = results.find_element_by_tag_name('a').click()
        # Wait until window appears
        driver.implicitly_wait(4)
        # Switch to iframe
        lst = driver.find_elements_by_xpath('//iframe')
        driver.switch_to.frame(lst[2])
        # Input data
        email_input = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff11_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
        conf_email = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff21_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
        msg_input = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff51_ctl00_ctl00_TextField"]').send_keys(PURPOSE_MSG)
        # Click and save
        save = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_savebutton2_ctl00_diidIOSaveItem"]').click()
        # Close driver
        driver.quit()
    
    elif one_search_event is False and one_search_years is True:
        for event_i in events:
            driver.implicitly_wait(4)
            # Select event type and year
            event = driver.find_element_by_xpath('//*[@id="lstEvento"]').send_keys(event_i)
            year = driver.find_element_by_xpath('//*[@id="lstYear"]').send_keys(years)
            search = driver.find_element_by_xpath('//*[@id="DeltaPlaceHolderMain"]/div[1]/div[1]/div/div[2]/div/a').click()
            results = driver.find_element_by_xpath('//*[@id="documentos"]')
            results = results.find_element_by_tag_name('a').click()
            # Wait until window appears
            driver.implicitly_wait(4)
            # Switch to iframe
            lst = driver.find_elements_by_xpath('//iframe')
            driver.switch_to.frame(lst[2])
            # Input data
            email_input = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff11_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
            conf_email = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff21_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
            msg_input = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff51_ctl00_ctl00_TextField"]').send_keys(PURPOSE_MSG)
            # Click and save
            save = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_savebutton2_ctl00_diidIOSaveItem"]').click()
            # Switch to main window
            driver.switch_to.default_content()
        # Close driver
        driver.quit()

    elif one_search_event is True and one_search_years is False:
        for year_i in years:
            driver.implicitly_wait(4)
            # Select event type and year
            event = driver.find_element_by_xpath('//*[@id="lstEvento"]').send_keys(events)
            year = driver.find_element_by_xpath('//*[@id="lstYear"]').send_keys(year_i)
            search = driver.find_element_by_xpath('//*[@id="DeltaPlaceHolderMain"]/div[1]/div[1]/div/div[2]/div/a').click()
            results = driver.find_element_by_xpath('//*[@id="documentos"]')
            results = results.find_element_by_tag_name('a').click()
            # Wait until window appears
            driver.implicitly_wait(4)
            # Switch to iframe
            lst = driver.find_elements_by_xpath('//iframe')
            driver.switch_to.frame(lst[2])
            # Input data
            email_input = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff11_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
            conf_email = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff21_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
            msg_input = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff51_ctl00_ctl00_TextField"]').send_keys(PURPOSE_MSG)
            # Click and save
            save = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_savebutton2_ctl00_diidIOSaveItem"]').click()
            # Switch to main window
            driver.switch_to.default_content()
        # Close driver
        driver.quit()

    elif one_search_event is False and one_search_years is False:
        for event_i in events:
            for year_i in years:
                driver.implicitly_wait(4)
                # Select event type and year
                event = driver.find_element_by_xpath('//*[@id="lstEvento"]').send_keys(event_i)
                year = driver.find_element_by_xpath('//*[@id="lstYear"]').send_keys(year_i)
                search = driver.find_element_by_xpath('//*[@id="DeltaPlaceHolderMain"]/div[1]/div[1]/div/div[2]/div/a').click()
                results = driver.find_element_by_xpath('//*[@id="documentos"]')
                results = results.find_element_by_tag_name('a').click()
                # Wait until window appears
                driver.implicitly_wait(4)
                # Switch to iframe
                lst = driver.find_elements_by_xpath('//iframe')
                driver.switch_to.frame(lst[2])
                # Input data
                email_input = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff11_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
                conf_email = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff21_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
                msg_input = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff51_ctl00_ctl00_TextField"]').send_keys(PURPOSE_MSG)
                # Click and save
                save = driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_savebutton2_ctl00_diidIOSaveItem"]').click()
                # Switch to main window
                driver.switch_to.default_content()
        # Close driver
        driver.quit()
