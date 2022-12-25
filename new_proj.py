import pygame
import random
import os
import sys

# Name of User PC
name_of_u = input("Введите имя пользователя: ")
name_of_dir = "C:/Users/" + name_of_u + "/Downloads/data/"
print(name_of_dir)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
infoObject = pygame.display.Info()
pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

pygame.display.flip()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

size = width, height
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = name
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def Play_Game():
    global name_of_dir
    pygame.init()
    pygame.mixer.music.load(name_of_dir + 'Unravel.mp3')
    pygame.mixer.music.play(-1)
    DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    infoObject = pygame.display.Info()
    pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

    green = pygame.image.load(name_of_dir + 'green.png').convert()
    blue = pygame.image.load(name_of_dir + 'blue.png').convert()

    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

    size = width, height
    screen = pygame.display.set_mode(size)

    screen.fill((0, 0, 0))
    pygame.display.flip()
    circles = []

    dog_surf = pygame.image.load(name_of_dir + 'Ghoul.jpg')
    dog_rect = dog_surf.get_rect(
        bottomright=(width, height))
    screen.blit(dog_surf, dog_rect)

    flPause = False
    running = True
    sized_1 = 0
    sized_2 = 1
    fps = 60
    time = 0
    time_cleaner = 0
    clock = pygame.time.Clock()
    radius = 90
    patent_color = False
    v = 1
    radius_grow = False
    pygame.mouse.set_visible(False)

    while running:
        time += clock.tick() / 1000 * v
        time_cleaner += clock.tick() / 1000 * v

        pos = pygame.mouse.get_pos()
        # giving color and shape to the circle
        if not patent_color:
            pygame.draw.circle(screen, (0, 255, 0),
                               pos, 50, 1)
        else:
            pygame.draw.circle(screen, (0, 0, 255),
                               pos, 25, 3)
        pygame.display.update()
        if time >= 0.53:
            dog_surf = pygame.image.load(name_of_dir + 'Ghoul.jpg')
            dog_rect = dog_surf.get_rect(
                bottomright=(width, height))
            screen.blit(dog_surf, dog_rect)

            random_x = random.randint(80, size[0] - 80)
            random_y = random.randint(80, size[1] - 80)
            new_poly = pygame.draw.circle(screen, (225, 100, 190), (random_x, random_y), 70)

            new_circle = pygame.draw.circle(screen, (255, 100, 190), (random_x, random_y), 90, 5)
            circles.append(random_x)
            circles.append(random_y)

            time = 0
            time_cleaner += 1

            radius_grow = True
        if radius_grow:
            new_circle = pygame.draw.circle(screen, (255, 100, 190), (circles[0], circles[1]), radius, 5)
            radius -= 47 / fps
            clock.tick(fps)
            if radius <= 70:
                screen.blit(green, (width / 2, height / 2))
                dog_surf = pygame.image.load(name_of_dir + 'Ghoul.jpg')
                dog_rect = dog_surf.get_rect(
                    bottomright=(width, height))
                screen.blit(dog_surf, dog_rect)
                radius_grow = False
                radius = 90
                circles.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flPause = not flPause
                    if flPause:
                        pygame.mixer.music.pause()
                        v = 0
                    else:
                        pygame.mixer.music.unpause()
                        v = 1
                elif event.key == pygame.K_ESCAPE:
                    Menu()
                elif event.key == pygame.K_z or event.key == pygame.K_x:
                    color = screen.get_at(pygame.mouse.get_pos())
                    patent_color = True
                    if color == (225, 100, 190) or color == (255, 100, 190):
                        if 70 < radius < 80:
                            screen.blit(blue, (circles[0], circles[1]))
                    else:
                        screen.blit(green, (width / 2, height / 2))
                else:
                    patent_color = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                color = screen.get_at(pygame.mouse.get_pos())
                patent_color = True
                if color == (225, 100, 190) or color == (255, 100, 190):
                    if 70 < radius < 80:
                        screen.blit(blue, (circles[0], circles[1]))
                else:
                    screen.blit(green, (width / 2, height / 2))
            else:
                patent_color = False
        pygame.display.flip()
    pygame.quit()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255,  0,  0)
GREEN = (0, 255,  0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)


def button_create(text, rect, inactive_color, active_color, action):

    font = pygame.font.Font(None, 40)

    button_rect = pygame.Rect(rect)

    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)

    return [text, text_rect, button_rect, inactive_color, active_color, action, False]


def button_check(info, event):

    text, text_rect, rect, inactive_color, active_color, action, hover = info

    if event.type == pygame.MOUSEMOTION:
        # hover = True/False
        info[-1] = rect.collidepoint(event.pos)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hover and action:
            action()


def button_draw(screen, info):

    text, text_rect, rect, inactive_color, active_color, action, hover = info

    if hover:
        color = active_color
    else:
        color = inactive_color

    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text_rect)


def on_click_button_1():
    global stage
    stage = 'game'
    Play_Game()

    print('You clicked Button 1')


def on_click_button_2():
    global stage
    stage = 'options'

    print('You clicked Button 2')


def on_click_button_3():
    global stage
    global running

    stage = 'exit'
    running = False
    pygame.quit()
    return


def on_click_button_return():
    global stage
    stage = 'menu'

    print('You clicked Button Return')


def Menu():
    global name_of_dir
    pygame.mouse.set_visible(True)
    pygame.mixer.music.load(name_of_dir + "ost.mp3")
    pygame.mixer.music.play(-1)
    pygame.init()
    screen_rect = screen.get_rect()

    # - objects -

    stage = 'menu'

    button_1 = button_create("GAME", (300, 100, 200, 75), RED, GREEN, on_click_button_1)
    button_3 = button_create("EXIT", (300, 300, 200, 75), RED, GREEN, on_click_button_3)

    # - mainloop -

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if stage == 'menu':
                button_check(button_1, event)

                button_check(button_3, event)
            elif stage == 'game':
                Play_Game()
                break
            elif stage == 'exit':
                on_click_button_3()
                pygame.quit()
                return

    # - draws -

        if stage == 'menu':
            if running:
                width, height = 10, 10
                try:
                    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
                except pygame.error:
                    pass
                new_surf = pygame.image.load(name_of_dir + 'osu_jpg.jpg')
                new_rect = new_surf.get_rect(
                    bottomright=(width, height))
                screen.blit(new_surf, new_rect)
                button_draw(screen, button_1)
                button_draw(screen, button_3)

        pygame.display.update()


try:
    Menu()
except pygame.error:
    pass
