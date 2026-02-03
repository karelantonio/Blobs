from dataclasses import dataclass

@dataclass
class Resource:
    name: str
    description: str
    excludes: list[str]
    includes: list[str]
    total: int
    icon: str|None

RESOURCES = [
    Resource(
        name="Blob",
        description="Little beings that only want to survive in this world. In this futuristic world its difficult say which is natural (born) and which is synthetic (made by the Tyrell Corporation)",
        excludes=[],
        includes=[],
        icon="res/blob.png",
        total=10,
    ),
    Resource(
        name="Fuel pipe",
        description="A pipe with (unlimited) fuel used in the power room to generate electricity, nobody knows where the fuel comes from but it seems like it never ends",
        excludes=["Laser Beam"],
        includes=[],
        icon="res/img-fuel-pipe.jpg",
        total=2
    ),
    Resource(
        name="Voltimeter",
        description="Used to control that not too much power is being generated",
        excludes=[],
        includes=[],
        icon="res/img-voltimeter.jpg",
        total=5,
    ),
    Resource(
        name="Ventilation fans",
        description="For extra cooling on the hot parts, can prevent fires",
        excludes=[],
        includes=[],
        icon="res/img-ventilation.jpg",
        total=2,
    ),
    Resource(
        name="Laser Beam",
        description="Used by the blobs to defend against intruders",
        excludes=["Fuel pipe"],
        includes=[],
        icon="res/img-laser-beam.jpg",
        total=1,
    ),
    Resource(
        name="Anti-radiation clothing",
        description="Going outside may incur in severe damage from the radioactive dust, wear this to reduce this effect",
        excludes=[],
        includes=["Blob"],
        icon="res/img-antirad.jpg",
        total=2,
    ),
    Resource(
        name="Protein",
        description="Used instead of food. No questions",
        excludes=[],
        includes=[],
        icon="res/img-protein.jpg",
        total=5,
    ),
    Resource(
        name="Water bottle",
        description="Half full bottles of water, can be used to carry more water or the blobs can even drink the water left in them",
        excludes=[],
        includes=[],
        icon="res/img-water.jpg",
        total=2,
    ),
    Resource(
        name="Chlorine",
        description="Used for water treatment, however you should take some care and use gloves",
        excludes=[],
        includes=["Gloves"],
        icon="res/img-chlorine.jpg",
        total=1,
    ),
    Resource(
        name="Gloves",
        description="Protection against heat and some chemicals",
        excludes=[],
        includes=[],
        icon="res/img-gloves.jpg",
        total=3,
    ),
    Resource(
        name="Electric sheep",
        description="This electric animal has its control panel hidden, so its less embarrassing for you to show it to your neighbours. But is it any different than a 'real' one?",
        excludes=[],
        includes=[],
        icon="res/img-elecsheep.jpg",
        total=1,
    )
]

RESOURCES_AS_DICT = {res.name: res for res in RESOURCES}
