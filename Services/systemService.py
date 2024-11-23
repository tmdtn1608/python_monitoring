import platform
import sys
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from kivy.core.window import Window
# macOS에서만 필요한 라이브러리 임포트
# if platform.system() == 'Darwin':
#     import objc
#     from Cocoa import NSApp, NSApplication, NSStatusBar, NSVariableStatusItemLength, NSMenu, NSMenuItem
#     NSApplicationActivationPolicyProhibited = 0
#     NSApplicationActivationPolicyRegular = 1
#     NSApplicationActivationPolicyAccessory = 2

# elif platform.system() == 'Windows': 
#     import win32gui
#     import win32con
'''
시스템 트레이 아이콘 생성 함수. 동작안함?
'''
def create_tray_icon(icon):
    # 트레이 아이콘 클릭 시 실행할 함수
    def on_clicked(icon, item):
        icon.stop()
        Window.show()  

    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill="blue")

    icon = Icon("test", image, menu=Menu(MenuItem("Restore", on_clicked)))
    icon.run()

