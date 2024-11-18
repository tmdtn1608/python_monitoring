from getmac import get_mac_address
import requests
from Services.settingService import settingService

'''
프로세스 항목 전송
'''
def send_process_log(param) :
    setting = settingService()
    payload = {
        "device": get_mac_address(),
        "process" : param
    }
    response = requests.post(setting.Config["LOG_URL"], json=payload)
    if response.status_code == 200 :
        return True
    else : return False