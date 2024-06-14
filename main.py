import pygame
import time

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
        self.speed_x = self.img.width
        self.speed_y = self.img.height

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

    def screen_blit(self, img, rect):
        self.screen.blit(img, rect)

    def warning_msg(self, text, timer):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render(text, True, (255, 255, 255))
        self.screen.blit(text, (self.__window_size[0] // 2 - text.get_width() // 2, \
            self.__window_size[1] // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(timer)


pygame.init()

pacman = Pacman()
display = Display()

img_monster1 = Image("img/monster_red_80.png")

clock = pygame.time.Clock()
fps = 10


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

    img_monster1.set_x(100)
    img_monster1.set_y(100)
    # img_monster1.set_x(display.weight() - img_monster1.width)
    # img_monster1.set_y(display.height() - img_monster1.height)

    if pacman.img.rect().colliderect(img_monster1.rect()):
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
    display.screen_blit(pacman.img.image(), pacman.img.rect())
    display.screen_blit(img_monster1.image(), img_monster1.rect())

    pygame.display.flip()   # обновление экрана
    clock.tick(fps)

pygame.quit()