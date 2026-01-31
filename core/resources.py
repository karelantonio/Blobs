from dataclasses import dataclass

@dataclass
class Resource:
    name: str
    description: str
    excludes: list[str]
    total: int
    icon: str|None

RESOURCES = [
    Resource(
        name="Blob",
        description="Little beings that only want to survive in this world. In this futuristic world its difficult say which is natural (born) and which is synthetic (made by the Tyrell Corporation)",
        excludes=[],
        icon="res/blob.png",
        total=10,
    ),
    Resource(
        name="Fuel pipe",
        description="A pipe with (unlimited) fuel used in the power room to generate electricity, nobody knows where the fuel comes from but it seems like it never ends",
        excludes=[],
        icon="res/img-fuel-pipe.jpg",
        total=2
    ),
    Resource(
        name="Voltimeter",
        description="Used to control that not too much power is being generated",
        excludes=[],
        icon="res/img-voltimeter.jpg",
        total=5,
    ),
    Resource(
        name="Ventilation fans",
        description="For extra cooling on the hot parts, can prevent fires",
        excludes=[],
        icon="res/img-ventilation.jpg",
        total=2,
    ),
    Resource(
        name="Laser Beam",
        description="Used by the blobs to defend against intruders",
        excludes=[],
        icon="res/img-laser-beam.jpg",
        total=1,
    ),
    Resource(
        name="Anti-radiation clothing",
        description="Going outside may incur in severe damage from the radioactive dust, wear this to reduce this effect",
        excludes=[],
        icon="res/img-antirad.jpg",
        total=2,
    ),
]

RESOURCES_AS_DICT = {res.name: res for res in RESOURCES}
