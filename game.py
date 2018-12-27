import random
import turtle
import math
import os

BASE_PATH = os.path.dirname(__file__)

window = turtle.Screen()
window.bgpic(os.path.join(BASE_PATH, 'images', 'background.png'))
window.setup(1200 + 10, 800 + 10)
window.screensize(1200, 800)
window.tracer(n=2)



# Базовые переменные для расположения и работы с ракетами вражескими и игрока
BASE_X = 0
BASE_Y = -300
# ENEMY_BASE_X_MIN = -600
# ENEMY_BASE_X_MAX = 600
# ENEMY_BASE_Y = 400
ENEMY_COUNT = 5  # 5 вражеских ракет, для контроля ракет летящих на игрока


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


'''
Функция которая создает ракеты
для сжатия кода, не создавания двух функций практически дублирующих друг друга
'''
def create_missile(color, x, y, x2, y2):
    missile = turtle.Turtle(visible=False)
    missile.color(color)
    missile.hideturtle()
    missile.speed(0)
    missile.penup()
    missile.setpos(x=x, y=y)
    missile.pendown()
    heading_rocket = missile.towards(x2, y2)  # заменяем calculate_heading(x1=x, y1=ENEMY_BASE_Y, x2=BASE_X, y2=BASE_Y) на функцию towards()
    missile.setheading(heading_rocket)
    missile.showturtle()
    info_about_rockets = {'missile': missile, 'target': [x2, y2],
                          'state': 'launched', 'radius': 0}
    return info_about_rockets


def fire_missile(x, y):
    info_about_rocket = create_missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info_about_rocket)

def fire_enemy_missile():
    x= random.randint(-600,600)
    y = 400
    info_about_rocket = create_missile(color='red', x=x, y=y, x2=BASE_X, y2=BASE_Y)
    enemy_missiles_rocket.append(info_about_rocket)

def move_missiles(missiles):
    for info_about_rocket in missiles:
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
        elif state == 'dead':
            missile.clear()
            missile.hideturtle()
        # elif state == 'dead':  # if rocket is make BOOM
    # уничтожаем ракеты игрока, чтобы не захламлять список
    dead_missiles = [info_about_rocket for info_about_rocket in missiles if
                     info_about_rocket['state'] == 'dead']  # Списовая сборка
    for dead in dead_missiles:
        missiles.remove(dead)



def check_enemy_count():
    if len(enemy_missiles_rocket) < ENEMY_COUNT:
        fire_enemy_missile()

def check_rocket_collision():
    for our_info in our_missiles:
        if our_info['state'] != 'explode':
            continue
        our_missile = our_info['missile']
        for enemy_info in enemy_missiles_rocket:
            enemy_missiles = enemy_info['missile']
            if enemy_missiles.distance(our_missile.xcor(),our_missile.ycor())< 20:
                enemy_info['state'] = 'dead'


our_missiles = []
enemy_missiles_rocket = []
window.onclick(fire_missile)

# Gaming cicle, and use State pattern
while True:
    window.update()
    check_enemy_count()
    check_rocket_collision()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles_rocket)
