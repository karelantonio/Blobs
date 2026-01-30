from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.recycleview import MDRecycleView
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty

from .common import *
from .state import *
from .resources import RESOURCES
from .events import EVENTS


class NewEventScreen(MDScreen):
    event_tpl = ObjectProperty(EVENTS[0])


class RootWidget(MDScreenManager):
    state = ObjectProperty(State())


class MainApp(MDApp):
    rootw = None

    def build(self):
        self.rootw = RootWidget()
        return self.rootw

    def switch_theme(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
