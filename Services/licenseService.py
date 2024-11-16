import keyring
from getmac import get_mac_address
import requests
from Services.settingService import settingService


def get_license_info() -> str | None :
    license_info = keyring.get_password("system", "username")
    return license_info

'''
라이센스 등록.
'''
def set_license_info(license : str) :
    setting = settingService()
    
    # license, mac_address 전송
    mac_address = get_mac_address()
    payload = {
        "license": license,
        "mac": mac_address
    }
    response = requests.post(setting.Config["LICENSE_REGIST_URL"], json=payload)
    data = response.json()
    value = data.get('result')
    if (value == True) :
        keyring.set_password("system","username",license)
    else : 
        return

def reset_license() :
    keyring.delete_password("system","username")

'''
라이센스 유효성 체크
'''
def check_license() :
    setting = settingService()
    
    license = get_license_info()
    mac_address = get_mac_address()

    payload = {
        "license": license,
        "mac": mac_address
    }
    response = requests.post(setting.Config["LICENSE_CHK_URL"], json=payload)
    data = response.json()
    value = data.get('result')
    return value