import random
import turtle
import math
import os

BASE_PATH = os.path.dirname(__file__)

window = turtle.Screen()
window.bgpic(os.path.join(BASE_PATH, 'images', 'background.png'))
window.setup(1200 + 10, 800 + 10)
window.screensize(1200, 800)
# window.tracer(n=2)

# Базовые переменные для расположения и работы с ракетами вражескими и игрока
BASE_X = 0
BASE_Y = -300
ENEMY_BASE_X_MIN = -500
ENEMY_BASE_X_MAX = 500
ENEMY_BASE_Y = 500


def calculate_heading(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    lenght = (dx ** 2 + dy ** 2) ** 0.5
    cos_alpha = dx / lenght
    alpha = math.acos(cos_alpha)
    alpha = math.degrees(alpha)
    if dy < 0:
        alpha = -alpha
    return alpha


def enemy_rocket_missle():
    x = random.randint(ENEMY_BASE_X_MIN, ENEMY_BASE_X_MAX)
    y = ENEMY_BASE_Y
    enemy = turtle.Turtle(visible=False)
    enemy.color('red')
    enemy.hideturtle()
    enemy.speed(0)
    enemy.penup()
    enemy.setpos(x=x, y=y)
    enemy.pendown()
    to_ground = calculate_heading(x1=x, y1=ENEMY_BASE_Y, x2=BASE_X, y2=BASE_Y)
    enemy.setheading(to_ground)
    enemy.showturtle()
    enemy_info = {'missile': enemy, 'target': [BASE_X, BASE_Y],
                  'state': 'launched', 'radius': 0}
    enemy_missiles_rocket.append(enemy_info)


def fire_missile(x, y):
    missile = turtle.Turtle(visible=False)
    missile.color('white')
    missile.hideturtle()
    missile.speed(0)
    missile.penup()
    missile.setpos(x=BASE_X, y=BASE_Y)
    missile.pendown()
    heading = calculate_heading(x1=BASE_X, y1=BASE_Y, x2=x, y2=y)
    missile.setheading(heading)
    missile.showturtle()
    info_about_rocket = {'missile': missile, 'target': [x, y],
                         'state': 'launched', 'radius': 0}
    our_missiles.append(info_about_rocket)


window.onclick(fire_missile)
our_missiles = []
enemy_missiles_rocket = []
numberTic = 0

# Gaming cicle, and use State pattern
while True:
    window.update()
    # ракеты игрока, распаковываем ее данные.
    for info_about_rocket in our_missiles:
        state = info_about_rocket['state']
        missile = info_about_rocket['missile']
        if state == 'launched':
            missile.forward(4)
            target = info_about_rocket['target']
            if missile.distance(x=target[0], y=target[1]) < 20:
                info_about_rocket['state'] = 'explode'
                missile.shape('circle')
        elif state == 'explode':
            info_about_rocket['radius'] += 1
            # check radius, and change rocket status
            if info_about_rocket['radius'] > 5:
                info_about_rocket['state'] = 'dead'
                missile.clear()
                missile.hideturtle()
            else:
                missile.shapesize(info_about_rocket['radius'])
        # elif state == 'dead':  # if rocket is make BOOM

    #ракеты вражеская, распаковываем ее данные.
    for info_about_enemy_rocket in enemy_missiles_rocket:
        state = info_about_enemy_rocket['state']
        enemy_rocket = info_about_enemy_rocket['missile']
        if state == 'launched':
            enemy_rocket.forward(5)
            target = info_about_enemy_rocket['target']
            if enemy_rocket.distance(x=target[0], y=target[1]) < 20:
                info_about_enemy_rocket['state'] = "explode"
                enemy_rocket.shape('circle')
        elif state == 'explode':
            info_about_enemy_rocket['radius'] += 1
            if info_about_enemy_rocket['radius'] > 4:
                info_about_enemy_rocket['state'] = 'dead'
                enemy_missiles_rocket.remove(info_about_enemy_rocket)
                enemy_rocket.clear()
                enemy_rocket.hideturtle()
            else:
                enemy_rocket.shapesize(info_about_enemy_rocket['radius'])

    #уничтожаем вражеские и  ракеты игрока, чтобы не захломлять список.
    dead_missiles = [info_about_rocket for info_about_rocket in our_missiles if
                     info_about_rocket['state'] == 'dead']  # Списовая сборка
    for dead in dead_missiles:
        our_missiles.remove(dead)

    #В бесконечном цикле делаем вызов функции создания ракеты вражеской, которая рандомно создается и летит к земле.
    if numberTic % random.randint(20, 100) == 0:
            enemy_rocket_missle()
            numberTic = 0
    numberTic += 1