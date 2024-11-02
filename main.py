import os
# Kivy 로깅을 완전히 비활성화하기 위한 환경 변수 설정
os.environ['KIVY_NO_CONSOLELOG'] = '1'
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
# service & component
from Services.monitoringService import monitoringService
from Services.licenseService import get_license_info, check_license
from component import get_license_input, get_license_validation
from Const import BASE_URL

class MyApp(App):
    
    def build(self):
        self.title = "monitor"
        Window.size = (380, 150)
        Window.left = 400
        Window.top = 100
        Window.resizable = False

        LabelBase.register(name='MyFont', fn_regular='./Resources/D2Coding-Ver1.3.2-20180524.ttf')

        grid = GridLayout(cols=2, rows=3, padding=15, spacing=15, row_force_default=True, row_default_height=70)
    
        grid.add_widget(Label(text='서버상태', font_name="MyFont", size_hint_x=None, width=150))
        grid.add_widget(Label(text='정상', font_name="MyFont", size_hint_x=None, width=100))
        
        grid.add_widget(Label(text='라이센스', font_name="MyFont", size_hint_x=None, width=150))
        
        license_info = get_license_info()
        if license_info is None :
            print("No license. Set license info")
            grid.add_widget(get_license_input(self))
        else :
            print("license : ", license_info)
            valid_check = check_license()
            grid.add_widget(get_license_validation(valid_check))
            # Start the WebSocket thread
            threading.Thread(target=self.start_websocket_thread, daemon=True).start()

        grid.add_widget(Label(text='서버전송', font_name="MyFont", size_hint_x=None, width=150))
        send_btn = Button(text='Button 2', font_name="MyFont", size_hint_x=None, width=210)
        send_btn.bind(on_press=self.send_request)
        grid.add_widget(send_btn)

        # Initialize the monitoring service
        self.monitoring_service = monitoringService()

        return grid
    
    def regist_request(self,instance) :
        print('press resgist')

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
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket!")
                self.websocket = websocket
                while True:
                    await self.send_process_info(websocket)
                    await asyncio.sleep(5) 
        except websockets.ConnectionClosed:
            print("Connection closed")

    async def send_process_info(self, websocket):
        process_info = self.monitoring_service.getProcess()
        json_data = json.dumps(process_info)
        # await websocket.send(json_data)
        await websocket.send("Send test")

    def on_stop(self):
        print("Stopping the app...")
        if(self.websocket is not None):
            print('check ')
            asyncio.get_event_loop().create_task(self.websocket.close())

if __name__ == '__main__':
    MyApp().run()
