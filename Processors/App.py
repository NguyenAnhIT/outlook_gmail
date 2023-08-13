import json
import os
import shutil
import tempfile
from random import randint
from threading import Thread
from time import sleep

import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from Processors.Proxies.ProxyAuth import ProxyAuth
from Processors.Proxies.UnsecuredProxy import UnsecuredProxy
from Processors.Helper import Helper
from Processors.Gmail.Gmail import Gmail
from Processors.Outlook.Outlook import Outlook
from Processors.Gmail30Min.Gmail30Min import Gmail30Min

class StartApp(Thread):
    def __init__(self,accounts = None,proxies = None,tableStatus=None,index = 0,index_thread = 0):
        super(StartApp, self).__init__()
        self.proxies = proxies
        self.proxy_auth = ProxyAuth()
        self.proxy_unsecured = UnsecuredProxy()
        self.list_accounts = accounts
        self.tableStatus = tableStatus
        self.index = index
        self.index_thread = index_thread
        self.email = None
        self.password = None
        self.process_gmail = Gmail()
        self.process_outlook = Outlook()
        self.process_gmail30min = Gmail30Min()
        self.configs = open(os.path.join(os.getcwd(),'Data','configs.json'),encoding='utf8').read()
        self.configs = json.loads(self.configs)





    def run(self):
        try:
            self.createBrowser()
            self.handling()
        except:
            self.closeBrowser()
            self.tableStatus.emit(self.index, 1, 'Error')
            #import traceback
            #traceback.print_exc()
            # import traceback
            # traceback.print_exc()
            if self.email and self.password:
                open('error.txt','a',encoding='utf8').write(self.email+':'+self.password+'\n')




    def createBrowser(self):
        opts = webdriver.ChromeOptions()
        caps = DesiredCapabilities().CHROME
        self.temp = os.path.normpath(tempfile.mkdtemp())
        self.tableStatus.emit(self.index,1,'Đang khởi tạo trình duyệt')
        opts.add_argument('--user-data-dir=' + self.temp)
        caps["pageLoadStrategy"] = "eager"
        opts.add_argument('--load-extension=' + os.path.join(os.getcwd(), 'Data', 'FakeFingerPrint', 'Raw'))
        opts.add_argument("--window-size=500,500")
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument("--disable-web-security")
        opts.add_argument("--disable-site-isolation-trials")
        opts.add_argument("--disable-application-cache")
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_argument(f"--window-position={self.index_thread * 300},0")
        # if self.proxies:
        #     self.proxy = self.proxies[self.index].strip('\n')
        #     self.proxy_auth.proxy_auth(proxy=self.proxy)
        # else:
        #     self.proxy_unsecured.unsecured_proxy()
        if self.proxies:
            opts.add_argument('--proxy-server=%s' % self.proxies)
        self.browser = uc.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver'), options=opts,
                                 desired_capabilities=caps)
        self.browser.get('chrome://settings/passwords')
        sleep(1)
        self.browser.execute_script("""document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section.expanded > settings-autofill-page").shadowRoot.querySelector("#passwordSection").shadowRoot.querySelector("#passwordToggle").click()""")
        sleep(0.5)
        self.browser.execute_script("""document.querySelector("body > settings-ui").shadowRoot.querySelector("#main").shadowRoot.querySelector("settings-basic-page").shadowRoot.querySelector("#basicPage > settings-section.expanded > settings-autofill-page").shadowRoot.querySelector("#passwordSection").shadowRoot.querySelector("#autosigninCheckbox").click()""")
        self.tableStatus.emit(self.index, 1, 'Đang kiểm tra')
        self.browser.get('https://browserleaks.com/canvas')
        sleep(3)


        #sleep(5000)



    def handling(self):
        try:
            if self.list_accounts:
                username = self.list_accounts[self.index].split('|')[0]
                password = self.list_accounts[self.index].split('|')[1]
                email_backup = self.list_accounts[self.index].split('|')[2].strip('\n')
            else:
                token = self.configs['key_gmail30min']
                account = self.process_gmail30min.get_new_gmail(token=token)
                username = account.split('|')[0]
                password = account.split('|')[1]
                email_backup = account.split('|')[2].strip('\n')
                self.tableStatus.emit(self.index, 0, username)
            check = self.process_gmail.login(browser=self.browser,username=username,password=password,email_backup=email_backup)
            if check == 'Login Success':
                self.tableStatus.emit(self.index, 1, 'Đăng nhập gmail thành công')
                self.browser.execute_script("window.open('');")
                sleep(0.5)
                self.browser.switch_to.window(self.browser.window_handles[-1])
                password_outlook = self.configs['password_outlook']
                check = self.process_outlook.register(browser=self.browser,username=username,password=password_outlook)
                if check == 'Send Inbox':
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    sleep(5)
                    code = self.process_gmail.check_inbox(browser=self.browser)
                    if code == False:
                        self.browser.close()
                        open('email_not_code.txt',a,encoding='utf8').write(self.list_accounts[self.index].strip('\n')+'\n')
                        self.tableStatus.emit(self.index, 1, 'Không nhận được mã code gmail !')
                        return
                    sleep(1)
                    self.browser.close()
                    sleep(0.5)
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    check = self.process_outlook.send_code(browser=self.browser,code=code)
                    if check == 'Success':
                        open('thanhcong.txt','a',encoding='utf8').write(username+'|'+password+'|'+email_backup.strip('\n')+f'|password_outlook:{password_outlook}'+'\n')
                        self.tableStatus.emit(self.index,1,'Thành công')
                        self.closeBrowser()

            else:
                self.closeBrowser()
                self.tableStatus.emit(self.index, 1, 'Email Error !')
        except:
            self.closeBrowser()
            self.tableStatus.emit(self.index, 1, 'Email Error !')









    def closeBrowser(self):
        try:
            self.browser.close()
            self.browser.quit()
            sleep(1)
            try:
                shutil.rmtree(r'%s' % (self.temp))
                print('clear')
            except:
                pass

        except:
            pass