from selenium import webdriver

EMAIL_ADD = 's.torresf@uninades.edu.co'    # Change this to your email address
PURPOSE_MSG = 'Data adquisition for TRACE-LAC project'    # Change this to your purpose message
DRIVER_PATH = '/Users/samueltorres/Documents/Projects/TRACE_LATAM/app/model/webscrapping/chromedriver'

URL = 'http://portalsivigila.ins.gov.co/Paginas/Buscador.aspx'

class SivigilaWebScrap():

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.prefs = {"download.default_directory" : "/Users/samueltorres/Documents/Projects/TRACE_LATAM/data/Multicity/Data/Raw_data",
                      "directory_upgrade": True}
        self.options.add_experimental_option("prefs", self.prefs)
        self.driver = webdriver.Chrome(options=self.options, executable_path=DRIVER_PATH)
        self.driver.get(URL)

    def input_to_download(self):
        email_input = self.driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff11_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
        conf_email = self.driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff21_ctl00_ctl00_TextField"]').send_keys(EMAIL_ADD)
        msg_input = self.driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_ff51_ctl00_ctl00_TextField"]').send_keys(PURPOSE_MSG)

    def close_driver(self):
        self.driver.quit()

    def get_data(self, years, event_type):
        # Check if multiple years and events are selected
        one_search_years = True
        one_search_event = True

        if len(years) > 1:
            one_search_years = False
        if event_type is list:
            one_search_event = False
        
        if one_search_event is True and one_search_years is True:
            # Select event type and year
            event = self.driver.find_element_by_xpath('//*[@id="lstEvento"]').send_keys(event_type[0])
            year = self.driver.find_element_by_xpath('//*[@id="lstYear"]').send_keys(years[0])
            search = self.driver.find_element_by_xpath('//*[@id="DeltaPlaceHolderMain"]/div[1]/div[1]/div/div[2]/div/a').click()
            results = self.driver.find_element_by_xpath('//*[@id="documentos"]')
            results = results.find_element_by_tag_name('a').click()
            # Wait until window appears
            self.driver.implicitly_wait(4)
            # Switch to iframe
            lst = self.driver.find_elements_by_xpath('//iframe')
            self.driver.switch_to.frame(lst[2])
            # Input data
            self.input_to_download()
            # Click and save
            save = self.driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_savebutton2_ctl00_diidIOSaveItem"]').click()
        
        elif one_search_event is False and one_search_years is True:
            for event_i in event_type:
                # Select event type and year
                event = self.driver.find_element_by_xpath('//*[@id="lstEvento"]').send_keys(event_i)
                year = self.driver.find_element_by_xpath('//*[@id="lstYear"]').send_keys(years)
                search = self.driver.find_element_by_xpath('//*[@id="DeltaPlaceHolderMain"]/div[1]/div[1]/div/div[2]/div/a').click()
                results = self.driver.find_element_by_xpath('//*[@id="documentos"]')
                results = results.find_element_by_tag_name('a').click()
                # Wait until window appears
                self.driver.implicitly_wait(4)
                # Switch to iframe
                lst = self.driver.find_elements_by_xpath('//iframe')
                self.driver.switch_to.frame(lst[2])
                # Input data
                self.input_to_download()
                # Click and save
                save = self.driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_savebutton2_ctl00_diidIOSaveItem"]').click()
                # Switch to main window
                self.driver.switch_to.default_content()

        elif one_search_event is True and one_search_years is False:
            for year_i in years:
                # Select event type and year
                event = self.driver.find_element_by_xpath('//*[@id="lstEvento"]').send_keys(event_type)
                year = self.driver.find_element_by_xpath('//*[@id="lstYear"]').send_keys(year_i)
                search = self.driver.find_element_by_xpath('//*[@id="DeltaPlaceHolderMain"]/div[1]/div[1]/div/div[2]/div/a').click()
                results = self.driver.find_element_by_xpath('//*[@id="documentos"]')
                results = results.find_element_by_tag_name('a').click()
                # Wait until window appears
                self.driver.implicitly_wait(4)
                # Switch to iframe
                lst = self.driver.find_elements_by_xpath('//iframe')
                self.driver.switch_to.frame(lst[2])
                # Input data
                self.input_to_download()
                # Click and save
                save = self.driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_savebutton2_ctl00_diidIOSaveItem"]').click()
                # Switch to main window
                self.driver.switch_to.default_content()
  
        elif one_search_event is False and one_search_years is False:
            for event_i in event_type:
                for year_i in years:
                    # Select event type and year
                    event = self.driver.find_element_by_xpath('//*[@id="lstEvento"]').send_keys(event_i)
                    year = self.driver.find_element_by_xpath('//*[@id="lstYear"]').send_keys(year_i)
                    search = self.driver.find_element_by_xpath('//*[@id="DeltaPlaceHolderMain"]/div[1]/div[1]/div/div[2]/div/a').click()
                    results = self.driver.find_element_by_xpath('//*[@id="documentos"]')
                    results = results.find_element_by_tag_name('a').click()
                    # Wait until window appears
                    self.driver.implicitly_wait(4)
                    # Switch to iframe
                    lst = self.driver.find_elements_by_xpath('//iframe')
                    self.driver.switch_to.frame(lst[2])
                    # Input data
                    self.input_to_download()
                    # Click and save
                    save = self.driver.find_element_by_xpath('//*[@id="ctl00_ctl40_g_a10db170_03d5_46af_9ccb_ba316e1ce046_savebutton2_ctl00_diidIOSaveItem"]').click()
                    # Switch to main window
                    self.driver.switch_to.default_content()
        
