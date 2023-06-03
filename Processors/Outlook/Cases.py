from time import sleep


class Cases(object):
    def __init__(self,browser):
        self.browser = browser


    def check_cases(self,timeout = 15):
        try:
            self.browser.find_element_by_css_selector('#enforcementFrame')
            return 'Captcha'
        except:
            pass

        try:
            #print(self.browser.page_source)
            if 'Stay signed in?' in self.browser.page_source:
                return 'Success'
        except:
            pass

        try:
            if 'Your Microsoft account brings everything together' in self.browser.page_source:
                return 'Continue'
        except:
            pass
        sleep(1)