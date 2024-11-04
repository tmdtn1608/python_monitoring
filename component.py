from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from Services.licenseService import check_license

def get_license_input(instance) -> tuple[BoxLayout, TextInput]:
    box = BoxLayout(orientation='horizontal')
    # TextInput 추가
    text_input = TextInput(hint_text='라이센스 입력', font_name="MyFont")
    box.add_widget(text_input)

    # Button 추가
    send_btn = Button(text='확인', font_name="MyFont", size_hint_x=None, width=100)
    # TODO : 이벤트 바인딩
    send_btn.bind(on_press=instance.regist_request) 
    box.add_widget(send_btn)
    return box, text_input

def get_license_validation(param : bool) -> Label: 
    value = '유효' if param == True else '무효'
    return Label(text=f"라이센스 {value}", font_name="MyFont")

