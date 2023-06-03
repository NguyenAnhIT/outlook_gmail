import json
import os.path
import random

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .Cases import Cases
from ..Helper import Helper
from time import sleep

class Outlook(object):
    def __init__(self):
        self.configs = open(os.path.join(os.getcwd(),'Data','configs.json')).read()
        self.configs = json.loads(self.configs)


    def register(self,browser,username,password):
        self.browser = browser
        self.helper = Helper(browser=self.browser)
        self.browser.get('https://signup.live.com/signup')
        sleep(1)
        self.helper.send_keys(element='#MemberName',value=username)
        sleep(1)
        self.browser.find_element_by_css_selector('#iSignupAction').click()
        sleep(2)
        self.helper.send_keys(element='#PasswordInput',value=password)
        sleep(1)
        self.browser.find_element_by_css_selector('#iSignupAction').click()
        sleep(2)
        fist_name,last_name = self.name_generator()
        self.helper.send_keys(element='#FirstName',value=fist_name)
        sleep(1)
        self.browser.find_element_by_css_selector('#LastName').send_keys(last_name)
        sleep(1)
        self.browser.find_element_by_css_selector('#iSignupAction').click()
        sleep(2)

        self.helper.finding(element='#Country')

        countrys = Select(self.browser.find_element(By.ID, "Country"))
        countrys.select_by_value('US')
        sleep(1)
        days = Select(self.browser.find_element(By.ID, "BirthDay"))
        months = Select(self.browser.find_element(By.ID, "BirthMonth"))
        months.select_by_value(str(random.randint(1, 12)))
        sleep(1)
        days.select_by_value(str(random.randint(1, 30)))
        sleep(0.5)
        self.browser.find_element_by_css_selector('#BirthYear').send_keys(random.randint(1985, 2000))
        sleep(1)
        self.browser.find_element_by_css_selector('#iSignupAction').click()
        sleep(5)
        return 'Send Inbox'


    def send_code(self,browser,code):
        try:
            self.browser = browser
            self.helper = Helper(browser=self.browser)
            sleep(1)
            self.browser.find_element_by_css_selector('input[name="VerificationCode"]').send_keys(code)
            sleep(1)
            self.browser.find_element_by_css_selector('#iSignupAction').click()
            sleep(3)
            cases = Cases(browser=self.browser)
            while True:
                check = cases.check_cases()
                if check == 'Captcha':
                    self.auto_captcha()
                    self.helper.checkPagesLoad()
                    #print('a')
                elif check == 'Success':
                    self.browser.find_element_by_css_selector('#idSIButton9').click()
                    sleep(5)
                    return 'Success'
                elif check == 'Continue':
                    self.browser.find_element_by_css_selector('button').click()
                    self.helper.checkPagesLoad()
                    sleep(2)



        except:
            # import traceback
            # traceback.print_exc()
            pass

    def processGetTokenAnyCaptcha(self, timeout=3):
        sleep(timeout)
        url = "https://api.anycaptcha.com/getTaskResult"
        payloads = {
            "clientKey": self.apiAnycaptcha,
            "taskId": int(self.taskID)
        }
        response = requests.post(url, json=payloads).json()
        if response.get("status", '') == "ready" and response["errorId"] == 0:
            return response["solution"]["token"]
        elif response.get("status", '') == "processing" and response["errorId"] == 0:
            return self.processGetTokenAnyCaptcha(timeout=3)
        elif response['errorId'] == 1:
            self.processGetTaskAnyCaptcha()
            return self.processGetTokenAnyCaptcha(timeout=3)
        else:
            print('Hệ thống anycaptcha đang gặp lỗi !')
            exit()

    def processGetTaskAnyCaptcha(self):
        self.apiAnycaptcha = self.configs['api_anycaptcha']
        payloads = {
            "clientKey": f"{self.apiAnycaptcha}",
            "task": {
                "type": "FunCaptchaTaskProxyless",
                "websiteURL": "https://signup.live.com/signup?lic=1&uaid=9b23f83c11f440f8993626a59f3aac7f",
                "websitePublicKey": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
            }
        }
        response = requests.post("https://api.anycaptcha.com/createTask", json=payloads).json()
        taskId = response.get('taskId', '')
        if bool(taskId):
            self.taskID = taskId
        else:
            return self.processGetTaskAnyCaptcha()


    def auto_captcha(self):
        self.processGetTaskAnyCaptcha()
        sleep(1)
        token = self.processGetTokenAnyCaptcha()
        print(token)
        self.browser.execute_script("""var anyCaptchaToken = '%s';
var enc = document.getElementById('enforcementFrame');
var encWin = enc.contentWindow || enc;
var encDoc = enc.contentDocument || encWin.document;
let script = encDoc.createElement('SCRIPT');
script.append('function AnyCaptchaSubmit(token) { parent.postMessage(JSON.stringify({ eventId: "challenge-complete", payload: { sessionToken: token } }), "*") }');
encDoc.documentElement.appendChild(script);
encWin.AnyCaptchaSubmit(anyCaptchaToken);"""%(token))
        sleep(6)



    def name_generator(self):
        first_name = ['Harold','Charles','Miranda','Max J','Michael','Bessie','Elsa W','Albert','Ernestine','Mary R','Marcia']
        last_name = ['Garland','Shelly','French','Burdine','McLelland','Qualls','Kramer','Fenster','Robertson','Sinha','Gutierrez','Norman']
        return first_name[random.randint(0,len(first_name)-1)],last_name[random.randint(0,len(last_name)-1)]





