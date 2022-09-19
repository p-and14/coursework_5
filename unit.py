from __future__ import annotations
from abc import ABC, abstractmethod
import random

from classes import classes, UnitClass
from equipment import Equipment, Weapon, Armor


class BaseUnit(ABC):
    def __init__(self, name: str, unit_class: str, weapon: str, armor: str):
        self.__name = name
        self.__unit_class = classes[0] if unit_class == "Воин" else classes[1]
        self.__health_points = self.__unit_class.max_health
        self.__stamina_points = self.__unit_class.max_stamina
        self.__weapon = Equipment().get_weapon(weapon)
        self.__armor = Equipment().get_armor(armor)
        self.__skill_used = False

    @property
    def name(self) -> str:
        return self.__name

    @property
    def unit_class(self) -> UnitClass:
        return self.__unit_class

    @property
    def health_points(self) -> float:
        return round(self.__health_points, 1)

    @health_points.setter
    def health_points(self, value: float) -> None:
        self.__health_points = value

    @property
    def stamina_points(self) -> float:
        return round(self.__stamina_points, 1)

    @stamina_points.setter
    def stamina_points(self, value: float) -> None:
        self.__stamina_points = value

    @property
    def weapon(self) -> Weapon:
        return self.__weapon

    @property
    def armor(self) -> Armor:
        return self.__armor

    @property
    def skill_used(self) -> bool:
        return self.__skill_used

    @skill_used.setter
    def skill_used(self, value: bool) -> None:
        self.__skill_used = value

    def _target_armor(self, target: BaseUnit) -> float:
        if target.stamina_points <= target.armor.stamina_per_turn:
            target_armor = 0.0
        else:
            target_armor = round((target.armor.defence * target.unit_class.armor_modifier), 1)
            target.stamina_points -= target.armor.stamina_per_turn
        return target_armor

    def _total_damage(self, target: BaseUnit) -> float:
        weapon_damage = round(self.weapon.damage_dealt(), 1)
        attacker_damage = round((weapon_damage * self.unit_class.attack_modifier), 1)
        target_armor = self._target_armor(target)

        if attacker_damage > target_armor:
            total_damage = attacker_damage - target_armor
        else:
            total_damage = 0.0
        return round(total_damage, 1)

    def taking_damage(self, damage: float) -> None:
        if self.health_points >= damage:
            self.health_points -= damage
        else:
            self.health_points = 0

    def apply_skill(self, target: BaseUnit) -> str:
        return self.unit_class.skill().use(self, target)

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass


class PlayerUnit(BaseUnit, ABC):
    def __repr__(self):
        return f"name: {self.name}, class: {self.unit_class}, " \
               f"hp: {round(self.health_points, 1)}, sp: {round(self.stamina_points, 1)}, " \
               f"weapon: {self.weapon}, armor: {self.armor}"

    def hit(self, target: BaseUnit) -> str:
        damage = self._total_damage(target)

        if self.stamina_points >= self.weapon.stamina_per_hit:
            self.stamina_points -= self.weapon.stamina_per_hit
            if damage:
                target.taking_damage(damage)
                result = f"{self.name}, используя {self.weapon.name}," \
                         f" пробивает {target.armor.name} соперника и наносит {damage} урона."
            else:
                result = f"{self.name}, используя {self.weapon.name}, наносит удар," \
                         f" но {target.armor.name} соперника его останавливает."
        else:
            result = f"{self.name} попытался использовать {self.weapon.name}," \
                     f" но у него не хватило выносливости."

        return result


class EnemyUnit(BaseUnit, ABC):
    def __repr__(self):
        return f"name: {self.name}, class: {self.unit_class}, " \
               f"hp: {round(self.health_points, 1)}, sp: {round(self.stamina_points, 1)}, " \
               f"weapon: {self.weapon}, armor: {self.armor}"

    def hit(self, target: BaseUnit) -> str:
        if not self.skill_used:
            use_skill = random.random()
            if use_skill > 0.8:
                self.skill_used = True
                return self.apply_skill(target)

        if self.stamina_points >= self.weapon.stamina_per_hit:
            damage = self._total_damage(target)
            self.stamina_points -= self.weapon.stamina_per_hit

            if damage:
                target.taking_damage(damage)
                result = f"{self.name}, используя {self.weapon.name}," \
                         f" пробивает {target.armor.name} соперника и наносит {damage} урона."
            else:
                result = f"{self.name}, используя {self.weapon.name}, наносит удар," \
                         f" но {target.armor.name} соперника его останавливает."
        else:
            result = f"{self.name} попытался использовать {self.weapon.name}," \
                     f" но у него не хватило выносливости."

        return result
