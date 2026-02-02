from datetime import datetime, timedelta
from dataclasses import dataclass
from json import loads, dumps

@dataclass
class Resource:
    name: str
    qty: int

    def to_dict(self):
        return {
            "name": self.name,
            "qty": self.qty
        }

    def from_dict(dct)->"Resource":
        return Resource(
            name=dct["name"],
            qty=dct["qty"]
        )

@dataclass
class Event:
    name: str
    date: datetime
    hours: int
    resources: list[Resource]

    def end_date(self)->datetime:
        return self.date + timedelta(hours=self.hours)

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date.strftime("%m/%d/%Y %H:%M:%S"),
            "hours": self.hours,
            "resources": [
                res.to_dict() for res in self.resources
            ]
        }

    def from_dict(dct)->"Event":
        return Event(
            name=dct["name"],
            date=datetime.strptime(dct["date"], "%m/%d/%Y %H:%M:%S"),
            hours=dct["hours"],
            resources=[Resource.from_dict(x) for x in dct["resources"]]
        )


def load_events_from_disk()->list[Event]:
    try:
        with open("save.json", "r", encoding="utf-8") as file:
            dct = loads(file.read())
            return [Event.from_dict(x) for x in dct]
    except Exception as err:
        print("Warning: Error reading events (ignored):", err)
        return []

def save_events_to_disk(evs: list[Event]):
    try:
        with open("save.json", "w", encoding="utf-8") as file:
            file.write(dumps([
                ev.to_dict() for ev in evs
            ]))
    except Exception as err:
        print("Warning: Error saving events (ignored):", err)
