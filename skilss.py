from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class Skill(ABC):
    user = None
    target = None

    @property
    @abstractmethod
    def skill_name(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @property
    @abstractmethod
    def required_stamina(self):
        pass

    @abstractmethod
    def skill_effect(self):
        pass

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        self.user = user
        self.target = target
        if user.stamina_points >= self.required_stamina:
            return self.skill_effect()
        else:
            return f"{user.name} попытался использовать {self.skill_name}, но у него не хватило выносливости."


class FerociousKick(Skill, ABC):
    skill_name = "Свирепый пинок"
    damage = 12
    required_stamina = 6

    def skill_effect(self) -> str:
        self.user.stamina_points -= self.required_stamina
        self.target.taking_damage(self.damage)

        return f"{self.user.name} использует {self.skill_name} и наносит {self.damage} урона сопернику."


class PowerfulStab(Skill, ABC):
    skill_name = "Мощный укол"
    damage = 15
    required_stamina = 5

    def skill_effect(self) -> str:
        self.user.stamina_points -= self.required_stamina
        self.target.taking_damage(self.damage)

        return f"{self.user.name} использует {self.skill_name} и наносит {self.damage} урона сопернику."
