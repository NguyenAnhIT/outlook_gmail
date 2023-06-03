import os


class ProxyAuth(object):
    def __init__(self):
        pass


    def proxy_auth(self,proxy):
        try:
            usernamePrx = proxy.split(':')[2]
            passwordPrx = proxy.split(':')[3].strip('\n')
        except:
            usernamePrx = "Admin"
            passwordPrx = "Admin"

        hostPrx = proxy.split(':')[0]
        portPrx = proxy.split(':')[1]
        backgroundJS = """
                            chrome.runtime.onMessage.addListener(function(response, sender, sendResponse) {
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

                    });




                    var host = '%s';
                    var port = %s;
                    var username = '%s';
                    var password = '%s';




                    var config = {
                        mode: "fixed_servers",
                        rules: {
                          singleProxy: {
                            scheme: "http",
                            host: host,
                            port: port
                          },
                          bypassList: ["localhost"]
                        }
                      };

                    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                    return {
                        authCredentials: {
                            username: username,
                            password: password
                        }
                    };
                    }

                    chrome.webRequest.onAuthRequired.addListener(
                            callbackFn,
                            {urls: ["<all_urls>"]},
                            ['blocking']
                    );""" % (hostPrx, int(portPrx), usernamePrx, passwordPrx)
        open(os.path.join(os.getcwd(), 'Data','FakeFingerPrint', 'RAW', 'Generate', 'background.js'), 'w',
             encoding='utf8').write(
            backgroundJS)
