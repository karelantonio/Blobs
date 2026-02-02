from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDListItem, MDListItemLeadingAvatar
from kivymd.uix.pickers import MDModalDatePicker, MDTimePickerDialVertical
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ListProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from datetime import datetime
from re import match

from .coldetect import check_exclusions, check_inclusions, check_collisions
from .events import load_events_from_disk, save_events_to_disk, Resource, Event
from .resources import RESOURCES, RESOURCES_AS_DICT
from .event_templates import EVENTS, EVENTS_AS_DICT


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

    def check_and_create_event_dammit(self):
        def err_snack(msg):
            MDSnackbar(
                MDSnackbarText(
                    text=msg,
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
            ).open()

        # Check a event template has been selected
        if self.event_tpl is None:
            err_snack("Error: Pick an event template first")
            return
        
        # Check if the date is set
        date: str = self.ids.date.text.strip()
        if len(date)==0:
            err_snack("Error: Pick a start date")
            return
        if match("\\d+/\\d+/\\d+", date) is None:
            err_snack("Error: Date does not look valid (must be DD/MM/YY)")
            return
        
        # The time
        time: str = self.ids.time.text.strip()
        if len(time)==0:
            err_snack("Error: Pick a time of the day")
            return
        if match("\\d+:\\d+", time) is None:
            err_snack("Error: Time does not look valid (must be DD/MM/YY)")
            return
        dt = datetime.strptime(f"{date} {time}:00", "%d/%m/%Y %H:%M:%S")

        # Now, the duration
        duration = self.ids.duration.text.strip()
        if len(duration)==0:
            err_snack("Error: Specify a duration")
            return
        try:
            duration = int(duration)
        except:
            err_snack("Error: Duration does not look like a valid integer")
            return

        if duration<0:
            err_snack("Error: Duration must be positive")
            return
        if duration==0:
            err_snack("Error: Duration cannot be zero nor negative, must be positive")
            return

        # Now, must satisfy all requirements
        for req in self.event_tpl.requires:
            name, qty = req.name, req.qty

            for res in self.resources:
                if res["name"] != name:
                    continue
                if res["qty"] < qty:
                    err_snack(f"Error: Requirement '{name}' is not satisfied (need to add {qty - res['qty']} more)")
                    return
                break

        # Check for exclusion, inclusion and collision errors
        inclerr = check_inclusions(self.resources)
        if inclerr is not None:
            err_snack("Error: " + inclerr)
            return
        
        exclerr = check_exclusions(self.resources)
        if exclerr is not None:
            err_snack("Error: " + exclerr)
            return

        colerr = check_collisions(dt, duration, self.resources)
        if colerr is not None:
            err_snack("Error: " + colerr)
            return

        # Everything OK, add and pop (and reset) this screen
        pass


class EventItem(RectangularRippleBehavior, ButtonBehavior, MDBoxLayout):
    name = StringProperty("")
    start = StringProperty("")
    end = StringProperty("")
    duration = StringProperty("")
    icon = StringProperty("")
    idx = NumericProperty(0)


class RootWidget(MDScreenManager):
    pass


class MainApp(MDApp):
    rootw = None
    events = ObjectProperty(load_events_from_disk())

    def build(self):
        self.bind(events=self.events_changed)
        self.rootw = RootWidget()
        print(self.events)
        events_data = [
            {
                "name": evt.name,
                "start": evt.date.strftime("%d/%m/%Y %H:%M"),
                "end": evt.end_date().strftime("%d/%m/%Y %H:%M"),
                "duration": f"{evt.hours} hrs",
                "icon": EVENTS_AS_DICT[evt.name].icon,
                "idx": i
            }
            for i, evt in enumerate(self.events)
        ]
        self.rootw.ids.overview.ids.events_rv.data = events_data
        return self.rootw
    
    def events_changed(self):
        # Save and update the recyclerview
        print("Events changed")

    def switch_theme(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
