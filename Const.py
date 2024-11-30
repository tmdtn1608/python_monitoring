import os
import sys
from dotenv import load_dotenv

# .env에서 환경변수 받아오기
if hasattr(sys, '_MEIPASS'):
    # 배포시
    dotenv_path = os.path.join(sys._MEIPASS, '.env')
else:
    # 개발버전시
    dotenv_path = '.env'

# API URL
BASE_URL=os.getenv('BASE_URL')
WS_URL=os.getenv('WS_URL')
LICENSE_URL=os.getenv('LICENSE_URL')
LICENSE_REGIST_URL=os.getenv('LICENSE_REGIST_URL')
LICENSE_CHK_URL=os.getenv('LICENSE_CHK_URL')
HISTORY_URL=os.getenv('HISTORY_URL')
LOG_URL=os.getenv('LOG_URL')
DEVICE_URL=os.getenv('DEVICE_URL')

# Font path
FONT_PATH=os.getenv('FONT_PATH')

# HISTORY ACT TYPE
CLIENT_LOGIN = os.getenv('CLIENT_LOGIN')
CLIENT_LOGOUT = os.getenv('CLIENT_LOGOUT')
USER_LOGIN = os.getenv('USER_LOGIN')
USER_LOGOUT = os.getenv('USER_LOGOUT')
BLACK_ADDED = os.getenv('BLACK_ADDED')
BLACK_REMOVED = os.getenv('BLACK_REMOVED')
WHITE_ADDED = os.getenv('WHITE_ADDED')
WHITE_REMOVED = os.getenv('WHITE_REMOVED')
CMD_KILL_BLACK = os.getenv('CMD_KILL_BLACK')
AUTO_KILL_BLACK = os.getenv('AUTO_KILL_BLACK')