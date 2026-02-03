from kivy.app import App
from datetime import datetime, timedelta
from .events import Event, Resource
from .resources import RESOURCES_AS_DICT, RESOURCES

def check_exclusions(rrss: list)->str|None:
    for resd1 in rrss:
        res1 = RESOURCES_AS_DICT[resd1["name"]]

        for resd2 in rrss:
            if resd2["qty"]==0:
                continue
            if resd2['name'] in res1.excludes:
                return f"{res1.name} must not be used at the same time as: {resd2['name']}"

def check_inclusions(rrss: list)->str|None:
    names = set([r["name"] for r in rrss if r["qty"]>0])
    for r in rrss:
        incl = RESOURCES_AS_DICT[r["name"]].includes
        for req in incl:
            if req not in names:
                return f"Resource {r['name']} requires: {req}"

def check_collisions(start: datetime, hours: int, rrss: list)->str|None:
    # Assume we've added this event, then there should be no conflicts
    evts: list[Event] = App.get_running_app().events.copy()
    evts.append(Event(
        name="ASD",
        date=start,
        hours=hours,
        resources=[Resource.from_dict(d) for d in rrss]
    ))

    starts = [evt.date for evt in evts]

    for start in sorted(starts):
        # This is to accumulate how much resources are being used
        allres = {res.name: 0 for res in RESOURCES}

        # Find all the events that contain this instant
        for evt in evts:
            if not (evt.date <= start < evt.end_date()):
                continue
            for res in evt.resources:
                allres[res.name] += res.qty
        for name, qty in allres.items():
            if qty>RESOURCES_AS_DICT[name].total:
                return f"If added, creates a collision (using more resources than the available)"
