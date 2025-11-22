from pydantic import BaseModel


class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str
    aka: str


thing1 = Creature(
    name="yeti",
    country="cn",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)

print("name is ", thing1.name)