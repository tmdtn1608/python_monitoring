from getmac import get_mac_address
import requests
from Services.settingService import settingService

'''
로그인/로그아웃 정보 보내기
'''
def send_history(param) -> bool:
    setting = settingService()
    mac_address = get_mac_address()
    payload = {
        "mac": mac_address,
        "actType" : param
    }
    response = requests.post(setting.Config["HISTORY_URL"], json=payload)
    if response.status_code == 200 :
        return True
    else : return False
