import random
import turtle
import math

window = turtle.Screen()
window.bgpic('images/background.png')
window.setup(1200 + 10, 800 + 10)
window.screensize(1200, 800)

BASE_X = 0
BASE_Y = -300
ENEMY_BASE_X = 0
ENEMY_BASE_Y = 500

def calculate_enime(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2-y1
    lenght = (dx ** 2 + dy ** 2)**0.5
    cos_alpha = dx / lenght
    alpha = math.acos(cos_alpha)
    alpha = math.degrees(alpha)
    return alpha

def calculate_heading(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    lenght = (dx ** 2 + (dy) ** 2) ** 0.5
    cos_alpha = dx / lenght
    alpha = math.acos(cos_alpha)
    alpha = math.degrees(alpha)
    if dy < 0:
        alpha = -alpha
    return alpha

def enemy_missle():
    enemy  = turtle.Turtle()
    enemy.color('red')
    # enemy.hideturtle()
    enemy.speed(1)
    enemy.penup()
    enemy.setpos(x=ENEMY_BASE_X,y=ENEMY_BASE_Y)

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
    info_about_rocket = {'missile': missile, 'target': [x, y], 'state': 'launched', 'radius': 0}
    our_missiles.append(info_about_rocket)


window.onclick(fire_missile)
our_missiles = []
enemy_missle()
# Gaming cicle, and use State pattern
while True:
    window.update()

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
            #check radius, and change rocket status
            if info_about_rocket['radius']>5:
                info_about_rocket['state'] = 'dead'
                missile.clear()
                missile.hideturtle()
            else:
                missile.shapesize(info_about_rocket['radius'])
        elif state == 'dead':#if rocket is make BOOM
            dead_missiles = [info_about_rocket for info_about_rocket in our_missiles if
                             info_about_rocket['state'] == 'dead']  # Списовая сборка
            for dead in dead_missiles:
                our_missiles.remove(dead)


