import pygame
import time

class Image():
    def __init__(self, path, speed=1):
        self.__image = pygame.image.load(path)
        self.speed = speed
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


def get_caption(HP):
    return f"PACMAN: {HP} ❤️"


pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode((window_size))
icon = pygame.image.load("img/pacman_icon.png")
pygame.display.set_icon(icon)

pacman = Pacman()

img_monster1 = Image("img/monster_red_80.png")

pygame.display.set_caption(get_caption(3))

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

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x = pacman.img.x() - pacman.img.speed
        if x < 0:
            x = 0
        pacman.img.set_x(x)

    if keys[pygame.K_RIGHT]:
        x = pacman.img.x() + pacman.img.speed
        if x > window_size[0] - pacman.img.width:
            x = window_size[0] - pacman.img.width
        pacman.img.set_x(x)

    if keys[pygame.K_UP]:
        y = pacman.img.y() - pacman.img.speed
        if y < 0:
            y = 0
        pacman.img.set_y(y)

    if keys[pygame.K_DOWN]:
        y = pacman.img.y() + pacman.img.speed
        if y > window_size[1] - pacman.img.height:
            y = window_size[1] - pacman.img.height
        pacman.img.set_y(y)

    img_monster1.set_x(100)
    img_monster1.set_y(100)
    # img_monster1.set_x(window_size[0] - img_monster1.width)
    # img_monster1.set_y(window_size[1] - img_monster1.height)

    if pacman.img.rect().colliderect(img_monster1.rect()):
        HP = pacman.HP 
        HP -= 1
        if HP <= 0:
            print("pacman is defeated!")
            running = False
            break
        else:
            pacman.HP = HP
            pygame.display.set_caption(get_caption(HP))

            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 74)
            text = font.render(f"Pacman is hurt! Осталось: {HP} HP", True, (255, 255, 255))
            screen.blit(text, (window_size[0] // 2 - text.get_width() // 2, window_size[1] // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(1000)

            pacman.img.set_x(0)
            pacman.img.set_y(0)
        time.sleep(1)

    screen.fill((255, 255, 255))
    screen.blit(pacman.img.image(), pacman.img.rect())
    screen.blit(img_monster1.image(), img_monster1.rect())

    pygame.display.flip()   # обновление экрана

pygame.quit()