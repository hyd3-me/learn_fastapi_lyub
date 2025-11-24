from pydantic import BaseModel


class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str
    aka: str

    def __eq__(self, other):
        if not isinstance(other, Creature):
            return False
        return (
            self.name == other.name
            and self.description == other.description
            and self.country == other.country
            and self.area == other.area
            and self.aka == other.aka
        )
