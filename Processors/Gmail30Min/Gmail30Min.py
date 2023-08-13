import requests


class Gmail30Min(object):
    def __init__(self):
        pass






    def get_new_gmail(self,token):
        url = f'https://gmail30min.com/api/san-pham/mua2?token={token}&category=4&quantity=1'
        response = requests.get(url).json()
        account = response['success']['products'][0]
        return account
