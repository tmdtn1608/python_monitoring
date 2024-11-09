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

    def getProcess(self) -> dict[str, str] | None : 
        if self.os_name == 'Windows': # Windows에 대한 함수 호출
            print("Running Windows specific function.")
            return self.getWindowsProcess()
        elif self.os_name == 'Linux': # Linux에 대한 함수 호출
            print("Running Linux specific function.")
            return self.getLinuxProcess()
        elif self.os_name == 'Darwin':  # macOS의 경우
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
        # return json_output
        return process_list

    def getWindowsProcess(self) -> json :
        process_list = []
        # pid가 windows에서 지원하는지 확인해볼 것.
        # mac status -> windows name, mac memory_percent -> windows memory_info
        for proc in psutil.process_iter(['pid','name', 'cpu_percent','memory_info']):
            process_info = proc.info
            process_list.append(process_info)

        json_output = json.dumps(process_list, indent=4)
        return json_output
    
    def getLinuxProcess(self) -> json :
        process_list = []
        # pid가 linux에서 지원하는지 확인해볼 것.
        # mac status -> windows name, mac memory_percent -> windows memory_info
        for proc in psutil.process_iter(['pid','gids', 'cpu_num','create_time']):
            process_info = proc.info
            process_list.append(process_info)

        json_output = json.dumps(process_list, indent=4)
        return json_output