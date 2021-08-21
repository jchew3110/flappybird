import pygame
import time
import os
import random
import neat
import os
pygame.font.init()

WIN_WIDTH = 500 #setting dimensions of game window
WIN_HEIGHT = 800
FLOOR = 730
MAXGENERATIONS = 30
FRAMERATE = 120
GEN = 0
HIGH_SCORE = 0

pygame.display.set_caption("Flappy Bird")

#uploading images

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")), (WIN_WIDTH, WIN_HEIGHT))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 #how much the bird tilts
    ROT_VEL = 20 #how much the bird rotates on each frame
    ANIMATION_TIME = 5 #how fast bird flaps it's wings 

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 #starts out looking flat
        self.tick_count = 0
        self.vel = 0
        self.height = self.y 
        self.img_count = 0 #which image are we currently showing for the bird
        self.img = self.IMGS[0] #references BIRD_IMGS
    
    def jump(self):
        self.vel = -11 #move up
        self.tick_count = 0
        self.height = self.y 
    
    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2 #calculates the velocity bird travels up or down 

        if d >= 16:
            d = 16 
        
        if d < 0:
            d -= 2 #fall at a constant rate
        
        self.y = self.y + d

        #when above y position at point of jump bird tills up, otherwise tilts down

        if d < 0 or self.y < self.height + 50: 
            if self.tilt < self.MAX_ROTATION:
                self.tilt  = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count += 1
        
        if self.img_count <= self.ANIMATION_TIME: 
            self.img = self.IMGS[0] #bird starts with flap up
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1] #wings are level
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2] #flap down
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1] 
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0] 
            self.img_count = 0 #reset counter
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt) #rotates bird image around left corner by default
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center) #changes centre of rotation to bird
        win.blit(rotated_image, new_rect.topleft) 

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 180
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) #flip and store 1st image for pipe
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) #Returns None if bottom pip and bird's pixels don't collide 
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False

#Our base image needs to constantly be moving
class Base: 
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG 

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL #moves images with velocity

        if self.x1 + self.WIDTH < 0: 
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0: #check whether images are off the screen
            self.x2 = self.x1 + self.WIDTH #cycle image back
        
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))    


def draw_window(win, birds, pipes, base, score, gen, high_score): #draws our game
    win.blit(BG_IMG, (0, 0)) #draws background (bg)

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255)) #score
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 50))
    
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255)) #generation
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255)) #alive
    win.blit(text, (10, 50))

    text = STAT_FONT.render("High Score: " + str(high_score),1,(255,255,255)) #alive
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    for bird in birds:
        bird.draw(win) #draws bird on top of bg

    pygame.display.update() #refreshes display

def main(genomes, config): 
    """
    runs the simulation of the current population of
    birds and sets their fitness based on the distance they
    reach in the game.
    """
    global GEN
    global HIGH_SCORE
    GEN += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    birds = []
    ge = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net) 
        birds.append(Bird(230, 350)) 
        g.fitness = 0 
        ge.append(g) 

    base = Base(FLOOR)
    pipes = [Pipe(WIN_WIDTH)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run and len(birds) > 0:
        clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width(): 
            pipe_ind = 1 

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird): #check for collision 
                     ge[x].fitness -= 1
                     birds.pop(x)
                     nets.pop(x)
                     ge.pop(x)
                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()
        
        if add_pipe:
            score += 1 
            if score >= HIGH_SCORE:
                HIGH_SCORE = score
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))
        
        for r in rem:
            pipes.remove(r)
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < - 50: #when we hit the bird
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN, HIGH_SCORE)

def run(config_path): #runs the NEAT algorithm to train a neural network to play flappy bird.
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    p = neat.Population(config)

    p.run(main, MAXGENERATIONS)

    print("The NEAT algorithms high score is: " + str(HIGH_SCORE))
    
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)