from time import sleep


class Helper(object):
    def __init__(self,browser):
        self.browser = browser
















    def click(self, element, timeout=15, index=0):
        check = False
        for i in range(0, timeout):
            try:
                self.browser.find_elements_by_css_selector(element)[index].click()
                check = True
                break
            except:
                sleep(1)
        return check

    def send_keys(self, element, value, timeout=15, index=0):
        check = False
        for i in range(0, timeout):
            try:
                self.browser.find_elements_by_css_selector(element)[index].send_keys(str(value))
                check = True
                break
            except:
                sleep(1)
        return check

    def finding(self, element, timeout=15, index=0):
        check = False
        for i in range(0, timeout):
            try:
                valueFound = self.browser.find_elements_by_css_selector(element)[index]
                check = True
                break
            except:
                sleep(1)

        return check


    def checkPagesLoad(self):
        self.browser.execute_script("""
                                        window.addEventListener('load', function() {
                                  var divs = document.createElement('div');
                                  divs.id = 'loaded-excute-script';
                                  document.body.appendChild(divs)
                                });""")

        self.finding('#loaded-excute-script')




