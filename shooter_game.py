#Create your own shooter
from pygame import *
from random import randint
mixer.init()
mixer.music.load("space.ogg")

init()
window = display.set_mode((700,500))
display.set_caption("shooter game")
background = transform.scale(image.load("galaxy.jpg"), (700,500))
missed = 0
score = 0

class GameSprite(sprite.Sprite): #Sprite is already a class in python
    def __init__(self, player_x, player_y, player_image, player_speed, sizex, sizey):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (sizex, sizey))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_x, player_y, player_image, player_speed):
        super().__init__(player_x, player_y, player_image, player_speed, 65, 75)
        self.cooldown = 0
        self.firerate = 10
    def move(self):
        keys = key.get_pressed()
        if self.cooldown > 0:
                self.cooldown -= 1
        if keys[K_RIGHT]:
            self.rect.x += 10
        if keys[K_LEFT]:
            self.rect.x -= 10
        if keys[K_SPACE]:
            mixer.music.load("fire.ogg")
            if self.cooldown <= 0:
                bullets.add(Bullet(self.rect.x + 25, self.rect.y-25, "bullet.png", 10, 20, 30))
                self.cooldown = self.firerate
            


class Enemy(GameSprite):
    def __init__(self, player_x, player_y, player_image, player_speed):
        super().__init__(player_x, player_y, player_image, player_speed, 60, 47)
    def update(self):
        global missed,text_lose
        if self.rect.y < 500:
                self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(50,650)
            missed += 1
            text_lose = font1.render("Missed : " +  str(missed), 1, (255,255,255))
    def respawn(self):
        global score , text_score
        self.rect.y += self.speed
        self.rect.y = 0
        self.rect.x = randint(50,650)
        self.rect.y += self.speed
   
        score += 1
        text_score = font1.render("Score : " +  str(score), 1, (255,255,255))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            bullets.remove(self)
    

#text
font.init()
font1 = font.SysFont("Arial", 25)
font2 = font.SysFont("Arial", 100)
text_lose = font1.render(
    "Missed : " +  str(missed), 1, (255,255,255)
)
text_score = font1.render("Score : " +  str(score), 1, (255,255,255))

end_text = font2.render("Game Over", True, (255,0,0))
win_text = font2.render("You Won!", True, (0,255,0))

#"spawning" players

player = Player (330,430,"rocket.png", 2)
ogenemy = Enemy(randint(50,650),randint(-50,0), "ufo.png", randint(1,3))
enemy2 = Enemy(randint(50,650),randint(-50,0), "ufo.png", randint(1,3))
enemy3 = Enemy(randint(50,650),randint(-50,0), "ufo.png", randint(1,3))
enemy4 = Enemy(randint(50,650),randint(-50,0), "ufo.png", randint(1,3))
enemy5 = Enemy(randint(50,650),randint(-50,0), "ufo.png", randint(1,3))

ufos = sprite.Group() #spritegroup
ufos.add(ogenemy, enemy2, enemy3, enemy4, enemy5)

bullets = sprite.Group()


clock = time.Clock()
run = True
FPS = 30
global finish
finish = False

while run:
    for e in event.get(): #event.get gives a list of all event (look at documentation) so it searches through them for pygame.QUIT
        if e.type == QUIT: #if you click "x" then it exits
            run = False #updating window everytime this runs

    if sprite.spritecollideany(player, ufos) != None: #this function allows the game to detect any collison between the groups 
        finish = True
    if finish == False and int(missed) < 3 and int(score) < 11:
        window.blit(background,(0,0))
        player.move()
        ufos.draw(window)
        ufos.update()
        bullets.draw(window)
        bullets.update()
        window.blit(text_lose,(10,10))
        window.blit(text_score, (10,30))
        player.reset()
    elif int(score) == 11:
        window.blit(win_text, (150, 200))
    else:
        window.blit(end_text, (110, 200))
    #collisions
    collided = sprite.groupcollide(ufos, bullets, False, True)
    for e in collided:
        e.respawn()

    display.update()
    clock.tick(FPS)
       
