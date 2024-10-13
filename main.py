import psutil
import platform

class main():
    name = ''
    os_name = ''
    os_info = ''
    processArr = []

    def __init__(self, name):
        self.name = name
        self.os_name = platform.system()
        self.os_info = platform.uname()

    def call(self): # 클래스의 메서드/함수는 다음과 같이 자기자신을 인자로 넘겨줘야한다.
        print(self.name)
        # print(f"{self.os_name}\n{self.os_info}")

    def getProcess(self): 
        if self.os_name == 'Windows':
            # Windows에 대한 함수 호출
            print("Running Windows specific function.")
        elif self.os_name == 'Linux':
            # Linux에 대한 함수 호출
            print("Running Linux specific function.")
        elif self.os_name == 'Darwin':  # macOS의 경우
            print("Running macOS specific function.")
            self.getMacProcess()
        else:
            print("Unknown Operating System.")
            return
        
    def getMacProcess(self) :
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
            print(proc.info)


testObj = main("TEST")

# testObj.call()
testObj.getProcess()
