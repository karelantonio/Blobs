from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDListItem, MDListItemLeadingAvatar
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout

from .state import *
from .resources import RESOURCES, RESOURCES_AS_DICT
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

class NewEventReq(MDBoxLayout):
    name = StringProperty("")
    icon = StringProperty("")
    qty  = StringProperty("")

class NewEventRes(RectangularRippleBehavior, ButtonBehavior, MDBoxLayout):
    name = StringProperty("")
    icon = StringProperty("")
    qty  = NumericProperty(0)

class NewEventScreen(MDScreen):
    resources = ListProperty([{
        "name": res.name,
        "icon": RESOURCES_AS_DICT[res.name].icon,
        "qty": 0,
    } for res in RESOURCES])
    event_tpl = None
    event_tpl_name = StringProperty("Pick an event")
    event_tpl_description = StringProperty("")
    event_tpl_icon = StringProperty("")

    def set_event_tpl(self, ev):
        self.event_tpl = ev
        self.event_tpl_name = ev.name
        self.event_tpl_description = ev.description
        self.event_tpl_icon = ev.icon
        self.update_reqs()
    
    def update_reqs(self):
        items = [
            {
                "name": req.name,
                "icon": RESOURCES_AS_DICT[req.name].icon,
                "qty": f"{req.qty} x"
            }
            for req in self.event_tpl.requires
        ]
        self.ids.requirements.data = items

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
