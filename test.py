import PySimpleGUI as sg
from enum import Enum, auto

class Const(Enum):
    enum_key = auto()
    str_key = "str_key"

test_layout = [
    [sg.Text("Using enum as the key"), sg.InputText(key=Const.enum_key)],
    [sg.Text("Using a string as the key"), sg.InputText(key=Const.str_key.value)],
    [sg.OK()]
]

window = sg.Window("test Window", layout=test_layout)

event, values = window.read()
print(f"event: {event}, values: {values}")
print(f"Enum key: {values[Const.enum_key]}")

window.close()

