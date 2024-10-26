from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock
import asyncio
import websockets
import requests
import threading

class MyApp(App):
    def build(self):
        self.title = "monitor"
        Window.size = (300, 120)  # 윈도우 크기
        Window.left = 400 # 오픈되는 윈도우 위치, left
        Window.top = 100 # 오픈되는 윈도우 위치, top
        Window.resizable = False # 크기조정
        Window.borderless = False # borderless

        # 사용할 폰트 설정 (TTF 파일 경로)
        #/Users/seungsubaek/Downloads/D2Coding-Ver1.3.2-20180524/D2Coding
        LabelBase.register(name='MyFont', fn_regular='./Resources/D2Coding-Ver1.3.2-20180524.ttf')
        
        # 종료 플래그 설정
        self.stop_event = threading.Event()

        # GridLayout 설정
        grid = GridLayout(
            cols=2, # 열 수
            rows=3, # 행 수
            padding=15, # 여백
            spacing=15, # 위젯 간 간격
            # size_hint=(0.5, 0.5), # 크기 비율, 확인 필요.....
            # pos_hint={'center_x': 0.4, 'center_y': 0.75}, # 위치 비율
            row_force_default=True, # 열 크기 강제
            row_default_height=60, # 열 크기 강제시 강제할 정도
            col_force_default = True, # 기본 너비 강제 적용
            col_default_width = 150 # 기본 열 너비 설정
        )

        # 라벨 및 버튼 추가
        grid.add_widget(
            Label(text='서버상태',font_name="MyFont", size_hint_x=None,width=150)
        )
        grid.add_widget(
            Label(text='정상', font_name="MyFont", size_hint_x=None,width=150)
        )
        grid.add_widget(
            Label(text='라이센스',font_name="MyFont", size_hint_x=None,width=150)
        )
        grid.add_widget(
            Label(text='라이센스 유효', font_name="MyFont", size_hint_x=None,width=200)
        )
        grid.add_widget(
            Label(text='서버전송',font_name="MyFont", size_hint_x=None,width=150)
        )
        send_btn = Button(text='Button 2',
                          font_name="MyFont", 
                          size_hint_x=None, 
                          width=150)
        send_btn.bind(on_press=self.send_request)
        grid.add_widget(send_btn)
        # Clock.schedule_once(lambda dt: asyncio.run(self.connect()), 0)
        Clock.schedule_once(lambda dt: self.start_websocket_thread(), 0)

        return grid
    
    def send_request(self, instance) :
        print("send request")
        # TODO : http request로 전송.
        response = requests.get("http://localhost:3000/")
        if response.status_code == 200:
            print(response.text)  # JSON 데이터를 출력
        else:
            print(f"Request failed with status code {response.status_code}")

    def start_websocket_thread(self):
        # WebSocket 연결을 스레드에서 실행
        thread = threading.Thread(target=asyncio.run, args=(self.connect(),))
        thread.start()

    async def connect(self):
        uri = "ws://localhost:3000/ws" 
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket!")
                
                # 연결 유지 및 메시지 수신
                while not self.stop_event.is_set():
                    await websocket.send("Ping")
                    response = await websocket.recv()
                    print("Server response:", response)
                    await asyncio.sleep(5)
        except websockets.ConnectionClosed:
            print("Connection closed")

    def on_stop(self):
        # 앱이 종료될 때 종료 플래그 설정
        print("Stopping the app and WebSocket connection...")
        self.stop_event.set()


'''
라이센스 정보 획득
'''
def get_license_info() -> bool :
    return True

if __name__ == '__main__':
    MyApp().run()
