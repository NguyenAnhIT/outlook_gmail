from .Cases import Cases
from ..Helper import Helper
from time import sleep


class Gmail(object):
    def __init__(self):

        pass

    def login(self,browser,username,password,email_backup):
        self.browser = browser
        self.helper = Helper(browser=self.browser)
        self.gmail_cases = Cases(browser=self.browser)
        self.browser.get('https://gmail.com')
        self.helper.send_keys(element='input[type="email"]',value=username)
        sleep(1)
        self.browser.find_elements_by_css_selector('button[jscontroller="soHxf"]')[1].click()
        sleep(2)
        self.helper.send_keys(element='input[type="password"]',value=password)
        sleep(1)
        try:
            self.browser.find_elements_by_css_selector('button[jscontroller="soHxf"]')[1].click()
        except:
            pass
        sleep(3)
        check_case = self.gmail_cases.check_cases()
        if check_case == 'EmailBackup':
            self.browser.find_element_by_css_selector('div[data-challengetype="12"]').click()
            sleep(2)
            self.helper.send_keys(element='input[type="email"]',value=email_backup)
            sleep(1)
            self.browser.find_element_by_css_selector('button[jscontroller="soHxf"]').click()
            sleep(6)
            self.browser.get('https://gmail.com')
            return 'Login Success'
        elif check_case == 'Login Success':
            return 'Login Success'



    def check_inbox(self,browser,count=5):
        if count<1:return False
        try:
            self.browser = browser
            self.browser.get('https://mail.google.com/mail/u/0/#search/Microsoft+account+Veirfy+your+email+address')
            sleep(8)
            div_main = self.browser.find_element_by_css_selector('div[role="main"]')
            list_tr = div_main.find_elements_by_css_selector('tr')
            for tr in list_tr:
                if 'Verify your email address' in tr.text:
                    tr.click()
                    break
            sleep(5)
            code = self.get_code_from_inbox()
            if len(code)>3:
                return code
            else:
                return self.check_inbox(browser=browser,count=count-1)

        except:
            # import traceback
            # traceback.print_exc()
            sleep(2)
            return self.check_inbox(browser=browser,count=count-1)

    def get_code_from_inbox(self):
        list_tr = self.browser.find_elements_by_css_selector('tr')
        list_tr = list_tr[::-1]
        for tr in list_tr:
            #print(tr.text)
            if 'address use this security code' in tr.text:
                code = tr.text.split(':')[1]
                return code




