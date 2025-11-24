import pytest
from model.creature import Creature
from service import creature as code
from error import Duplicate, Missing

sample = Creature(
    name="Yeti",
    description="Hirsute Himalayan",
    country="CN",
    area="Himalayas",
    aka="Abominable Snowman",
)


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_one("Yeti")
    assert resp == sample


def test_get_missing():
    with pytest.raises(Missing):
        resp = code.get_one("boxturtle")
