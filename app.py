from flask import Flask, render_template, request, redirect, url_for

from unit import PlayerUnit, EnemyUnit
from classes import thief, warrior
from equipment import Equipment
from arena import Arena

app = Flask(__name__)

heroes = {}
arena = Arena()
battle_result = []


@app.route("/")
def main_page():
    heroes.clear()
    battle_result.clear()
    return render_template("index.html")


@app.route("/choose-hero/", methods=["GET", "POST"])
def choose_hero():
    if request.method == "GET":
        result = {
            "header": "Выберите героя",
            "classes": [thief.name, warrior.name],
            "weapons": Equipment().get_weapon_names(),
            "armors": Equipment().get_armor_names()
        }
        return render_template("hero_choosing.html", result=result)

    elif request.method == "POST":
        req = request.form
        player = PlayerUnit(req["name"], req["unit_class"], req["weapon"], req["armor"])
        heroes["player"] = player
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy", methods=["GET", "POST"])
def choose_enemy():
    if request.method == "GET":
        result = {
            "header": "Выберите врага",
            "classes": [thief.name, warrior.name],
            "weapons": Equipment().get_weapon_names(),
            "armors": Equipment().get_armor_names()
        }
        return render_template("hero_choosing.html", result=result)

    elif request.method == "POST":
        req = request.form
        enemy = EnemyUnit(req["name"], req["unit_class"], req["weapon"], req["armor"])
        heroes["enemy"] = enemy
        return redirect(url_for("fight"))


@app.route("/fight/")
def fight():
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes, result='Бой начался!')


@app.route("/fight/hit")
def hit():
    if arena.game_is_on:
        result = arena.next_move()
        battle_result.append(result)
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return redirect(url_for("end_fight"))


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_on:
        if not arena.player.skill_used:
            result = arena.player.apply_skill(arena.enemy)
            if arena.check_players_health():
                result = f"{result} {arena.end_game()}"
            else:
                result += f" {arena.enemy.hit(arena.player)}"
            arena.player.skill_used = True
            battle_result.append(result)
        else:
            result = "Навык уже использован."
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return redirect(url_for("end_fight"))


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_on:
        arena.regenerate_stamina()
        result = arena.enemy.hit(arena.player)
        if arena.check_players_health():
            result = f"{result} {arena.end_game()}"
        battle_result.append(result)
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return redirect(url_for("end_fight"))


@app.route("/fight/end-fight")
def end_fight():
    # arena.end_game()
    return redirect(url_for("main_page"))


@app.route("/fight/show-statistics")
def show_statistics():
    result = " ".join(battle_result)
    return render_template("fight.html", heroes=heroes, battle_result=result)


if __name__ == "__main__":
    app.run()
