from time import sleep


class Cases(object):
    def __init__(self,browser):
        self.browser = browser


    def check_cases(self,timeout=10):
        for i in range(timeout):
            try:
                self.browser.find_element_by_css_selector('div[data-challengetype="12"]')
                return 'EmailBackup'
            except:
                pass
            try:
                if 'account' not in str(self.browser.current_url).lower() and 'mail' in str(self.browser.current_url).lower():
                    return 'Login Success'
            except:
                pass




            sleep(1)
        return False
