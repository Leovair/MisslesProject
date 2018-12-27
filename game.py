import random
import turtle
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
ENEMY_COUNT = 1  # 5 вражеских ракет, для контроля ракет летящих на игрока

'''
Создадим класс Missiles, в котором будет наш объект ракеты. 
'''
class Missile:
    def __init__(self, x, y, color, x2, y2):
        # self.x = x
        # self.y = y
        self.color = color
        pen = turtle.Turtle(visible=False)
        pen.color(color)
        pen.speed(0)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        heading_rocket = pen.towards(x2, y2)
        pen.setheading(heading_rocket)
        pen.showturtle()
        self.pen = pen

        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(4)
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
                self.pen.shape('circle')
        elif self.state == 'explode':
            self.radius += 1
            # check radius, and change rocket status
            if self.radius > 5:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()


'''
Функция которая создает ракеты
для сжатия кода, не создавания двух функций практически дублирующих друг друга
'''
def create_missile(color, x, y, x2, y2):
    missile = Missile(x=x, y=y, color=color, x2=x2, y2=y2)
    return missile


def fire_missile(x, y):
    info_about_rocket = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info_about_rocket)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    info_about_rocket = Missile(color='red', x=x, y=y, x2=BASE_X, y2=BASE_Y)
    enemy_missiles_rocket.append(info_about_rocket)


def move_missiles(missiles):
    for missile in missiles:
        missile.step()
    # elif state == 'dead':  # if rocket is make BOOM
    # уничтожаем ракеты игрока, чтобы не захламлять список
    dead_missiles = [missile for missile in missiles if
                     missile.state == 'dead']  # Списовая сборка
    for dead in dead_missiles:
        missiles.remove(dead)


def check_enemy_count():
    if len(enemy_missiles_rocket) < ENEMY_COUNT:
        fire_enemy_missile()


def check_rocket_collision():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        for enemy_missile in enemy_missiles_rocket:
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius * 10:
                enemy_missile.state = 'dead'


def our_base():
    base = turtle.Turtle(visible=True)
    base.hideturtle()
    base.speed(0)
    base.penup()
    base.setpos(x=BASE_X, y=BASE_Y)
    pic_path = os.path.join(BASE_PATH, 'images', 'base.gif')
    window.register_shape(pic_path)
    base.shape(pic_path)
    base.showturtle()


def game_over():
    return base_health < 0


window.onclick(fire_missile)

our_missiles = []  # список наших ракет
enemy_missiles_rocket = []  # писок вражеских ракет
base_health = 2000


def check_impact_to_base():
    global base_health
    for enemy_missile in enemy_missiles_rocket:
        if enemy_missile.state != 'explode':
            continue
        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_missile.radius * 10:
            base_health -= 100
            print('basehealth',base_health)

while True:  # Gaming cicle, and use State pattern
    window.update()
    check_impact_to_base()
    if game_over():
        continue
    check_enemy_count()
    check_rocket_collision()
    our_base()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles_rocket)
