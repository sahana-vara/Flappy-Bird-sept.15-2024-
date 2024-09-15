import pygame
from pygame.locals import * #*=everything
import random

pygame.init()
clock=pygame.time.Clock()
fps=60 #frame per second - keep updating every 60 milliseconds

screen_width=864
screen_height=936
pygame.display.set_caption("Flappy Bird")
screen=pygame.display.set_mode((screen_width,screen_height))

font=pygame.font.SysFont("Bauhaus 93",60)

white=(255,255,255)

#def game variables
ground_scroll=0
scroll_speed=4
flying=False
game_over=False
pipe_gap=150 #gap in between
pipe_frequency=1500 #milliseconds
last_pipe=pygame.time.get_ticks()-pipe_frequency 
score=0
pass_pipe=False

#loading images
bg=pygame.image.load("assets/bg.png")
ground_img=pygame.image.load("assets/ground.png")
button_img=pygame.image.load("assets/restart button.png")

def draw_text(text,font,color,x,y):
    txt=font.render(text,True,color)
    screen.blit(txt,(x,y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(screen_height/2)
    score=0
    return score #return value stored in variable which = 0 

class Bird(pygame.sprite.Sprite):
    def __init_(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0 #images will keep changing bc theyre in a list
        self.counter=0 #to create animation effect
        for num in range(1,4): #always one more than the amount
            img=pygame.image.load(f"assets/bird{num}.png")
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center = [x,y]
        self.vel=0 #speed of bird
        self.clicked=False #clicked down on screen
    
    def update(self):
        if flying==True:
            #apply gravity
            self.vel+=0.5
            if self.vel >8:
                self.vel=8
            if self.rect.bottom<768: #ground
                self.rect.y += int(self.vel) #fall until it reaches the ground
            
        if game_over==False:
            #for bird to jump
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                self.vel=-10 #make it go up
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False 
            
            #handling the animation
            flap_cooldown=5
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter=0
                self.index += 1
                if self.index >= len(self.images): #if they've gone through all of the three bird images
                    self.index=0
                self.image=self.images[self.index]

            #rotating the bird
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-2)
        else:
            #pointing the bird to the ground
            self.image=pygame.transform.rotate(self.image[self.index],-90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.init #shorter way of doing "super init"
        self.image=pygame.image.load("assets/pipe.png")
        self.rect.self.image.get_rect()

        #if position=1, pipe will come from top, if=-1, pipe comes from bottom
        if position==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-int(pipe_gap/2)]
        elif position==-1:
            self.rect.topleft=[x,y-int(pipe_gap/2)]

    def update(self): #to move the pipe
        self.rect.x-=scroll_speed 
        if self.rect.right < 0: #if the right side of the pipe becomes 0, it disappears
            self.kill()

class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)  #so the top left corner is what the x + y value represent
    
    def draw(self):
        action=False #action=visibility of button
        #get the mouse pos
        pos=pygame.mouse.get_pos()
    
        #to check if mouseover (collidepoint) or clicked (clicking)
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True
        
        #drawing the restart button
        screen.blit(self.image,self.rect.x,self.rect.y)
        return action 
    
pipe_group=pygame.sprite.Group()
bird_group=pygame.sprite.Group()

#object creation
flappy=Bird(100,int(screen_height/2))
bird_group.add(flappy)

#create object for the button class
button=Button(screen_width//2-50,screen_height//2-100,button_img) #//=int value

run=True
while run:
    clock.tick(fps)
    screen.blit(bg,(0,0))

    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

#draw and scrolling the ground
screen.blit(ground_img,(ground_scroll,768))

#checking the score
if len(pipe_group)>0:
    if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left and if bird_group_sprites()[0].rect.right>pipe_group.sprites()[0].rect.right and pass_pipe=False:
        pass_pipe=True
    if pass_pipe==True:
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right:
            score=score+1
            pass_pipe=False
draw_text(str(score),font,white,int(screen.width/2),20)