import pygame, sys, random

pygame.init()
width, height = 330, 330
display = pygame.display.set_mode((width, height))

class Snake:
    def __init__(self):
        self.body = []
        self.direction = 'r'
        self.keys = { pygame.K_RIGHT: 'r', pygame.K_LEFT: 'l', pygame.K_DOWN: 'd', pygame.K_UP: 'u' }
        self.image = pygame.image.load('res/img/body_new.png').convert()
    def add_body(self, x, y):
        self.body.append([x, y])
    def isDead(self):
        for b in self.body[2:]:
            if b == self.body[0]:
                return True
        if self.body[0][0] < 0 or self.body[0][0] >= 16 or self.body[0][1] < 0 or self.body[0][1] >= 12:
            return True
    def getCoord(self):
        return self.body[0]
    def update(self, events):
        prevx, prevy, px, py = 0, 0, 0, 0
        d = self.direction
        
        key = pygame.key.get_pressed()
        if key in self.keys:
            d = self.keys[key]
                   
        if d == 'r' and self.direction == 'l':   self.direction = 'l'
        elif d == 'l' and self.direction == 'r': self.direction = 'r'
        elif d == 'u' and self.direction == 'd': self.direction = 'd'
        elif d == 'd' and self.direction == 'u': self.direction = 'u'
        else:   self.direction = d
        
        if self.direction == 'r':
            self.body[0][0] += 1
        elif self.direction == 'd':
            self.body[0][1] += 1
        elif self.direction == 'l':
            self.body[0][0] -= 1
        elif self.direction == 'u':
            self.body[0][1] -= 1
    
        prevx, prevy = self.body[0][0], self.body[0][1]    

        for b in self.body:
            px, py = b[0], b[1]
            b[0], b[1] = prevx, prevy
            prevx, prevy = px, py
        
    def draw(self):
        for b in self.body:
            display.blit(self.image, (b[0] * 30 + 1, b[1] * 30 + 1))
        pygame.display.update()


snake = Snake()
#game
gameOver = False
fpsClock = pygame.time.Clock()
timer = 0

#colors
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red   = (255, 0, 0)

font = pygame.font.Font('res/fonts/midnight_snacks.ttf', 40)
#playgame
playgame = font.render('Playgame', True, black)
p_rect = playgame.get_rect()
p_rect.x = (width - playgame.get_width()) // 2
#settings
settings = font.render('Settings', True, black)
s_rect = settings.get_rect()
s_rect.x = (width - settings.get_width()) // 2
#scores
scores = font.render('Scores', True, black)
sc_rect = scores.get_rect()
sc_rect.x = (width - scores.get_width()) // 2  
  
menu = [playgame, settings, scores]
menu_rect = [p_rect, s_rect, sc_rect]
for i in range(3):
    menu_rect[i].y = 80 + i * 50

score = 0

#apple
appleX, appleY = 0, 0

#images
gridImg  = pygame.image.load('res/img/tile_new.png').convert()
appleImg = pygame.image.load('res/img/apple_new.png').convert()

def randCoord():
    global appleX, appleY
    while [appleX, appleY] in snake.body:
        appleX, appleY = random.randint(0, width//30 - 1), random.randint(0, height//30 - 1)

def toCoord(x, y):
    return [x // 30, y // 30]

def reset():
    global score
    snake.body = []
    snake.add_body(0,0)
    randCoord()
    score = 0

def update(events):
    global px, py, prevx, prevy, timer, score
    
    timer += 4

    if timer % 40 == 0:   
        snake.update(events)
        timer = 0
    
    if [appleX, appleY] == snake.getCoord():
        randCoord()
        snake.add_body(prevx, prevy)
        score += 10
        
    if snake.isDead():
        reset()

def makeGrid():
    for y in range(height // 30):
        for x in range(width // 30):
            yield (1 + x * 30, 1 + y * 30)     
            
def drawMenu():
    for i in range(3):
        display.blit(menu[i], menu_rect[i])

def drawGrid():
    for coord in makeGrid():
        display.blit(gridImg, coord)

def draw():
    drawGrid()
    display.blit(appleImg, (appleX * 30 + 1, appleY * 30 + 1))
    snake.draw()

def main():
    global d, direction
    isPlay = False
    reset()
    while not gameOver:
        display.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for mr in menu_rect:
                    if mr.collidepoint(event.pos):
                        isPlay = True
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                isPlay = False
        
        if isPlay:
            update(pygame.event.get())
            draw()
            pygame.display.set_caption('Score: {}'.format(score))
        else:
            reset()
            drawMenu()
            pygame.display.set_caption("Snake")
        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(30)
    
if __name__ == '__main__':
    main()    
