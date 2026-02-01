from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDListItem, MDListItemLeadingAvatar
from kivymd.uix.pickers import MDModalDatePicker, MDTimePickerDialVertical
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout

from .state import *
from .resources import RESOURCES, RESOURCES_AS_DICT
from .events import EVENTS


class EventResQuantityPicker(MDDialog):
    name = StringProperty("")
    qty = NumericProperty(0)
    evt_selected = ObjectProperty(lambda x: None)

    def get_total(self):
        return RESOURCES_AS_DICT[self.name].total

    def on_ok(self):
        self.dismiss()
        self.evt_selected(int(self.ids.slider.value))

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
    qty_text = StringProperty("0 x")
    evt_qty_update = ObjectProperty(lambda x, y: None)

    def show_qnt_picker(self):
        def on_selected(new_qty):
            self.evt_qty_update(self.name, new_qty)
        EventResQuantityPicker(name=self.name, qty=self.qty, evt_selected=on_selected).open()

class NewEventScreen(MDScreen):
    resources = ListProperty()
    event_tpl = None
    event_tpl_name = StringProperty("Pick an event")
    event_tpl_description = StringProperty("")
    event_tpl_icon = StringProperty("")

    def __init__(self, *args, **kwa):
        super().__init__(*args, **kwa)
        self.resources = [{
            "name": res.name,
            "icon": RESOURCES_AS_DICT[res.name].icon,
            "evt_qty_update": self.evt_qty_update,
            "qty": 0,
            "qty_text": "0 x",
        } for res in RESOURCES]

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

    def show_date_picker(self, wid, focus):
        if not focus:
            return

        def on_ok(datp):
            datp.dismiss()
            self.ids.date.text = f"{datp.day}/{datp.month}/{datp.year}"

        def on_cancel(datp):
            datp.dismiss()

        datp = MDModalDatePicker(on_ok=on_ok, on_cancel=on_cancel)
        datp.open()

    def show_time_picker(self, wid, focus):
        if not focus:
            return
        
        def on_ok(timp):
            timp.dismiss()
            self.ids.time.text = f"{timp.hour}:{timp.minute}"

        def on_cancel(timp):
            timp.dismiss()

        timp = MDTimePickerDialVertical(on_ok=on_ok, on_cancel=on_cancel)
        timp.open()

    def evt_qty_update(self, name, new_qty):
        copy = self.resources.copy()
        for i, e in enumerate(self.resources):
            if e["name"] == name:
                copy[i]["qty"] = new_qty
                copy[i]["qty_text"] = f"{new_qty} x"
                break
        self.resources = copy
        self.ids.resources_rv.data = copy
        self.ids.resources_rv.refresh_from_data()

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
