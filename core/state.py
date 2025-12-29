from dataclasses import dataclass
from kivy.app import App

@dataclass
class State:
    pass

def state()->State:
    return App.get_running_app().state

def set_state(st: State):
    App.get_running_app().state = st

