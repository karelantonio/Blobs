from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty

from .common import *
from .state import *


class MaterialButton(Button):
    pass


class StartScreen(Screen):
    pass


class RootWidget(ScreenManager):
    state = ObjectProperty(State())


class MainApp(App):
    rootw = None

    def build(self):
        self.rootw = RootWidget()
        return self.rootw
