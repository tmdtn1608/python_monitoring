import json
from typing import List
import psutil
import platform

class monitoringService():
    os_name = ''
    os_info = ''
    processArr = []

    def __init__(self):
        self.os_name = platform.system()
        self.os_info = platform.uname()
        print(f"{self.os_name}\n{self.os_info}")

    def getProcess(self): 
        if self.os_name == 'Windows': # Windows에 대한 함수 호출
            print("Running Windows specific function.")
            return self.getWindowsProcess()
        elif self.os_name == 'Linux': # Linux에 대한 함수 호출
            print("Running Linux specific function.")
        elif self.os_name == 'Darwin':  # macOS의 경우
            print("Running macOS specific function.")
            return self.getMacProcess()
        else:
            print("Unknown Operating System.")
            return
        
    def getMacProcess(self) -> json:
        process_list = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
            process_info = proc.info
            process_list.append(process_info)

        json_output = json.dumps(process_list, indent=4)
        return json_output

    def getWindowsProcess(self) :
        # pid가 windows에서 지원하는지 확인해볼 것.
        # mac status -> windows name, mac memory_percent -> windows memory_info
        for proc in psutil.process_iter(['pid','name', 'cpu_percent','memory_info']):
            print(proc)