import pygame
import random
import os
xpos = 440
ypos = 140
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (xpos,ypos)


pygame.init()

pygame.display.set_caption("Snek!")
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
win_width = 400
win_height = 400
fps = 12

win = pygame.display.set_mode((win_width,win_height))
background_image = pygame.image.load('background.png').convert()
background_image = pygame.transform.scale(background_image, (win_width,win_height))
clock = pygame.time.Clock()

class Snake:

    def __init__(self, width, height, x, y, vel):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vel = vel
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        snake_sprite = pygame.image.load('snake.png').convert()
        win.blit(snake_sprite, (self.x,self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        
    def get_rect(self):
        return pygame.Rect(self.hitbox)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

class Tail:
    
    def __init__(self, width, height, x, y, tailposition):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.tailposition = tailposition
        self.index = 0
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        snake_sprite = pygame.image.load('snake.png').convert()
        self.x = self.get_x()
        self.y = self.get_y()
        win.blit(snake_sprite, (self.x,self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        
    def get_rect(self):
        return pygame.Rect(self.hitbox)

    def get_x(self):
        self.index = -1*(self.tailposition+1)
        self.x = positionx[self.index]
        return self.x
    def get_y(self):
        self.index = -1*(self.tailposition+1)
        self.y = positiony[self.index]
        return self.y
    
class Treat:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        treat_sprite = pygame.image.load('treat.png').convert()
        win.blit(treat_sprite, (self.x,self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)

    def get_rect(self):

        return pygame.Rect(self.hitbox)


snake = Snake(10, 10, 200, 200, 10)
tailobjectlist = [snake]
positionx = [snake.x]
positiony = [snake.y]
positionoflasttail = []
positionoflasttail = []
score = []
treats=[]
tail = False
numberoftreats = True
moveright = True
moveleft = False
moveup = False
movedown = False
gameover = False

def gameover():
    global gameover
    gameover = True
    snake.vel = 0
    redrawGameWindow()
##    gameFont = pygame.font.SysFont('fixedsys', 60)
##    gameoversurface = gameFont.render('Game Over.', False, (0,0,0))
    #win.blit(gameoversurface,(5,5))

def redrawGameWindow():
    win.blit(background_image, (0,0))
    global gameover
    
    if gameover == True:
        gameFont = pygame.font.SysFont('fixedsys', 60)
        gameoversurface = gameFont.render('Game Over.', False, (255,0,0))
        win.blit(gameoversurface,(100,160))
    
    snake.draw(win)
    treat.draw(win)
    if len(tailobjectlist) > 0:
        for i in tailobjectlist:
            i.draw(win)
        
    pygame.display.update()

run = True
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    while numberoftreats:
        width = 10
        height = 10
        x = random.randint(0, ((win_width-width)//10))*10
        y = random.randint(0, ((win_height-height)//10))*10
        treat = Treat(width, height, x, y)
        treats.append(treat)
        numberoftreats = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake.x > 0:
        moveright = False
        moveleft = True
        moveup = False
        movedown = False
    if keys[pygame.K_RIGHT] and snake.x < win_width-snake.width:
        moveright = True
        moveleft = False
        moveup = False
        movedown = False
    if keys[pygame.K_UP] and snake.y > 0:
        moveright = False
        moveleft = False
        moveup = True
        movedown = False
    if keys[pygame.K_DOWN] and snake.y < win_height-snake.height:
        moveright = False
        moveleft = False
        moveup = False
        movedown = True

    if moveright:
        snake.x += snake.vel
        positionx.append(snake.x)
        positiony.append(snake.y)
    if moveleft:
        snake.x -= snake.vel
        positionx.append(snake.x)
        positiony.append(snake.y)
    if moveup:
        snake.y-=snake.vel
        positionx.append(snake.x)
        positiony.append(snake.y)
    if movedown:
        snake.y += snake.vel
        positionx.append(snake.x)
        positiony.append(snake.y)
        
        
    if snake.get_rect().colliderect(treat.get_rect()):
        treats.clear()
        score.append(1)
        numberoftreats = True
        tailposition = (len(tailobjectlist))
        index = -1*(len(tailobjectlist)+1)            
        if len(tailobjectlist)==0:
            tail= True
            tail = Tail(10, 10, positionx[index], positiony[index], (tailposition))
            tailobjectlist.append(tail)
            tailposition+=1
        else:
            tail = Tail(10, 10, positionx[index], positiony[index], tailposition)
            tailobjectlist.append(tail)
            tailposition+=1

    if (len(tailobjectlist))>0:
        for i in tailobjectlist[1:-1]:
            if snake.get_rect().colliderect(i.get_rect()):
                gameover()
    if snake.x >= win_width or snake.x < 0:
        gameover()
    if snake.y >= win_height or snake.y <0:
        gameover()
        
        
    redrawGameWindow()


pygame.quit()
