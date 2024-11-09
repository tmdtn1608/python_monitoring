import os
# Kivy 로깅 비활성화 환경변수
# os.environ['KIVY_NO_CONSOLELOG'] = '1'
#kivy ui
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
# module
import asyncio
import websockets
import requests
import json
import threading
from getmac import get_mac_address
# service & component
from Services.monitoringService import monitoringService
from Services.licenseService import get_license_info, check_license, reset_license, set_license_info
from Services.historyService import send_history
from component import get_license_input, get_license_validation
from Const import BASE_URL, CLIENT_LOGIN, CLIENT_LOGOUT, HISTORY_URL

class MyApp(App):
    
    def build(self):
        self.title = "monitor"
        Window.size = (380, 150)
        Window.left = 400
        Window.top = 100
        Window.resizable = False

        # FOR DEBUGGING
        # reset_license()

        LabelBase.register(name='MyFont', fn_regular='./Resources/D2Coding-Ver1.3.2-20180524.ttf')

        grid = GridLayout(cols=2, rows=3, padding=15, spacing=15, row_force_default=True, row_default_height=70)
    
        grid.add_widget(Label(text='서버상태', font_name="MyFont", size_hint_x=None, width=150))
        grid.add_widget(Label(text='정상', font_name="MyFont", size_hint_x=None, width=100))
        
        grid.add_widget(Label(text='라이센스', font_name="MyFont", size_hint_x=None, width=150))
        
        license_info = get_license_info()
        if license_info is None :
            print("No license. Set license info")
            box, self.license_input = get_license_input(self)
            grid.add_widget(box)
        else :
            print("license : ", license_info)
            valid_check = check_license()
            grid.add_widget(get_license_validation(valid_check))
            if(valid_check == True) :
                # Start the WebSocket thread
                threading.Thread(target=self.start_websocket_thread, daemon=True).start()
            else :
                print("Invalid license or device")

        grid.add_widget(Label(text='서버전송', font_name="MyFont", size_hint_x=None, width=150))
        send_btn = Button(text='Button 2', font_name="MyFont", size_hint_x=None, width=210)
        send_btn.bind(on_press=self.send_request)
        grid.add_widget(send_btn)

        # Initialize the monitoring service
        self.monitoring_service = monitoringService()

        return grid
    
    def regist_request(self,instance) :
        license_text = self.license_input.text
        set_license_info(license_text)


    def send_request(self, instance):
        response = requests.get(BASE_URL + "/")
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Request failed with status code {response.status_code}")

    def start_websocket_thread(self):
        # Run the asyncio event loop in this thread
        asyncio.run(self.connect())


    async def connect(self):

        uri = "ws://localhost:5000/ws"
        while True : 
            try:
                async with websockets.connect(uri) as websocket:
                    print("Connected to WebSocket!")
                    login_res : bool = send_history(CLIENT_LOGIN)
                    self.websocket = websocket
                    while login_res:
                        await self.send_process_info(websocket)
                        await asyncio.sleep(5) 
            except websockets.ConnectionClosed:
                send_history(CLIENT_LOGOUT)
                print("Connection closed")

    async def send_process_info(self, websocket):
        # json dict[str,str]
        process_info = self.monitoring_service.getProcess()
        device = get_mac_address()
        process_json = {"device": device, "process": process_info}
        json_txt = json.dumps(process_json)
        # FIXME : websocket 전송이 아닌 http로 전송
        await websocket.send(json_txt)

    def on_stop(self):
        print("Stopping the app...")
        send_history(CLIENT_LOGOUT)
        print('check ')

if __name__ == '__main__':
    MyApp().run()
