import random, math, sys, time, pygame
from pygame.locals import *

FPS = 30
SECS = 60

FRAMES = FPS * SECS
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FONT_SIZE = 32
BOXSIZE = 30
GAME_OVER = 'game_over'
GAME_PLAY = 'game_play'
rect_list = []
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
NAVY = (0, 0, 128)
reapersize = 32
reaper = pygame.Rect(WINDOWWIDTH / 2, WINDOWHEIGHT / 2, reapersize, reapersize)

def main():
    global FPSCLOCK, DISPLAYSURF, FRAMES
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    fontObj = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
    game_state = GAME_OVER
    score = 0
    high_score = 0
    

    beep = pygame.mixer.Sound('beeps.wav')
    gameover = pygame.mixer.Sound('gameover.wav')
    pygame.mixer.music.load('reaper.mp3')
    
    
    pygame.display.set_caption('MouseReaper')

    
    
    down_W = False
    down_A = False
    down_S = False
    down_D = False
    
    while True:
        DISPLAYSURF.fill(BLACK)
        start = False
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                start = True
                if event.key == K_w:
                    down_W = True
                if event.key == K_a:
                    down_A = True
                if event.key == K_s:
                    down_S = True
                if event.key == K_d:
                    down_D = True
            if event.type == KEYUP:
                if event.key == K_w:
                    down_W = False
                if event.key == K_a:
                    down_A = False
                if event.key == K_s:
                    down_S = False
                if event.key == K_d:
                    down_D = False

        if game_state == GAME_OVER:
            textSurfaceObjxx = fontObj.render("Press any key to start!", True, WHITE)
            textRectObjxx = textSurfaceObjxx.get_rect()
            textRectObjxx.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(textSurfaceObjxx, textRectObjxx)

            high = "High score: " + str(high_score)
            textSurfaceObjxxx = fontObj.render(high, True, WHITE)
            textRectObjxxx = textSurfaceObjxxx.get_rect()
            textRectObjxxx.center = (WINDOWWIDTH / 2, (WINDOWHEIGHT / 2) - 60)
            DISPLAYSURF.blit(textSurfaceObjxxx, textRectObjxxx)
            
            if start:
                pygame.mixer.music.play(-1, 0)
                pygame.mixer.music.set_volume(0.1)
                game_state = GAME_PLAY
                score = 0
                rect_list.clear()
                spawn_souls(10)
                frames = FPS * SECS
                reaper.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
                
                     
        elif game_state == GAME_PLAY:
            frames -= 1

            
            
            timer = "Time: " + str(frames // FPS)
            textSurfaceObj = fontObj.render(timer, True, WHITE)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.topleft = (0, 0)
            DISPLAYSURF.blit(textSurfaceObj, textRectObj)

            scorex = "Score: " + str(score)
            textSurfaceObjx = fontObj.render(scorex, True, WHITE)
            textRectObjx = textSurfaceObjx.get_rect()
            textRectObjx.topright = (WINDOWWIDTH, 0)
            DISPLAYSURF.blit(textSurfaceObjx, textRectObjx)

            pygame.draw.rect(DISPLAYSURF, NAVY, reaper)
            for soul in rect_list:
                pygame.draw.rect(DISPLAYSURF, GRAY, soul)

            if frames % 30 == 0:
                spawn_soul()
            if frames == 0:
                if score > high_score:
                    high_score = score

                game_state = GAME_OVER
                pygame.mixer.music.stop()
                gameover.play()
                time.sleep(3)
                pygame.event.clear()

            speed = 8
            if down_W:
                reaper.y -= speed
            if down_A:
                reaper.x -= speed
            if down_S:
                reaper.y += speed
            if down_D:
                reaper.x += speed
              
            if reaper.x < 0:
                reaper.x = 0
            if reaper.x > WINDOWWIDTH - reapersize:
                reaper.x = WINDOWWIDTH - reapersize
            if reaper.y < 0:
                reaper.y = 0
            if reaper.y > WINDOWHEIGHT - reapersize:
                reaper.y = WINDOWHEIGHT - reapersize
            
            for rect in rect_list:
                if rect.colliderect(reaper):
                    rect_list.remove(rect)
                    score += 1
                    if len(rect_list) == 0:
                        score += 10
                        spawn_souls(10)
                        beep.play()
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)

  
def spawn_soul():
    spawned = False
    while not spawned:
        x = random.randint(FONT_SIZE, WINDOWWIDTH - BOXSIZE)
        y = random.randint(FONT_SIZE, WINDOWHEIGHT - BOXSIZE)
        current_soul = pygame.Rect(x, y, 30, 30)

        if current_soul.collidelist(rect_list) == -1 and not current_soul.colliderect(reaper):
            rect_list.append(current_soul)
            spawned = True


def spawn_souls(count):
    for x in range(count):
        spawn_soul()


if __name__ == '__main__':
    main()