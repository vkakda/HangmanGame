#########################################################
## File Name: hangman.py                               ##
## Description:  Shri ram group of college muzaffarnagar - hangman game project   ##
#########################################################
import pygame
import random

pygame.init()
winWidth = 700
winHeight = 480
win = pygame.display.set_mode((winWidth, winHeight), pygame.RESIZABLE)
#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#
DARK_BG = (58, 12, 163)        # Deep blue-violet background
LIGHT_TEXT = (255, 255, 255)   # Pure white text
ACCENT1 = (255, 0, 110)        # Vibrant pink for buttons
ACCENT2 = (0, 255, 200)        # Bright aqua for guessed letters
ACCENT3 = (255, 221, 51)       # Vivid yellow for win/lose message

BLACK = (20, 20, 20)           # For outlines
WHITE = (255,255,255)
RED = (255, 61, 61)            # Bright red for errors
GREEN = (0, 255, 90)           # Neon green for correct
BLUE = (0, 191, 255)           # Sky blue for accents
LIGHT_BLUE = (0, 255, 255)     # Cyan for highlights

btn_font = pygame.font.SysFont("comicsansms", 24, bold=True)
guess_font = pygame.font.SysFont("comicsansms", 28, bold=True)
lost_font = pygame.font.SysFont('comicsansms', 48, bold=True)
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('hangman0.png'), pygame.image.load('hangman1.png'), pygame.image.load('hangman2.png'), pygame.image.load('hangman3.png'), pygame.image.load('hangman4.png'), pygame.image.load('hangman5.png'), pygame.image.load('hangman6.png')]

limbs = 0


def setup_buttons():
    global buttons
    buttons.clear()
    buttons_per_row = 13
    width = win.get_width()
    height = win.get_height()

    # Calculate max button diameter and spacing to fit all buttons in the width
    min_spacing = 4
    max_button_radius = int(min(width, height) * 0.045)  # Responsive max radius
    # Calculate the maximum possible button diameter and spacing for current width
    max_total_button_width = width * 0.96  # leave some margin
    button_diameter = max_total_button_width / (buttons_per_row + (buttons_per_row - 1) * 0.5)
    button_diameter = min(button_diameter, max_button_radius * 2)
    button_radius = int(button_diameter // 2)
    button_spacing = max(int(button_radius * 0.5), min_spacing)

    # Recalculate row width with these values
    row_width = buttons_per_row * button_diameter + (buttons_per_row - 1) * button_spacing
    start_x = int((width - row_width) // 2 + button_radius)

    # Adjust vertical positions based on height
    button_y1 = int(height * 0.13)
    button_y2 = int(height * 0.27)
    for i in range(26):
        if i < 13:
            y = button_y1
            x = int(start_x + i * (button_diameter + button_spacing))
        else:
            y = button_y2
            x = int(start_x + (i - 13) * (button_diameter + button_spacing))
        buttons.append([ACCENT1, x, y, button_radius, True, 65 + i])
        # buttons.append([color, x_pos, y_pos, radius, visible, char])


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    width = win.get_width()
    height = win.get_height()
    # Create a vertical gradient background for more interactivity
    for y in range(height):
        color = (
            58 + int((255-58) * y / height),
            12 + int((0-12) * y / height),
            163 + int((110-163) * y / height)
        )
        pygame.draw.line(win, color, (0, y), (width, y))
    # Responsive font for keys
    if buttons:
        key_font_size = max(12, int(buttons[0][3] * 1.2))
    else:
        key_font_size = 24
    key_font = pygame.font.SysFont("comicsansms", key_font_size, bold=True)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            hue = i / 26.0
            r = int(255 * abs((hue * 6) % 6 - 3) / 3)
            g = int(255 * abs((hue * 6 + 2) % 6 - 3) / 3)
            b = int(255 * abs((hue * 6 + 4) % 6 - 3) / 3)
            btn_color = (max(100, min(r,255)), max(100, min(g,255)), max(100, min(b,255)))
            # Draw shadow
            pygame.draw.circle(win, (30,30,30), (buttons[i][1]+3, buttons[i][2]+3), buttons[i][3]+3)
            # Draw main button (responsive radius)
            pygame.draw.circle(win, btn_color, (buttons[i][1], buttons[i][2]), buttons[i][3])
            # Draw thick bright outline
            pygame.draw.circle(win, WHITE, (buttons[i][1], buttons[i][2]), buttons[i][3], max(2, buttons[i][3]//7))
            # Draw letter with bold white font and shadow, responsive size
            label = key_font.render(chr(buttons[i][5]), 1, (0,0,0))
            win.blit(label, (buttons[i][1] - (label.get_width() / 2)+2, buttons[i][2] - (label.get_height() / 2)+2))
            label = key_font.render(chr(buttons[i][5]), 1, WHITE)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    # Draw guess dashes/letters in bold, vibrant yellow, responsive font size
    spaced = spacedOut(word, guessed)
    # Responsive font size based on width and height
    dash_font_size = max(18, min(int(height * 0.09), int(width * 0.045)))
    dash_font = pygame.font.SysFont("comicsansms", dash_font_size, bold=True)
    label1 = dash_font.render(spaced, 1, (255, 221, 51))
    rect = label1.get_rect()
    length = rect[2]
    win.blit(label1, (width/2 - length/2, height - int(height * 0.17)))

    # Draw hangman image, scale and center
    pic = hangmanPics[limbs]
    pic_height = int(height * 0.35)
    scale = pic_height / pic.get_height()
    pic_width = int(pic.get_width() * scale)
    pic_scaled = pygame.transform.smoothscale(pic, (pic_width, pic_height))
    win.blit(pic_scaled, (width/2 - pic_width/2 + 20, int(height * 0.31)))
    pygame.display.update()


def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    lostTxt = 'You Lost, press any key to play again...'
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(1000)
    width = win.get_width()
    height = win.get_height()
    # Gradient background for end screen
    for y in range(height):
        color = (
            255 - int((255-58) * y / height),
            int((221-12) * y / height),
            51 + int((163-51) * y / height)
        )
        pygame.draw.line(win, color, (0, y), (width, y))

    if winner == True:
        label = lost_font.render(winTxt, 1, ACCENT3)
    else:
        label = lost_font.render(lostTxt, 1, ACCENT1)

    wordTxt = lost_font.render(word.upper(), 1, LIGHT_TEXT)
    wordWas = lost_font.render('The phrase was: ', 1, LIGHT_TEXT)

    win.blit(wordTxt, (width/2 - wordTxt.get_width()/2, int(height * 0.61)))
    win.blit(wordWas, (width/2 - wordWas.get_width()/2, int(height * 0.51)))
    win.blit(label, (width / 2 - label.get_width() / 2, int(height * 0.29)))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True
    limbs = 0
    guessed = []
    word = randomWord()
    setup_buttons()

#MAINLINE

setup_buttons()
word = randomWord()
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            setup_buttons()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()

# always quit pygame when done!
