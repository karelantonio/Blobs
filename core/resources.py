from dataclasses import dataclass
from typing import Optional, Dict
from tomllib import loads

@dataclass
class Tag:
    name: str
    description: str

def load_tags():
    # Exception: We assume in the rest of the program that this
    # json file was loaded successfully, so any error here should
    # be fatal
    with open("./res/resource-tags.toml", "r", encoding="utf-8") as file:
        dkt = loads(file.read())
        res = dict()
        for key, value in dkt.items():
            match value:
                case {"name": name, "description": description}:
                    res[key] = Tag(name=name, description=description)
        return res

TAGS: Dict[str,Tag] = load_tags()
