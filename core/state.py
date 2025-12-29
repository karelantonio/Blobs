from dataclasses import dataclass
from kivy.app import App
from kivy.event import EventDispatcher

class State(EventDispatcher):
    def __init__(self, *args, **kwa):
        super().__init__(*args, *kwa)
        # Initialize here


def state()->State:
    return App.get_running_app().rootw.state


def set_state(st: State):
    App.get_running_app().rootw.state = st

