import pygame
import time
import random
import math

WINDOW_SIZE = (800, 640)
DIRECTIONS = ('L', 'R', 'U', 'D')
FPS = 10
objects = None
HP = 3
scores = 0

# Класс для работы с экраном
class Display():
    def __init__(self):
        self.__window_color = (255, 255, 255)
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_icon(pygame.image.load("img/pacman_icon.png"))
        self.set_caption()

    def set_caption(self):
        pygame.display.set_caption(f"PACMAN HP: {'❤' * HP} Очки: {scores}")

    def screen_fill(self):
        self.screen.fill(self.__window_color)

    def screen_blit(self, image):
        self.screen.blit(image.image(), image.rect())

    def warning_msg(self, text, timer):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render(text, True, (255, 255, 255))
        self.screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2,
            WINDOW_SIZE[1] // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(timer)


# Класс для описания спрайтов
class Image():
    def __init__(self, path, position=''):
        self.__image = pygame.image.load(path)
        self.__rect = self.__image.get_rect()
        self.width = self.__rect.width
        self.height = self.__rect.height
        self.__start_position = position
        self.set_start_position()

    @property
    def x(self):
        return self.__rect.x

    @property
    def y(self):
        return self.__rect.y

    @x.setter
    def x(self, new_x):
        self.__rect.x = new_x

    @y.setter
    def y(self, new_y):
        self.__rect.y = new_y

    def rect(self):
        return self.__rect

    def image(self):
        return self.__image

    def set_start_position(self):
        match self.__start_position:
            case 'LU':
                self.x = 0
                self.y = 0
            case 'RU':
                self.x = WINDOW_SIZE[0] - self.width
                self.y = 0
            case 'LD':
                self.x = 0
                self.y = WINDOW_SIZE[1] - self.height
            case 'RD':
                self.x = WINDOW_SIZE[0] - self.width
                self.y = WINDOW_SIZE[1] - self.height

# Класс "Героя"
class Pacman:
    def __init__(self, position):
        self.img = Image("img/pacman.png", position)
        self.speed_x = self.img.width
        self.speed_y = self.img.height

    def move_left(self):
        x = self.img.x - self.speed_x
        if x < 0:
            x = 0
        self.img.x = x

    def move_right(self):
        x = self.img.x + self.speed_x
        if x > WINDOW_SIZE[0] - self.img.width:
            x = WINDOW_SIZE[0] - self.img.width
        self.img.x = x

    def move_up(self):
        y = self.img.y - self.speed_y
        if y < 0:
            y = 0
        self.img.y = y

    def move_down(self):
        y = self.img.y + self.speed_y
        if y > WINDOW_SIZE[1] - self.img.height:
            y = WINDOW_SIZE[1] - self.img.height
        self.img.y = y

# Класс мостров
class Monster:
    def __init__(self, img_path, position):
        self.img = Image(img_path, position)
        self.speed_x = self.img.width
        self.speed_y = self.img.height

    def move(self, source: Display):
        direction = random.choice(DIRECTIONS)
        if direction == 'L':
            x = self.img.x - self.speed_x
            if x < 0:
                x = 0
            self.img.x = x
        elif direction == 'R':
            x = self.img.x + self.speed_x
            if x > WINDOW_SIZE[0] - self.img.width:
                x = WINDOW_SIZE[0] - self.img.width
            self.img.x = x
        elif direction == 'U':
            y = self.img.y - self.speed_y
            if y < 0:
                y = 0
            self.img.y = y
        elif direction == 'D':
            y = self.img.y + self.speed_y
            if y > WINDOW_SIZE[1] - self.img.height:
                y = WINDOW_SIZE[1] - self.img.height
            self.img.y = y


# Класс еды для Пэкмэна
class Food:
    def __init__(self, img_path):
        self.img = Image(path=img_path)
        self.timer_interval = 3
        self.timer = 0

    def positioning(self):
        if self.timer > 0:
            self.timer -= 1
            return

        while True:
            x = random.randint(0, (math.floor(WINDOW_SIZE[0]/self.img.width) - 1) * self.img.width)
            y = random.randint(0, (math.floor(WINDOW_SIZE[1]/self.img.height) - 1) * self.img.height)

            unique = True  # Флаг уникальности координат
            for obj in objects:
                if obj.img.x == x and obj.img.y == y:
                    unique = False
                    break  # Прерываем цикл, если нашли совпадение

            if unique:
                self.img.x = x
                self.img.y = y
                self.timer = self.timer_interval
                break  # Прерываем внешний цикл только если координаты уникальны


pygame.init()

clock = pygame.time.Clock()

display = Display()

pacman = Pacman(position='LU')
monster1 = Monster(img_path="img/monster_red.png", position='RD')
objects = [pacman, monster1]

cherry = Food(img_path="img/cherry.png")

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # if event.type == pygame.MOUSEMOTION:
        #     mouse_x, mouse_y = pygame.mouse.get_pos()
        #     pacman.img.__rect.center = mouse_x, mouse_y

    # передвижение Pacman - клавишами
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman.move_left()
    if keys[pygame.K_RIGHT]:
        pacman.move_right()
    if keys[pygame.K_UP]:
        pacman.move_up()
    if keys[pygame.K_DOWN]:
        pacman.move_down()

    # передвижение монстра - автоматически
    monster1.move(display)

    # Пэкмэн накнуся на монстра
    if pacman.img.rect().colliderect(monster1.img.rect()):
        HP -= 1
        if HP <= 0:
            display.warning_msg(f"Игра окончена! Результат: {scores}", 2000)

            running = False
            break
        else:
            display.set_caption()

            display.warning_msg(f"Осторожнее! Осталось HP: {HP}", 1000)

            for obj in objects:
                obj.img.set_start_position()
        time.sleep(1)

    # переназначение места пищи, если пришло время
    cherry.positioning()

    # Пэкмэн съел еду
    if pacman.img.rect().colliderect(cherry.img.rect()):
        scores += 1
        display.set_caption()
        cherry.timer = 0
        # назначение нового места пищи
        cherry.positioning()
        time.sleep(1)

    display.screen_fill()
    display.screen_blit(pacman.img)
    display.screen_blit(monster1.img)
    display.screen_blit(cherry.img)

    pygame.display.flip()   # обновление экрана
    clock.tick(FPS)

pygame.quit()