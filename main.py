from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
import asyncio
import websockets
import requests
import json
import threading

from Services.monitoringService import monitoringService

class MyApp(App):
    
    def build(self):
        self.title = "monitor"
        Window.size = (300, 120)
        Window.left = 400
        Window.top = 100
        Window.resizable = False

        LabelBase.register(name='MyFont', fn_regular='./Resources/D2Coding-Ver1.3.2-20180524.ttf')

        grid = GridLayout(cols=2, rows=3, padding=15, spacing=15)

        grid.add_widget(Label(text='서버상태', font_name="MyFont"))
        grid.add_widget(Label(text='정상', font_name="MyFont"))
        grid.add_widget(Label(text='라이센스', font_name="MyFont"))
        grid.add_widget(Label(text='라이센스 유효', font_name="MyFont"))
        grid.add_widget(Label(text='서버전송', font_name="MyFont"))

        send_btn = Button(text='Button 2', font_name="MyFont")
        send_btn.bind(on_press=self.send_request)
        grid.add_widget(send_btn)

        # Initialize the monitoring service
        self.monitoring_service = monitoringService()

        # Start the WebSocket thread
        threading.Thread(target=self.start_websocket_thread, daemon=True).start()

        return grid

    def send_request(self, instance):
        response = requests.get("http://localhost:3000/")
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Request failed with status code {response.status_code}")

    def start_websocket_thread(self):
        # Run the asyncio event loop in this thread
        asyncio.run(self.connect())

    async def connect(self):
        uri = "ws://localhost:3000/ws"
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket!")
                while True:
                    await self.send_process_info(websocket)
                    await asyncio.sleep(5)  # Wait before sending the next message
        except websockets.ConnectionClosed:
            print("Connection closed")

    async def send_process_info(self, websocket):
        process_info = self.monitoring_service.getProcess()
        print("============================\n",process_info) # why return None?
        json_data = json.dumps(process_info)
        await websocket.send(json_data)  # Send the JSON data
        print("Sent process info:", json_data)

    def on_stop(self):
        print("Stopping the app...")

if __name__ == '__main__':
    MyApp().run()
