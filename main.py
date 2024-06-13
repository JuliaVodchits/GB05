import pygame


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



pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode((window_size))
pygame.display.set_caption("Тестовый проект")
icon = pygame.image.load("img/pacman_icon.png")
pygame.display.set_icon(icon)

img_packman = Image("img/pacman_80.png")
img_monster1 = Image("img/monster_red_80.png")

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # if event.type == pygame.MOUSEMOTION:
        #     mouse_x, mouse_y = pygame.mouse.get_pos()
        #     img_packman.__rect.center = mouse_x, mouse_y

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x = img_packman.x() - img_packman.speed
        if x < 0:
            x = 0
        img_packman.set_x(x)

    if keys[pygame.K_RIGHT]:
        x = img_packman.x() + img_packman.speed
        if x > window_size[0] - img_packman.width:
            x = window_size[0] - img_packman.width
        img_packman.set_x(x)

    if keys[pygame.K_UP]:
        y = img_packman.y() - img_packman.speed
        if y < 0:
            y = 0
        img_packman.set_y(y)

    if keys[pygame.K_DOWN]:
        y = img_packman.y() + img_packman.speed
        if y > window_size[1] - img_packman.height:
            y = window_size[1] - img_packman.height
        img_packman.set_y(y)

    img_monster1.set_x(window_size[0] - img_monster1.width)
    img_monster1.set_y(window_size[1] - img_monster1.height)

    if img_packman.rect().colliderect(img_monster1.rect()):


    screen.fill((255, 255, 255))
    screen.blit(img_packman.image(), img_packman.rect())
    screen.blit(img_monster1.image(), img_monster1.rect())

    pygame.display.flip()   # обновление экрана

pygame.quit()