import keyring
from getmac import get_mac_address
import requests
from Const import DEVICE_URL, LICENSE_REGIST_URL, LICENSE_CHK_URL 

'''
로컬 라이센스값 가져오기(키체인)
'''
def get_license_info() -> str | None :
    license_info = keyring.get_password("system", "username")
    return license_info

'''
라이센스 등록.
'''
def set_license_info(license : str) :
    
    # license, mac_address 전송
    mac_address = get_mac_address()
    payload = {
        "license": license,
        "mac": mac_address
    }
    response = requests.post(LICENSE_REGIST_URL, json=payload)
    data = response.json()
    value = data.get('result')
    if (value == True) :
        keyring.set_password("system","username",license)
    else : 
        return

'''
라이센스 초기화
'''
def reset_license(device) :
    # 로컬에서 삭제
    keyring.delete_password("system","username")
    # db에서 삭제
    payload = {
        "mac" : device
    }

    response = requests.delete(DEVICE_URL, json=payload)
    if(response.status_code == 200) :
        return True
    else : return False

'''
라이센스 유효성 체크
'''
def check_license() :
    
    license = get_license_info()
    mac_address = get_mac_address()

    payload = {
        "license": license,
        "mac": mac_address
    }
    response = requests.post(LICENSE_CHK_URL, json=payload)
    data = response.json()
    value = data.get('result')
    return value
