from dataclasses import dataclass
from typing import Optional, Dict
from tomllib import loads

@dataclass
class Requirement:
    name: str
    qty: int

@dataclass
class EventTemplate:
    name: str
    duration: int
    icon: str|None
    description: str
    requires: list[Requirement]

EVENTS = [
    EventTemplate(
        name="Generate electricity",
        description="Send blobs to the power room to generate electricity. Without electricity blobs can't cook (Breaking bad reference) nor have water",
        icon="res/img-evt-power.jpg",
        duration=1,
        requires=[
            Requirement(name="Blob", qty=2),
            Requirement(name="Fuel pipe", qty=1),
            Requirement(name="Voltimeter", qty=1)
        ]
    ),
    EventTemplate(
        name="Visit neighbour",
        description="Go to see if your neighbour is alive. In this lonely world its just nice to see other people. Take care with the radiation",
        icon="res/img-evt-go-outside.jpg",
        duration=3,
        requires=[
            Requirement(name="Blob", qty=1)
        ]
    )
]

EVENTS_AS_DICT = {
    evt.name: evt for evt in EVENTS
}
