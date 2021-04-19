#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os
import blocks

MOVE_SPEED = 6
WIDTH = 32
HEIGHT = 34
COLOR =  "#888888"
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.1 # скорость смены кадров
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами
global score, dies
score = 0
dies = 0

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = 75 # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = 55
        self.yvel = 0 # скорость вертикального перемещения
        self.onGround = False # На земле ли я?
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR))
        self.image = image.load('%s/ball/00.png' % ICON_DIR)
        self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект
        self.image.set_colorkey(Color(COLOR)) # делаем фон прозрачным
        self.running = False

    def score_up(self):
        global score
        score += 100
    def score_end(self):
        return score
        
    def ending(self):
        self.running =  True
    def end(self):
        if self.running:
            return False
        else:
            return True
    
    def die(self):
        global dies
        time.wait(50)
        self.teleporting(self.startX, self.startY)
        dies += 1
    def deaths(self):
        return dies
    
    def check(self):
        self.startX = 1760
        self.startY = 128
            
    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def update(self, left, right, up, platforms):
        
        if up:
            if self.onGround: # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
                       
        if left:
            self.xvel = -MOVE_SPEED # Лево = x- n
 
        if right:
            self.xvel = MOVE_SPEED # Право = x + n
         
        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0
            
        if not self.onGround:
            self.yvel +=  GRAVITY
            
        self.onGround = False; # Мы не знаем, когда мы на земле((   
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)
   
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p): # если есть пересечение платформы с игроком
                if isinstance(p, blocks.BlockDie): # если пересакаемый блок - blocks.BlockDie
                    self.die()# умираем
                elif isinstance(p, blocks.Check): # если пересакаемый блок - blocks.Check
                    self.check()
                elif isinstance(p, blocks.Ring):
                    self.score_up()
                elif isinstance(p, blocks.End):
                    self.ending()
                    
                else:
                    if xvel > 0:                      # если движется вправо
                        self.rect.right = p.rect.left # то не движется вправо

                    if xvel < 0:                      # если движется влево
                        self.rect.left = p.rect.right # то не движется влево

                    if yvel > 0:                      # если падает вниз
                        self.rect.bottom = p.rect.top # то не падает вниз
                        self.onGround = True          # и становится на что-то твердое
                        self.yvel = 0                 # и энергия падения пропадает

                    if yvel < 0:                      # если движется вверх
                        self.rect.top = p.rect.bottom # то не движется вверх
                        self.yvel = 0                 # и энергия прыжка пропадает
                
