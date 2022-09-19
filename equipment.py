import json
from dataclasses import dataclass
import random
from typing import List, Optional
import marshmallow_dataclass

from config import DATA_DIR


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    def damage_dealt(self) -> float:
        return random.uniform(self.min_damage, self.max_damage)


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


EquipmentDataSchema = marshmallow_dataclass.class_schema(EquipmentData)


class Equipment:
    def __init__(self):
        self._data = self._load_data()

    def _load_data(self) -> EquipmentData:
        with open(f'{DATA_DIR}/equipment.json', 'r') as f:
            data = json.load(f)
            return EquipmentDataSchema().load(data)

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        for weapon in self._data.weapons:
            if weapon.name == weapon_name:
                return weapon

        return None

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        for armor in self._data.armors:
            if armor.name == armor_name:
                return armor

        return None

    def get_weapon_names(self) -> List[str]:
        return [weapon.name for weapon in self._data.weapons]

    def get_armor_names(self) -> List[str]:
        return [armor.name for armor in self._data.armors]
