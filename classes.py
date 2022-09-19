from dataclasses import dataclass
from typing import Type

from skilss import Skill, PowerfulStab, FerociousKick


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack_modifier: float
    stamina_modifier: float
    armor_modifier: float
    skill: Type[Skill]


warrior = UnitClass(
    name='Воин',
    max_health=60.0,
    max_stamina=30.0,
    attack_modifier=0.8,
    stamina_modifier=0.9,
    armor_modifier=1.2,
    skill=FerociousKick
)

thief = UnitClass(
    name='Вор',
    max_health=50.0,
    max_stamina=25.0,
    attack_modifier=1.5,
    stamina_modifier=1.2,
    armor_modifier=1.0,
    skill=PowerfulStab
)

classes = [warrior, thief]
