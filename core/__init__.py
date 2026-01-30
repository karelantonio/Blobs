from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDListItem, MDListItemLeadingAvatar
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout

from .common import *
from .state import *
from .resources import RESOURCES
from .events import EVENTS


class EventChooserDialogItem(MDListItem):
    image = StringProperty("")
    title = StringProperty("")
    value = ObjectProperty(None)
    selected_evt = ObjectProperty(None)

    def selected(self):
        self.selected_evt(self.value)

class EventChooserDialog(MDDialog):
    selected_evt = ObjectProperty(lambda x: None)

    def open(self, *args, **kwa):
        def dismiss_and_select(x):
            self.dismiss()
            self.selected_evt(x)

        cnt = self.ids.container
        for evt in EVENTS:
            cnt.add_widget(EventChooserDialogItem(
                image=evt.icon,
                title=evt.name,
                value=evt,
                selected_evt=dismiss_and_select
            ))
        super().open(*args, **kwa)

class NewEventScreen(MDScreen):
    event_tpl = EVENTS[0]
    event_tpl_name = StringProperty(event_tpl.name)
    event_tpl_description = StringProperty(event_tpl.description)
    event_tpl_icon = StringProperty(event_tpl.icon)

    def set_event_tpl(self, ev):
        self.event_tpl = ev
        self.event_tpl_name = ev.name
        self.event_tpl_description = ev.description
        self.event_tpl_icon = ev.icon

    def show_event_chooser_dialog(self):
        EventChooserDialog(selected_evt=self.set_event_tpl).open()


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
