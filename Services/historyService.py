from getmac import get_mac_address
import requests
from Const import CLIENT_LOGIN, HISTORY_URL


def send_history(param) -> bool:
    mac_address = get_mac_address()
    payload = {
        "mac": mac_address,
        "actType" : param
    }
    response = requests.post(HISTORY_URL, json=payload)
    if response.status_code == 200 :
        return True
    else : return False
