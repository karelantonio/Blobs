from kivy.app import App
from datetime import datetime, timedelta

from .coldetect import check_collisions

def find_hole(hours, resources)->datetime:
    nw = datetime.now()
    ends = set([e.end_date() for e in App.get_running_app().events if e.end_date()>nw]
               + [datetime(year=nw.year, month=nw.month, day=nw.day, hour=nw.hour, minute=nw.minute)])
    for dt in sorted(ends):
        if check_collisions(dt, hours, resources) is None:
            return dt

    return nw # TODO: This is a workaround, but there should be at least one date (the last at least)
