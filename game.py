import random
import turtle
import math
window = turtle.Screen()
window.bgpic('images/background.png')
window.setup(1200 + 10, 800 + 10)
window.screensize(1200, 800)

BASE_X = 0
BASE_Y = -300

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

def fire_missile(x,y):
    missile = turtle.Turtle(visible=False)
    missile.color('white')
    missile.hideturtle()
    missile.speed(0)
    missile.penup()
    missile.setpos(x=BASE_X, y=BASE_Y)
    missile.pendown()
    heading = calculate_heading(x1=BASE_X, y1=BASE_Y, x2 =x ,y2=y)
    missile.setheading(heading)
    missile.showturtle()


    our_missiles.append(missile)
    our_missiles_target.append([x,y])
    our_missiles_state.append('launched')
    our_missiles_radius.append(0)
    # missile.forward(500)
    # missile.shape('circle')
    # missile.shapesize(2)
    # missile.shapesize(3)
    # missile.shapesize(4)
    # missile.clear()
    # missile.hideturtle()

# def airplane(y):
#     pen = turtle.Turtle()
#     pen.color('red')
#     for current_x in [-400,-200,0, 200,400]:
#         pen.penup()
#         pen.setpos(current_x, y=y)
#         pen.pendown()
#         pen.circle(radius=random.randint(50,200))
#         pen.penup()
#         pen.forward(100)
#         pen.pendown()
#         pen.circle(radius=100)

#
# airplane(100)

window.onclick(fire_missile)
our_missiles = []
our_missiles_target = []#записываем цель
our_missiles_radius = []
our_missiles_state = []
#Делаем бесконечный цикл
while True:
    window.update()

    for num, missile in enumerate(our_missiles):
        if our_missiles_state[num] == 'launched':
            missile.forward(4)
            target = our_missiles_target[num]
            if missile.distance(x=target[0], y=target[1]) < 20:
                our_missiles_state[num] = 'explode'
                missile.shape('circle')
        elif our_missiles_state[num] == 'explode':
            our_missiles_radius[num] += 1
            missile.shapesize(our_missiles_radius[num])

