#import keyboard
import random
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("LCD_1.5_Code/RaspberryPi/python")
from lib import LCD_1inch5
from PIL import Image,ImageDraw,ImageFont
from gpiozero import Button
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

LEFT_MEM = 1
RIGHT_MEM = 2
UP_MEM = 3
DOWN_MEM = 4

tick_delay = 0

game_active = False

grey = 0 #(150,150,150)
black = 1 #( 0, 0, 0)
white = 2 #(255, 255, 255)	#LH Z
green = 3 #(0, 255, 0)		#straight
red = 4 #( 255, 0, 0)		#square
blue = 5 #(0, 0, 255)		#T
yellow = 6 #(255, 255, 0)	#RH L
magenta = 7 #(255, 0, 255)	#LH L
cyan = 8 #(0, 255, 255)	#RH Z

#init colors
back_color = "#dcdcdc"
tetris_colors = ("#969696", "#000000", "#ffffff", "#00ff00", "#ff0000", "#0000ff", "#ffff00", "#ff00ff", "#00ffff")

TokenType_Square = 0
TokenType_Straight = 1
TokenType_T = 2
TokenType_RH_L = 3
TokenType_LH_L = 4
TokenType_RH_Z = 5
TokenType_LH_Z =6

score = 0

row0_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row1_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row2_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row3_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row4_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row5_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row6_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row7_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row8_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row9_NewToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)

row0_NewToken = list(row0_NewToken)
row1_NewToken = list(row1_NewToken)
row2_NewToken = list(row2_NewToken)
row3_NewToken = list(row3_NewToken)
row4_NewToken = list(row4_NewToken)
row5_NewToken = list(row5_NewToken)
row6_NewToken = list(row6_NewToken)
row7_NewToken = list(row7_NewToken)
row8_NewToken = list(row8_NewToken)
row9_NewToken = list(row9_NewToken)

row0_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row1_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row2_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row3_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row4_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row5_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row6_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row7_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row8_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row9_CurToken = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)

row0_CurToken = list(row0_CurToken)
row1_CurToken = list(row1_CurToken)
row2_CurToken = list(row2_CurToken)
row3_CurToken = list(row3_CurToken)
row4_CurToken = list(row4_CurToken)
row5_CurToken = list(row5_CurToken)
row6_CurToken = list(row6_CurToken)
row7_CurToken = list(row7_CurToken)
row8_CurToken = list(row8_CurToken)
row9_CurToken = list(row9_CurToken)

row0_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row1_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row2_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row3_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row4_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row5_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row6_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row7_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row8_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)
row9_GridColor = (red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red, red)

row0_GridColor = list(row0_GridColor)
row1_GridColor = list(row1_GridColor)
row2_GridColor = list(row2_GridColor)
row3_GridColor = list(row3_GridColor)
row4_GridColor = list(row4_GridColor)
row5_GridColor = list(row5_GridColor)
row6_GridColor = list(row6_GridColor)
row7_GridColor = list(row7_GridColor)
row8_GridColor = list(row8_GridColor)
row9_GridColor = list(row9_GridColor)

NewTokenColor = (row0_NewToken, row1_NewToken, row2_NewToken, row3_NewToken, row4_NewToken, row5_NewToken, row6_NewToken, row7_NewToken, row8_NewToken, row9_NewToken)
CurTokenColor = (row0_CurToken, row1_CurToken, row2_CurToken, row3_CurToken, row4_CurToken, row5_CurToken, row6_CurToken, row7_CurToken, row8_CurToken, row9_CurToken)
GridColor = (row0_GridColor, row1_GridColor, row2_GridColor, row3_GridColor, row4_GridColor, row5_GridColor, row6_GridColor, row7_GridColor, row8_GridColor, row9_GridColor)

NewTokenColor = list(NewTokenColor)
CurTokenColor = list(CurTokenColor)
GridColor = list(GridColor)

#return current time in milli-seconds
def time_ms():
    return int(time.time() * 1000)

#draw grid and tokens
def draw_grid() :
    global score
    #init
    xOrigin = 60.0
    yOrigin = 30.0
    pitch = 12.0
    # Create blank image for drawing.
    logging.info("create image1 object:")
    image1 = Image.new("RGB", (disp.width,disp.height ), "LIGHTGREY")
    logging.info("create draw object:")
    draw = ImageDraw.Draw(image1)
    #draw score
    Font1 = ImageFont.truetype("LCD_1.5_Code/RaspberryPi/python/Font/Font02.ttf",24)
    draw.text((85, 2), 'Score: '  + str(score), fill = "BLACK", font=Font1)
    #draw vertical lines
    y1 = yOrigin
    y2 = yOrigin + 20 * pitch
    for i in range(11):
        x1 = xOrigin + i * pitch
        x2 = x1
        draw.line([(x1, y1),(x2, y2)], fill = "BLACK",width = 1)
    #draw horizontal lines
    x1 = xOrigin
    x2 = xOrigin + 10 * pitch
    for i in range(21):
        y1 = yOrigin + i * pitch
        y2 = y1
        draw.line([(x1, y1),(x2, y2)], fill = "BLACK",width = 1)
    #draw squares
    for i in range(10):
        for j in range(20):
            x1 = xOrigin + 1 + (i * pitch) #left
            y1 = yOrigin + 1 + (j * pitch) #top
            if CurTokenColor[i][j] != grey :
                #draw current token
                draw.rectangle([(x1, y1),(x1 + pitch - 2, y1 + pitch - 2)],fill = tetris_colors[CurTokenColor[i][j]])
            else :
                #draw existing grid
                draw.rectangle([(x1, y1),(x1 + pitch - 2, y1 + pitch - 2)],fill = tetris_colors[GridColor[i][j]])
    #update screen
    logging.info("display image1:")
    image1=image1.rotate(0)
    disp.ShowImage(image1)

#handle timer event
def TokenTmr() :
    #drop current token one row
    if CurTokenExist() :
        for i in range(10) :
            #top row is empty
            NewTokenColor[i][0] = grey;
            #NewToken will be one row lower than CurToken
            for j in range(19) :
                NewTokenColor[i][j+1] = CurTokenColor[i][j];
    #create new token
    elif InitToken(RandomToken()) == False :
            #if no room for new token then game is over
            return False
    #evaluate new token for collision with previous tokens added to grid
    if CheckNewTokenCollision() :
        #no collision found, set cur token = new token
        UpdateCurToken()
        #if current token is down, add current token to grid
        if CheckCurTokenDown() == False :
            AddCurTokenToGrid()
        #return succes
        return True
    else :
        if CurTokenExist() :
            AddCurTokenToGrid()
            #return success
            return True
        else :
            #no room to add new token, game is over
            return False

#handle left user input
def TokenLeft() :
    #if cur token does not exist then exit
    if CurTokenExists() == False : return False
    #confirm token is not already at the left extent
    for j in range(20) :
        if CurTokenColor[0][j] != grey :
            #return failure
            return False;
    #shift token left
    for i in range(9) :
        for j in range(20) :
            NewTokenColor[i][j] = CurTokenColor[i+1][j]
    #check for new toke collision with tokens previously added to grid
    if CheckNewTokenCollision() :
        #no collision detected, update cur token = new token
        UpdateCurToken()
        #return success
        return True
    else :
        #collision detected, return failure
        return False

def TokenRight() :
    #if cur token does not exist then exit
    if CurTokenExists() == False : return False
    #confirm token is not already at the right extent
    for j in range(20) :
        if CurTokenColor[9][j] != grey :
            #return failure
            return False
    #shift token right
    for i in range(9) :
        for j in range(20) :
            NewTokenColor[i + 1][j] = CurTokenColor[i][j]
    #check for new toke collision with tokens previously added to grid
    if CheckNewTokenCollision() :
        #no collision detected, update cur token = new token
        UpdateCurToken()
        #return success
        return True
    else :
        #collision detected, return failure
        return False

def TokenRotate() :
    #if cur token does not exist then exit
    if CurTokenExists() == False : return False
    #find extents
    iTop = 99
    iLeft = 99
    iBottom = -1
    iRight = -1
    for i in range(10) :
        for j in range(20) :
            if CurTokenColor[i][j] != grey :
                if j < iTop : iTop = j
                if j > iBottom : iBottom = j
                if i < iLeft : iLeft = i
                if i > iRight : iRight = i
    iWidth = iRight - iLeft
    iHeight = iBottom - iTop
    #determine if there's room to rotate, return failure if there is not room
    if (iTop - iWidth + 1) < 0 : return False
    if (iLeft + iHeight) > 9 : return False
    #rotate token
    for i in range(iWidth + 1) :
        for j in range(iHeight + 1) :
            NewTokenColor[iLeft + j][iTop - i + 1] = CurTokenColor[iLeft + i][iTop + j]
    #check for collision
    if CheckNewTokenCollision() :
        UpdateCurToken()
        #if current token is down, add current token to grid
        if CheckCurTokenDown() == False : AddCurTokenToGrid()
        #return success
        return True
    else :
        #return failure
        return False

def TokenDown() :
    #if cur token does not exist then exit
    if CurTokenExists() == False : return False
    #iterate until new token reached down extent
    while True :
        #shift token down
        for i in range(10) :
            for j in range(19) :
                NewTokenColor[i][j + 1] = CurTokenColor[i][j]
        #check for new toke collision with tokens previously added to grid
        if CheckNewTokenCollision() :
            #no collision detected, update cur token = new token
            UpdateCurToken()
            #if current token is down, add current token to grid
            if CheckCurTokenDown() == False :
                AddCurTokenToGrid()
                #return success
                return True
        else :
            AddCurTokenToGrid()
            #return success
            return True

#determine if current token exists
def CurTokenExist() :
    #return True if current token found
    for i in range(10) :
        for j in range(20) :
            if CurTokenColor[i][j] != grey : return True
    #return False if no current token found
    return False

#return random value between 0 and 6
def RandomToken() :
    return random.randint(0,7)

def InitToken(arg) :
    #clear new token grid
    for i in range(10) :
        for j in range(20) :
            NewTokenColor[i][j] = grey
    #add token arg to new token grid
    if arg == TokenType_Square :
        NewTokenColor[4][0] = red
        NewTokenColor[5][0] = red
        NewTokenColor[4][1] = red
        NewTokenColor[5][1] = red
    elif arg == TokenType_Straight :
        NewTokenColor[4][0] = green
        NewTokenColor[4][1] = green
        NewTokenColor[4][2] = green
        NewTokenColor[4][3] = green
    elif arg == TokenType_T:
        NewTokenColor[4][0] = blue
        NewTokenColor[5][0] = blue
        NewTokenColor[6][0] = blue
        NewTokenColor[5][1] = blue
    elif arg == TokenType_RH_L:
        NewTokenColor[4][0] = yellow
        NewTokenColor[5][0] = yellow
        NewTokenColor[6][0] = yellow
        NewTokenColor[4][1] = yellow
    elif arg == TokenType_LH_L:
        NewTokenColor[4][0] = magenta
        NewTokenColor[5][0] = magenta
        NewTokenColor[6][0] = magenta
        NewTokenColor[6][1] = magenta
    elif arg == TokenType_RH_Z:
        NewTokenColor[4][0] = cyan
        NewTokenColor[5][0] = cyan
        NewTokenColor[5][1] = cyan
        NewTokenColor[6][1] = cyan
    elif arg == TokenType_LH_Z:
        NewTokenColor[4][1] = white
        NewTokenColor[5][1] = white
        NewTokenColor[5][0] = white
        NewTokenColor[6][0] = white
    if CheckNewTokenCollision() :
        #no collision detected, return success
        return True
    else :
        #collision detected, return failure
        return False

def CheckNewTokenCollision() :
    #evaluate new token and make current token = new token
    for i in range(10) :
        for j in range(20) :
            #if collision found, return False
            if (NewTokenColor[i][j] != grey) and (GridColor[i][j] != grey) :
                return False
    #no collision found, return True
    return True

def CheckCurTokenDown() :
    #evaluate new token and make current token = new token
    for i in range(10) :
        #if new token at down extent, return False
        if (CurTokenColor[i][19] != grey) : return False
    #new token not at down extent, return True
    return True

def CheckNewTokenDown() :
    #evaluate new token and make current token = new token
    for i in range(10) :
        #if new token at down extent, return False
        if NewTokenColor[i][19] != grey : return False
    #new token not at down extent, return True
    return True

#set current token = new token, clear new token
def UpdateCurToken() :
    for i in range(10) :
        for j in range(20) :
            CurTokenColor[i][j] = NewTokenColor[i][j]
            NewTokenColor[i][j] = grey
    return True

#add current token to grid, clear current and new tokens
#check grid for complete rows and remove them if found
def AddCurTokenToGrid() :
    global score
    global tick_delay
    #add current token to grid and clear new and current tokens
    for i in range(10) :
        for j in range(20) :
            if(CurTokenColor[i][j] != grey) : GridColor[i][j] = CurTokenColor[i][j]
            CurTokenColor[i][j] = grey
            NewTokenColor[i][j] = grey
    #check for complete rows and remove them if found
    for j in range(20) :
        #check row
        iRowFound = j
        for i in range(10) :
            if GridColor[i][j] == grey :
                iRowFound = -1
                break
        #remove row if found
        if iRowFound >= 0 :
            #increment score
            score += 1
            #adjust delay
            tick_delay = int(float(tick_delay) * 0.95)
            #shift rows down, overwriting row found
            for n in range(iRowFound, 0, -1) :
                for m in range(10) : GridColor[m][n] = GridColor[m][n-1]
            #set top row to nothing
            for m in range(10) : GridColor[m][0] = grey
    #return success
    return True

def CurTokenExists() :
    for i in range(10) :
        for j in range(20) :
            if CurTokenColor[i][j] != grey :
                #return success
                return True
    #return failure
    return False

def NewGame() :
    global score
    global score_mem
    global last_update
    global key_mem
    global last_keypress
    global last_keypress_delay
    global tick_delay
    #init score
    logging.info("NewGame():")
    score = 0
    score_mem=0
    #init grid and tokens
    for i in range(10) :
        for j in range(20) :
            GridColor[i][j] = grey
            CurTokenColor[i][j] = grey
            NewTokenColor[i][j] = grey
    #update screen
    draw_grid()
    #init clock
    tick_delay = 500
    last_update = time_ms()
    last_keypress = time_ms()
    last_keypress_delay = 500
    key_mem = 0

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0

btnStart = Button(23)
btnLeft = Button(19)
btnUp = Button(6)
btnRight = Button(13)
btnDown = Button(26)
buzTone = TonalBuzzer(12)

logging.basicConfig(level=logging.DEBUG)

try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch5.LCD_1inch5(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    logging.info("create disp object:")
    disp = LCD_1inch5.LCD_1inch5()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #init game
    NewGame()
    #game loop
    while 1:
	#left
        #if (btnLeft.is_pressed  or keyboard.is_pressed('left')) and game_active :
        if btnLeft.is_pressed and game_active :
            if (key_mem != LEFT_MEM) or (time_ms() > (last_keypress + last_keypress_delay)) :
                TokenLeft()
                #update surface
                draw_grid()
                last_keypress = time_ms()
                if (key_mem != LEFT_MEM) :
                    last_keypress_delay = 400
                    key_mem = LEFT_MEM
                else :
                    last_keypress_delay = 10
	#right
        #if (btnRight.is_pressed  or keyboard.is_pressed('right')) and game_active :
        if btnRight.is_pressed and game_active :
            if (key_mem != RIGHT_MEM) or (time_ms() > (last_keypress + last_keypress_delay)) :
                TokenRight()
                #update surface
                draw_grid()
                last_keypress = time_ms()
                if (key_mem != RIGHT_MEM) :
                    last_keypress_delay = 400
                    key_mem = RIGHT_MEM
                else :
                    last_keypress_delay = 10
	#up (rotate)
        #if (btnUp.is_pressed  or keyboard.is_pressed('up')) and game_active :
        if btnUp.is_pressed and game_active :
            if (key_mem != UP_MEM) :
                TokenRotate()
                #update surface
                draw_grid()
                last_keypress = time_ms()
                key_mem = UP_MEM
	#down
        #if (btnDown.is_pressed  or keyboard.is_pressed('down')) and game_active :
        if btnDown.is_pressed and game_active :
            if (key_mem != DOWN_MEM) or (time_ms() > (last_keypress + last_keypress_delay)) :
                TokenDown()
                #update surface
                draw_grid()
                last_keypress = time_ms()
                if (key_mem != DOWN_MEM) :
                    last_keypress_delay = 400
                    key_mem = DOWN_MEM
                else :
                    last_keypress_delay = 10
	#start
        #if (btnStart.is_pressed  or keyboard.is_pressed('enter')) :
        if btnStart.is_pressed :
            #init game
            NewGame()
            game_active = True
        #if not(btnLeft.is_pressed or btnRight.is_pressed or btnUp.is_pressed or btnDown.is_pressed or keyboard.is_pressed('left') or keyboard.is_pressed('right') or keyboard.is_pressed('up') or keyboard.is_pressed('down')) :
        if not(btnLeft.is_pressed or btnRight.is_pressed or btnUp.is_pressed or btnDown.is_pressed) :
            key_mem = 0
        if game_active :
            #handle timed event
            if time_ms() > (last_update + tick_delay) :
                #update surface
                buzTone.play("C4")
                game_active = TokenTmr()
                time.sleep(0.05)
                buzTone.stop()
                #update screen
                if game_active :
                    draw_grid()
                    last_update = time_ms()
            #handle score change (complete rows found)
            if score != score_mem :
                score_mem = score

except IOError as e:
    logging.info(e)
