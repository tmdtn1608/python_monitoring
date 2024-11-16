import os
from dotenv import dotenv_values,load_dotenv
load_dotenv()

class settingService ():
    Config = {}
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if(self.Config == {}) :
            current_dir = os.getcwd()
            default_path = os.path.join(current_dir,".env")
            # .env 파일이 현재 위치에 있는지 확인
            if os.path.exists(default_path):
                # .env 파일 로드
                self.Config = dotenv_values(dotenv_path=current_dir)
            else:
                env_file_path = os.path.join(current_dir,"monitoring-client",".env")
                self.Config = dotenv_values(env_file_path)