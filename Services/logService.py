from getmac import get_mac_address
import requests
from Const import LOG_URL

'''
프로세스 항목 전송
'''
def send_process_log(param) :

    payload = {
        "device": get_mac_address(),
        "process" : param
    }
    response = requests.post(LOG_URL, json=payload)
    if response.status_code == 200 :
        return True
    else : return False