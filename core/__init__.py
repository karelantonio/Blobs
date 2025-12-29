from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout

from .common import *


class StartScreen(AnchorLayout):
    pass


class MainApp(App):
    def build(self):
        return StartScreen()
