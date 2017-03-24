import pygame, random, sys
from pygame.locals import *

# WINDOW
WIDTH, HEIGHT = 330, 300
SIZE = WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
FPS = 30

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)

# IMAGES
gridImg = pygame.image.load('res/img/tile_new.png')
bodyImg = pygame.image.load('res/img/body_new.png')
appleImg = pygame.image.load('res/img/apple_new.png')

# SOUNDS
# eat = pygame.mixer.Sound('res/sounds/eat.ogg')

# Snake
class Snake:
    def __init__(self, x, y):
        self.body = []
        self.add_body(x, y)
        self.direction = 'r'
    def reset(self):
        self.body = []
        self.body.append([0, 0])
        self.direction = 'r'
    def add_body(self, x, y):
        self.body.append([x, y])
    def get_pos(self):
        return self.body[0]
    def move_body(self):
        prevx, prevy = self.body[0]   
        for b in self.body:
            px, py = b
            b[0], b[1] = prevx, prevy
            prevx, prevy = px, py
snake = Snake(0, 0)
keys = { pygame.K_RIGHT: 'r', pygame.K_LEFT: 'l', pygame.K_DOWN: 'd', pygame.K_UP: 'u' }
d = snake.direction
timer = 0

# Apple
class Apple:
    def __init__(self):
        self.x, self.y = 0, 0
        self.rand()
    def rand(self):
        while self.get_pos() in snake.body:
            self.x = random.randint(0, WIDTH // 30 - 1)
            self.y = random.randint(0, HEIGHT // 30 - 1)
    def get_pos(self):
        return [self.x, self.y]
apple = Apple()
#Button
class Button:
    def __init__(self, text='button', x=0, y=0, size=40):
        self.textSurface = pygame.font.Font('res/fonts/midnight_snacks.ttf', size).render(text, True, black)
        self.textRect = self.textSurface.get_rect()
        self.textRect.center = x, y
    def pressed(self, x, y):
        if self.textRect.collidepoint(x, y):
            return True
    def changecursor(self, x, y):
        return self.textRect.collidepoint(x, y)
    def draw(self):
        screen.blit(self.textSurface, self.textRect)
#Scores
class Score:
    def __init__(self, filepath):
        self.filepath = filepath
        self.score = 0
    def reset(self):
        self.score = 0
    def clearscores(self):
        filescore = open(self.filepath, 'w')
        filescore.truncate()
        filescore.write(str(0))
        filescore.close()
    def save(self):
        if self.score > self.restore():
            filescore = open(self.filepath, 'w')
            filescore.truncate()
            filescore.write(str(self.score))
            filescore.close()
    def restore(self):
        filescore = open(self.filepath)
        score = filescore.readline()
        filescore.close()
        return int(score)
score = Score('res/scores.txt')

def drawtext(text, x, y, size):
    textSurface = pygame.font.Font('res/fonts/midnight_snacks.ttf', size).render(text, True, black)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    screen.blit(textSurface, textRect)

def reset():
    global d
    snake.reset()
    score.reset()
    d = snake.direction
    apple.rand()
    
def terminate():
    pygame.quit()
    sys.exit()    
    
def update(events):
    global d, timer
    
    for e in events:
        if e.type == KEYDOWN and e.key == K_SPACE:
            apple.rand()
        if e.type == KEYDOWN and e.key in keys:
            d = keys[e.key]
                   
    if d == 'r' and snake.direction == 'l':   snake.direction = 'l'
    elif d == 'l' and snake.direction == 'r': snake.direction = 'r'
    elif d == 'u' and snake.direction == 'd': snake.direction = 'd'
    elif d == 'd' and snake.direction == 'u': snake.direction = 'u'
    else:   snake.direction = d
    
    timer += 4
    
    if timer % 40 == 0:
        if snake.direction == 'r':
            snake.body[0][0] += 1
        elif snake.direction == 'd':
            snake.body[0][1] += 1
        elif snake.direction == 'l':
            snake.body[0][0] -= 1
        elif snake.direction == 'u':
            snake.body[0][1] -= 1
        
        snake.move_body()
        
        timer = 0
    if (snake.body[0] in snake.body[3:] or
        snake.body[0][0] < 0 or
        snake.body[0][0] > (WIDTH - 30)//30 or
        snake.body[0][1] < 0 or
        snake.body[0][1] > (HEIGHT - 30)//30):
        gameover_state()
    
    if apple.get_pos() == snake.get_pos():
        snake.add_body(*snake.body[-1])
        apple.rand()
        score.score += 1
        score.save()
    pygame.display.set_caption('Snake | Scores: %s' % score.score)
    
    
def draw(screen):
    # Draw grid
    for y in range(HEIGHT // 30):
        for x in range(WIDTH // 30):
            screen.blit(gridImg, (1 + x * 30, 1 + y * 30))  
    # Draw snake
    for b in snake.body:
        screen.blit(bodyImg, (b[0] * 30 + 1, b[1] * 30 + 1))
    # Draw apple
    screen.blit(appleImg, (apple.x * 30 + 1, apple.y * 30 + 1))

def gameover_state():
    playagain = Button('PlayAgain', WIDTH//2-50, 250, 25)
    menu = Button('Menu', WIDTH//2+75, 250, 25)
    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if playagain.pressed(*e.pos):
                    reset()
                    done = True
                if menu.pressed(*e.pos):
                    reset()
                    menu_state()
            if e.type == MOUSEMOTION:
                if any([playagain.changecursor(*e.pos), menu.changecursor(*e.pos)]):
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
        screen.fill(white)
        drawtext('GameOver', WIDTH//2, 90, 45)
        drawtext('Your score: %r' % score.score, WIDTH//2, 150, 25)
        playagain.draw()
        menu.draw()
        pygame.display.update()

def play_state():
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    while True:
        if pygame.event.get(QUIT):
            terminate()
        
        if pygame.key.get_pressed()[K_ESCAPE]:
            pygame.display.set_caption('Snake')
            reset()
            return
        
        screen.fill(white)
        
        update(pygame.event.get())
        draw(screen)
        
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)

def scores_state():
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    resetbutton = Button('Reset', WIDTH//2, 250)
    back = Button('back', 40, 25, 20)
    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if resetbutton.pressed(*e.pos):
                    score.clearscores()
                if back.pressed(*e.pos):
                    done = True
            if e.type == MOUSEMOTION:
                if any([resetbutton.changecursor(*e.pos), back.changecursor(*e.pos)]):
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:  
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
        screen.fill(white)
        drawtext('Highscore:', WIDTH // 2, 100, 45)
        drawtext(str(score.restore()), WIDTH // 2, 150, 30)
        resetbutton.draw()
        back.draw()
        pygame.display.update()

def menu_state():
    playbutton = Button('Playgame', WIDTH//2, 120)
    scorebutton = Button('Scores', WIDTH//2, 180)
    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == QUIT:
                terminate()
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if playbutton.pressed(*e.pos):
                    play_state()
                if scorebutton.pressed(*e.pos):
                    scores_state()
            if e.type == MOUSEMOTION:
                if any ([playbutton.changecursor(*e.pos), scorebutton.changecursor(*e.pos)]):
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                else:  
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
        screen.fill(white)
        playbutton.draw()
        scorebutton.draw()
        pygame.display.flip()

def main():
    menu_state()

if __name__ == '__main__':
    main()
