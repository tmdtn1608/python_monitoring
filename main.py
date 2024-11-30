# basic
import os
import sys
# kivy ui
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.button import Button
# module
import asyncio
import websockets
import json
import threading
from getmac import get_mac_address
from dotenv import load_dotenv
# service & component
from Services.monitoringService import monitoringService
from Services.licenseService import cancel_license, get_license_info, check_license, set_license_info
from Services.historyService import send_history
from Services.logService import send_process_log
from Services.systemService import create_tray_icon
from component import get_license_input, get_license_validation
from Const import CLIENT_LOGIN, CLIENT_LOGOUT, WS_URL
# Kivy 로깅 비활성화 환경변수
# os.environ['KIVY_NO_CONSOLELOG'] = '1'


class ProcessMonitor(App):
    '''
    Initialize
    '''
    def build(self):
        Window.bind(on_minimize=self.on_minimize)
        self.title = "monitor"
        Window.size = (380, 150)
        Window.left = 400
        Window.top = 100
        Window.resizable = False

        # mac 주소
        self.mac = get_mac_address()

        LabelBase.register(
            name='MyFont', 
            fn_regular="/System/Library/Fonts/AppleSDGothicNeo.ttc")

        grid = GridLayout(cols=2, rows=3, padding=15, spacing=15, row_force_default=True, row_default_height=70)
    
        grid.add_widget(Label(text='서버상태', font_name="MyFont", size_hint_x=None, width=150))
        grid.add_widget(Label(text='정상', font_name="MyFont", size_hint_x=None, width=100))
        
        grid.add_widget(Label(text='라이센스', font_name="MyFont", size_hint_x=None, width=150))
        
        self.license_info = get_license_info()
        if self.license_info is None :
            print("No license. Set license info")
            box, self.license_input = get_license_input(self)
            grid.add_widget(box)
        else :
            valid_check = check_license()
            grid.add_widget(get_license_validation(valid_check))
            if(valid_check == True) :
                # Start the WebSocket thread
                threading.Thread(target=self.start_websocket_thread, daemon=True).start()
            else :
                print("Invalid license or device")

        # 시연배포용
        reset_btn = Button(text='라이센스 초기화', font_name="MyFont", size_hint_x=None, width=250)
        reset_btn.bind(on_press=self.reset_license) 
        grid.add_widget(reset_btn)

        # Initialize monitoring service
        self.monitoring_service = monitoringService()

        return grid
    '''
    Window 최소화 이벤트 리스너 -> 아이콘트레이
    '''
    def on_minimize(self, window, *args):
        Window.hide()
        threading.Thread(target=create_tray_icon, daemon=True).start()
    '''
    라이센스 등록 API
    '''
    def regist_request(self,instance) :
        license_text = self.license_input.text
        set_license_info(license_text)
        os.execl(sys.executable, sys.executable, *sys.argv)
    '''
    라이센스 초기화
    '''
    def reset_license(self, instance) :
        cancel_license(self.mac)
        os.execl(sys.executable, sys.executable, *sys.argv)
    '''
    웹소켓 쓰레드
    '''
    def start_websocket_thread(self):
        # Run the asyncio event loop in this thread
        asyncio.run(self.connect())

    '''
    웹소켓 송수신 및 접속관리
    '''
    async def connect(self):
        uri = WS_URL
        while True : 
            try:
                async with websockets.connect(uri) as websocket:
                    print("Connected to WebSocket!")
                    login_res : bool = send_history(CLIENT_LOGIN)
                    self.websocket = websocket
                    
                    while login_res:
                        await asyncio.gather(
                            self.send_process_info(websocket),
                            self.receive_terminate()
                        ) 
            except websockets.ConnectionClosed:
                send_history(CLIENT_LOGOUT)
                print("Connection closed")

    '''
    웹소켓 Heartbeat & 프로세스 목록 전송
    '''
    async def send_process_info(self, websocket):
        while True :
            process_info = self.monitoring_service.get_process()
            process_json = {"device": self.mac, "process": process_info}
            send_process_log(process_json)
            websocket_ping = {"from" : self.mac}
            print("SEND WEBSOCKET")
            await websocket.send(json.dumps(websocket_ping))
            await asyncio.sleep(5)

    '''
    프로세스 종료메세지 수신 리스너
    '''
    async def receive_terminate(self):
        while True:
            message = await self.websocket.recv()
            print(f"SUCCESS TERMINATE RECEIVE: {message}")
            self.monitoring_service.kill_process(message)

    '''
    Destroy
    '''
    def on_stop(self):
        print("Stopping the app...")
        if self.license_info is not None :
            send_history(CLIENT_LOGOUT)

if __name__ == '__main__':
    ProcessMonitor().run()
