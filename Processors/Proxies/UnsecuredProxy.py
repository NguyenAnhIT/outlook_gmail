import os


class UnsecuredProxy(object):
    def __init__(self):
        pass





    def unsecured_proxy(self):
        background = """chrome.runtime.onMessage.addListener(function(response, sender, sendResponse) {
                        if (response.message == 'deleteAll'){

                            chrome.browsingData.remove({
                                "since": 0
                              }, {
                                "appcache": true,
                                "cache": true,
                                "cookies": true,
                                "downloads": true,
                                "fileSystems": true,
                                "formData": true,
                                "history": true,
                                "indexedDB": true,
                                "localStorage": true,
                                "pluginData": true,
                                "passwords": true,
                                "webSQL": true
                              });
                        }

                    });"""
        open(os.path.join(os.getcwd(), 'Data','FakeFingerPrint', 'RAW', 'Generate', 'background.js'), 'w',
             encoding='utf8').write(
            background)
