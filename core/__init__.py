from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen

from .common import *


class MaterialButton(Button):
    pass


class StartScreen(Screen):
    pass


class MainApp(App):
    def build(self):
        return self.root
