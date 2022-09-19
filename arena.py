from typing import Optional

from unit import BaseUnit


class Arena:
    player = None
    enemy = None
    amount_stamina_recovering = 2
    game_is_on = False

    def __repr__(self):
        return f"player: {self.player}\nenemy: {self.enemy}"

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_on = True

    def next_move(self) -> str:
        self.regenerate_stamina()
        player_hit = self.player.hit(self.enemy)
        enemy_hit = self.enemy.hit(self.player)

        if self.check_players_health() == "Игрок выиграл битву!":
            result = f"{player_hit} {self.end_game()}"
        elif self.check_players_health() == "Игрок проиграл битву!":
            result = f"{enemy_hit} {self.end_game()}"
        elif self.check_players_health() == "Ничья!":
            result = f"{enemy_hit} {player_hit} {self.end_game()}"
        else:
            result = f"{player_hit} {enemy_hit}"
        return result

    def regenerate_stamina(self) -> None:
        units = (self.player, self.enemy)
        for unit in units:
            if unit.stamina_points < unit.unit_class.max_stamina - \
                    (self.amount_stamina_recovering * unit.unit_class.stamina_modifier):
                unit.stamina_points += (self.amount_stamina_recovering * unit.unit_class.stamina_modifier)
            else:
                unit.stamina_points = unit.unit_class.max_stamina

    def check_players_health(self) -> Optional[str]:
        if self.player.health_points <= 0 and self.enemy.health_points <= 0:
            result = "Ничья!"
        elif self.player.health_points <= 0:
            result = "Игрок проиграл битву!"
        elif self.enemy.health_points <= 0:
            result = "Игрок выиграл битву!"
        else:
            result = None

        return result

    def end_game(self) -> Optional[str]:
        self.game_is_on = False
        return self.check_players_health()
