import pygame
import time
import random

DIRECTIONS = ('L', 'R', 'U', 'D')

class Display():
    def __init__(self):
        self.__window_size = (800, 600)
        self.__window_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.__window_size))
        pygame.display.set_icon(pygame.image.load("img/pacman_icon.png"))
        self.set_caption(3)

    def weight(self):
        return self.__window_size[0]

    def height(self):
        return self.__window_size[1]

    def set_caption(self, HP):
        pygame.display.set_caption(f"PACMAN: {HP} ❤️")

    def screen_fill(self):
        self.screen.fill(self.__window_color)

    def screen_blit(self, image):
        self.screen.blit(image.image(), image.rect())

    def warning_msg(self, text, timer):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render(text, True, (255, 255, 255))
        self.screen.blit(text, (self.__window_size[0] // 2 - text.get_width() // 2,
            self.__window_size[1] // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(timer)


class Image():
    def __init__(self, path):
        self.__image = pygame.image.load(path)
        self.__rect = self.__image.get_rect()
        self.width = self.__rect.width
        self.height = self.__rect.height

    def x(self):
        return self.__rect.x
    
    def y(self):
        return self.__rect.y
        
    def set_x(self, new_x):
        self.__rect.x = new_x

    def set_y(self, new_y):
        self.__rect.y = new_y

    def rect(self):
        return self.__rect

    def image(self):
        return self.__image



class Pacman():
    def __init__(self):
        self.HP = 3
        self.img = Image("img/pacman_80.png")
        self.speed_x = self.img.width/2
        self.speed_y = self.img.height/2


class Monster():
    def __init__(self):
        self.img = Image("img/monster_red_80.png")
        self.speed_x = self.img.width/2
        self.speed_y = self.img.height/2
        self.__direction = ''

    def move(self):
        self.__direction = random.choice(DIRECTIONS)
        if self.__direction == 'L':
            x = self.img.x() - self.speed_x
            if x < 0:
                x = 0
            self.img.set_x(x)
        elif self.__direction == 'R':
            x = self.img.x() + self.speed_x
            if x > display.weight() - self.img.width:
                x = display.weight() - self.img.width
            self.img.set_x(x)
        elif self.__direction == 'U':
            y = self.img.y() - self.speed_y
            if y < 0:
                y = 0
            self.img.set_y(y)
        elif self.__direction == 'D':
            y = self.img.y() + self.speed_y
            if y > display.height() - self.img.height:
                y = display.height() - self.img.height
            self.img.set_y(y)



pygame.init()

clock = pygame.time.Clock()
fps = 10

display = Display()

pacman = Pacman()
monster1 = Monster()
monster1.img.set_x(display.weight() - monster1.img.width)
monster1.img.set_y(display.height() - monster1.img.height)


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
        x = pacman.img.x() - pacman.speed_x
        if x < 0:
            x = 0
        pacman.img.set_x(x)

    if keys[pygame.K_RIGHT]:
        x = pacman.img.x() + pacman.speed_x
        if x > display.weight() - pacman.img.width:
            x = display.weight() - pacman.img.width
        pacman.img.set_x(x)

    if keys[pygame.K_UP]:
        y = pacman.img.y() - pacman.speed_y
        if y < 0:
            y = 0
        pacman.img.set_y(y)

    if keys[pygame.K_DOWN]:
        y = pacman.img.y() + pacman.speed_y
        if y > display.height() - pacman.img.height:
            y = display.height() - pacman.img.height
        pacman.img.set_y(y)

    # передвижение монстра - автоматически
    monster1.move()

    if pacman.img.rect().colliderect(monster1.img.rect()):
        HP = pacman.HP 
        HP -= 1
        if HP <= 0:
            display.warning_msg(f"Вы проиграли!", 2000)

            running = False
            break
        else:
            pacman.HP = HP
            display.set_caption(HP)

            display.warning_msg(f"Осторожнее! Осталось: {HP} HP", 1000)

            pacman.img.set_x(0)
            pacman.img.set_y(0)
        time.sleep(1)

    display.screen_fill()
    display.screen_blit(pacman.img)
    display.screen_blit(monster1.img)

    pygame.display.flip()   # обновление экрана
    clock.tick(fps)

pygame.quit()