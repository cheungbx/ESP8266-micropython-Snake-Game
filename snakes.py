# ----------------------------------------------------------
#  Snake Game 
#  ESP8266 (node MCU D1 mini)  micropython
# by Billy Cheung  2019 08 31
#
# SPI OLED 
# GND
# VCC
# D0/Sck - D5 (=GPIO14=HSCLK)
# D1/SDA - D7 (=GPIO13=HMOSI)
# RES    - D0 (=GPIO16)
# DC     - D4 (=GPIO2)
# CS     - D1 (=GPIO5)
# Speaker
# GPIO15  D8     Speaker
#
#buttons  A0
# A0 VCC-10K0-U-10K-L-10K-R-10K-D-10K-GND 
# GPIO0   D3——   A

import gc
gc.collect()
print (gc.mem_free())
import utime
from utime import sleep_ms, ticks_ms, ticks_us, ticks_diff
from machine import Pin, SPI, PWM, ADC

import ssd1306
from random import getrandbits, seed

# ----------------------------------------------------------
# Global variables
# ----------------------------------------------------------

SCREEN_WIDTH  = 128
SCREEN_HEIGHT = 64
SNAKE_SIZE    = 4
SNAKE_LENGTH  = 4
SNAKE_EXTENT  = 2
COLS          = (SCREEN_WIDTH  - 4) // SNAKE_SIZE
ROWS          = (SCREEN_HEIGHT - 4) // SNAKE_SIZE
OX            = (SCREEN_WIDTH  - COLS * SNAKE_SIZE) // 2
OY            = (SCREEN_HEIGHT - ROWS * SNAKE_SIZE) // 2
COLOR_BG      = 0
COLOR_WALL    = 1
COLOR_SNAKE   = 1
COLOR_APPLE   = 1
COLOR_SCORE   = 1
COLOR_LOST_BG = 1
COLOR_LOST_FG = 0
MODE_START    = 0
MODE_READY    = 1
MODE_PLAY     = 2
MODE_LOST     = 3
MODE_EXIT     = 4


# configure oled display I2C SSD1306
hspi = SPI(1, baudrate=8000000, polarity=0, phase=0)
#DC, RES, CS 
display = ssd1306.SSD1306_SPI(128, 64, hspi, Pin(2), Pin(16), Pin(5)) 


#--------- pin layout
btn_val=[0, 207, 394, 584, 847]

btnUp = 1
btnLeft = 2
btnRight = 3
btnDown = 4
btnA = 12
pinA = Pin(0, Pin.IN, Pin.PULL_UP)
buzzer = Pin(15, Pin.OUT)
adc = ADC(0)

def pressed (btn, wait_release=False) :
  if btn != btnA :
    a0=adc.read()
    if (a0 > btn_val[btn]-20) and (a0 < btn_val[btn]+20):
      while wait_release and  ((a0 < btn_val[btn]-20) or (a0 > btn_val[btn]+20)):
        sleep_ms (5)
      return True   
    
  elif not pinA.value():
    sleep_ms (1)
    if pinA.value():
      return False
    #wait for key release
    while wait_release and not btn.value() :
      sleep_ms (5)
    return True
  return False


tones = {
    'c4': 262,
    'd4': 294,
    'e4': 330,
    'f4': 349,
    'f#4': 370,
    'g4': 392,
    'g#4': 415,
    'a4': 440,
    "a#4": 466,
    'b4': 494,
    'c5': 523,
    'c#5': 554,
    'd5': 587,
    'd#5': 622,
    'e5': 659,
    'f5': 698,
    'f#5': 740,
    'g5': 784,
    'g#5': 831,
    'a5': 880,
    'b5': 988,
    'c6': 1047,
    'c#6': 1109,
    'd6': 1175,
    ' ': 0
}


def playTone(tone, tone_duration, total_duration):
            beeper = PWM(buzzer, freq=tones[tone], duty=512)
            utime.sleep_ms(tone_duration)
            beeper.deinit()
            utime.sleep_ms(int(total_duration * 1000)-tone_duration)
            
# ----------------------------------------------------------
# Game management
# ----------------------------------------------------------

def tick():
    if not game['refresh']:
        clearSnakeTail()
    
    if game['mode'] == MODE_START:
        resetSnake()
        spawnApple()
        game['mode'] = MODE_READY
        game['score'] = 0
        game['time']  = 0
    elif game['mode'] == MODE_READY:
        game['refresh'] = False
 
        handleButtons()
        moveSnake()
        if snakeHasMoved():
            playTone('c5', 100, 0.5)
            game['mode'] = MODE_PLAY
    elif game['mode'] == MODE_PLAY:
        handleButtons()
        moveSnake()
        if game['refresh']:
            game['refresh'] = False
        if didSnakeEatApple():
            playTone('d6', 20, 0.02)
            playTone('c5', 20, 0.02)
            playTone('f4', 20, 0.02)
            game['score'] += 1
            game['refresh'] = True
            extendSnakeTail()
            spawnApple()
        if didSnakeBiteItsTail() or didSnakeHitTheWall():
            playTone('c4', 500, 1)
            game['mode'] = MODE_LOST
            game['refresh'] = True
    elif game['mode'] == MODE_EXIT:
        return
    else:
        handleButtons()

    draw()
    game['time'] += 1

    
def spawnApple():
    apple['x'] = getrandbits (6) %  (COLS - 1)
    apple['y'] = getrandbits (7) % (ROWS - 1)

def handleButtons():
    if game['mode'] == MODE_LOST :
        if pressed(btnA):
            game['mode'] = MODE_START
        elif pressed(btnLeft):
            game['mode'] = MODE_EXIT 
    elif pressed(btnLeft) :
        dirSnake(-1, 0)
    elif pressed(btnRight) :
        dirSnake(1, 0)
    elif pressed(btnUp) :
        dirSnake(0, -1)
    elif pressed(btnDown):
        dirSnake(0, 1)
    


# ----------------------------------------------------------
# Snake management
# ----------------------------------------------------------

def resetSnake():
    x = COLS // 2
    y = ROWS // 2
    snake['x'] = []
    snake['y'] = []
    for _ in range(SNAKE_LENGTH):
        snake['x'].append(x)
        snake['y'].append(y)
    snake['head'] = SNAKE_LENGTH - 1
    snake['len']  = SNAKE_LENGTH
    snake['vx'] = 0
    snake['vy'] = 0

def dirSnake(dx, dy):
    snake['vx'] = dx
    snake['vy'] = dy

def moveSnake():
    h = snake['head']
    x = snake['x'][h]
    y = snake['y'][h]
    h = (h + 1) % snake['len']
    snake['x'][h] = x + snake['vx']
    snake['y'][h] = y + snake['vy']
    snake['head'] = h

def snakeHasMoved():
    return snake['vx'] or snake['vy']

def didSnakeEatApple():
    h = snake['head']
    return snake['x'][h] == apple['x'] and snake['y'][h] == apple['y']

def extendSnakeTail():
    i = snake['head']
    n = snake['len']
    i = (i + 1) % n
    x = snake['x'][i]
    y = snake['y'][i]
    for _ in range(SNAKE_EXTENT):
        snake['x'].insert(i, x)
        snake['y'].insert(i, y)
    snake['len'] += SNAKE_EXTENT

def didSnakeBiteItsTail():
    h = snake['head']
    n = snake['len']
    x = snake['x'][h]
    y = snake['y'][h]
    i = (h + 1) % n
    for _ in range(n-1):
        if snake['x'][i] == x and snake['y'][i] == y:
            return True
        i = (i + 1) % n
    return False

def didSnakeHitTheWall():
    h = snake['head']
    x = snake['x'][h]
    y = snake['y'][h]
    return x < 0 or x == COLS or y < 0 or y == ROWS

# ----------------------------------------------------------
# Graphic display
# ----------------------------------------------------------

def draw():
    if game['mode'] == MODE_LOST:
        drawGameover()
    elif game['refresh']:
        clearScreen()
        drawWalls()
        drawSnake()
    else:
        drawSnakeHead()
    drawScore()
    drawApple()
    display.show()

def clearScreen():
    color = COLOR_LOST_BG if game['mode'] == MODE_LOST else COLOR_BG
    display.fill(color)
def drawGameover():
    display.fill_rect(10,20,100,35,0)
    display.text("GAME OVER",20,20,1)
    display.text("A to Play",20,30,1)    
    display.text("L to Stop",20,40,1)
 
def drawWalls():
    color = COLOR_LOST_FG if game['mode'] == MODE_LOST else COLOR_WALL
    display.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,color)

def drawSnake():
    isTimeToBlink = game['time'] % 4 < 2
    color = COLOR_LOST_FG if game['mode'] == MODE_LOST and isTimeToBlink else COLOR_SNAKE
    n = snake['len']
    for i in range(n):
        drawDot(snake['x'][i], snake['y'][i], color)

def drawSnakeHead():
    h = snake['head']
    drawDot(snake['x'][h], snake['y'][h], COLOR_SNAKE)

def clearSnakeTail():
    h = snake['head']
    n = snake['len']
    t = (h + 1) % n
    drawDot(snake['x'][t], snake['y'][t], COLOR_BG)

def drawScore():
    display.text(str(game['score']),2,2,1)

def drawApple():
    drawDot(apple['x'], apple['y'], COLOR_APPLE)

def drawDot(x, y, color):
    display.fill_rect(OX + x * SNAKE_SIZE, OY + y * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE,color)

def waitForUpdate():
    # wait the amount of them that makes up 30 frame per second
    timer_dif = int(1000/30) - ticks_diff(ticks_ms(), timer)
    if timer_dif > 0:
      sleep_ms(timer_dif)
    return


# ----------------------------------------------------------
# Initialization
# ----------------------------------------------------------

# Seed random numbers
seed(ticks_us())

game = {
    'mode':    MODE_START,
    'score':   0,
    'time':    0,
    'refresh': True
}

snake = {
    'x':    [],
    'y':    [],
    'head': 0,
    'len':  0,
    'vx':   0,
    'vy':   0
}

apple = { 'x': 0, 'y': 0 }

# ----------------------------------------------------------
# Main loop
# ----------------------------------------------------------
while game['mode'] != MODE_EXIT :
  timer = ticks_ms()
  tick()
  waitForUpdate()



