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