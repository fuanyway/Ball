#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import *
from player import *
from blocks import *
from levels import *

#Объявляем переменные
WIN_WIDTH = 500 #Ширина создаваемого окна
WIN_HEIGHT = 256 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#7CC8FF"

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
        
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)        

def gen_lvl(level):
    x=y=0 # координаты
    for row in level: # вся строка
        for col in row: # каждый символ
            if col == "-":
                pf = Platform(x,y)
                entities.add(pf)
                platforms.append(pf)

            if col == "*":
                bd = BlockDie(x,y)
                entities.add(bd)
                platforms.append(bd)
    
            if col == "^":
                ch = Check(x,y)
                entities.add(ch)
                platforms.append(ch)
                
            if col == "$":
                end = End(x,y)
                entities.add(end)
                platforms.append(end)
    
            if col == "+":
                r = Ring(x,y)
                entities.add(r)
                platforms.append(r)
                
            x += PLATFORM_WIDTH #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0                   #на каждой новой строчке начинаем с нуля
#def generate_nev_level():
def main():
    pygame.init() # Инициация PyGame, обязательная строчка 
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    pygame.display.set_caption("Bounce Ball") # Пишем в шапку
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом
    
    hero = Player(75,55) # создаем героя по (x,y) координатам
    
    left = right = False # по умолчанию - стоим
    up = False
    numb = 0
    running = True

    global entities, platforms
    entities = pygame.sprite.Group() # Все объекты
    platforms = [] # то, во что мы будем врезаться или опираться
    
    entities.add(hero)
           
    level = get_level(numb)

    timer = pygame.time.Clock()

    gen_lvl(level)
    
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT   # высоту
    
    camera = Camera(camera_configure, total_level_width, total_level_height)
    
    while running: # Основной цикл программы
        timer.tick(60)
        for e in pygame.event.get(): # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
                
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        screen.blit(bg, (0,0))      # Каждую итерацию необходимо всё перерисовывать 

        Text = 'Score: ' + str(hero.score_end())
        (x,y,fontSize) = (10,40,52) 
        myFont = pygame.font.SysFont("None", fontSize) 
        fontColor = (255,255,255) 
        fontImage = myFont.render(Text, 0, (fontColor))
        if hero.score_up():
            screen.blit(fontImage, camera.apply(e))
            gen_lvl(level)
            
        camera.update(hero) # центризируем камеру относительно персонажа
        hero.update(left, right, up,platforms) # передвижение
        #entities.draw(screen) # отображение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        numb += 1
        running = hero.end()

        if not running:
            Text = 'LEVEL COMPLETED'
            (x,y,fontSize) = (980,64,64) 
            myFont = pygame.font.SysFont("None", fontSize) 
            fontColor = (255, 215, 0) 
            fontImage = myFont.render(Text, 1, (fontColor))
            screen.blit(fontImage, camera.apply(e))
        
        pygame.display.update()     # обновление и вывод всех изменений на экран
        

if __name__ == "__main__":
    main()
