#########################################################
## File Name: hangman.py                               ##
## Name - Vishal                                       ##
## Description: Shri Ram Group of College Muzaffarnagar##
##               - Hangman Game Project                ##
#########################################################

import pygame
import random
import sys

pygame.init()

# Window setup
winWidth, winHeight = 700, 480
win = pygame.display.set_mode((winWidth, winHeight), pygame.RESIZABLE)
pygame.display.set_caption("Hangman Game - Shri Ram College")

# Colors
DARK_BG = (58, 12, 163)
LIGHT_TEXT = (255, 255, 255)
ACCENT1 = (255, 0, 110)
ACCENT2 = (0, 255, 200)
ACCENT3 = (255, 221, 51)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (255, 61, 61)
GREEN = (0, 255, 90)
BLUE = (0, 191, 255)
LIGHT_BLUE = (0, 255, 255)

# Fonts (initialized once here, scaled in redraw_game_window if needed)
btn_font = pygame.font.SysFont("comicsansms", 24, bold=True)
guess_font = pygame.font.SysFont("comicsansms", 28, bold=True)
lost_font = pygame.font.SysFont('comicsansms', 48, bold=True)
score_font = pygame.font.SysFont("comicsansms", 26, bold=True)  # Added for score display

# Game Variables
word = ''
buttons = []
guessed = []
limbs = 0
max_limbs = 6  # max wrong guesses allowed
score = 0  # Added: Track number of wins

# Load Hangman Images
hangmanPics = [pygame.image.load(f'hangman{i}.png') for i in range(max_limbs + 1)]


def setup_buttons():
    global buttons
    buttons.clear()

    width = win.get_width()
    height = win.get_height()

    total_letters = 26

    min_button_radius = max(12, int(width * 0.015))
    max_button_radius = min(35, int(width * 0.035))

    margin_x = int(width * 0.03)

    for buttons_per_row in range(13, 5, -1):
        factor = buttons_per_row + (buttons_per_row - 1) * 0.5
        max_diameter = (width - 2 * margin_x) / factor

        candidate_radius = max(min_button_radius, min(max_button_radius, max_diameter / 2))
        if candidate_radius <= max_button_radius:
            button_radius = int(candidate_radius)
            break
    else:
        buttons_per_row = 6
        button_radius = min_button_radius

    button_diameter = button_radius * 2
    button_spacing = int(button_radius * 0.5)
    total_width = buttons_per_row * button_diameter + (buttons_per_row - 1) * button_spacing
    start_x = int((width - total_width) / 2 + button_radius)

    rows = (total_letters + buttons_per_row - 1) // buttons_per_row
    vertical_spacing = int(button_radius * 2.2)
    start_y = int(height * 0.13)

    letter_index = 0
    for row in range(rows):
        y = start_y + row * vertical_spacing
        for col in range(buttons_per_row):
            if letter_index >= total_letters:
                break
            x = start_x + col * (button_diameter + button_spacing)
            buttons.append([ACCENT1, int(x), int(y), button_radius, True, 65 + letter_index])
            letter_index += 1


def redraw_game_window():
    """
    Redraw the entire game window every frame.
    """
    global guessed, hangmanPics, limbs, score

    width = win.get_width()
    height = win.get_height()

    # Draw gradient background
    for y in range(height):
        color = (
            58 + int((255 - 58) * y / height),
            12 + int((0 - 12) * y / height),
            163 + int((110 - 163) * y / height)
        )
        pygame.draw.line(win, color, (0, y), (width, y))

    key_font_size = max(14, int(buttons[0][3] * 1.2)) if buttons else 24
    key_font = pygame.font.SysFont("comicsansms", key_font_size, bold=True)

    # Draw buttons
    for i, btn in enumerate(buttons):
        color, x, y, radius, visible, ascii_code = btn
        if visible:
            hue = i / 26.0
            r = int(255 * abs((hue * 6) % 6 - 3) / 3)
            g = int(255 * abs((hue * 6 + 2) % 6 - 3) / 3)
            b = int(255 * abs((hue * 6 + 4) % 6 - 3) / 3)
            btn_color = (max(100, min(r, 255)), max(100, min(g, 255)), max(100, min(b, 255)))

            pygame.draw.circle(win, BLACK, (x, y), radius + 4)
            pygame.draw.circle(win, btn_color, (x, y), radius)
            pygame.draw.circle(win, WHITE, (x, y), radius, max(2, radius // 6))

            letter = chr(ascii_code)
            label_shadow = key_font.render(letter, True, BLACK)
            label = key_font.render(letter, True, WHITE)
            win.blit(label_shadow, (x - label.get_width() // 2 + 1, y - label.get_height() // 2 + 1))
            win.blit(label, (x - label.get_width() // 2, y - label.get_height() // 2))

    # Draw the guessed word with spaces and underscores
    spaced = spacedOut(word, guessed)
    dash_font_size = max(18, min(int(height * 0.09), int(width * 0.045)))
    dash_font = pygame.font.SysFont("comicsansms", dash_font_size, bold=True)
    label1 = dash_font.render(spaced, True, ACCENT3)
    win.blit(label1, (width / 2 - label1.get_width() / 2, height - int(height * 0.17)))

    # Draw hangman image
    pic = hangmanPics[limbs]
    pic_height = int(height * 0.35)
    scale = pic_height / pic.get_height()
    pic_width = int(pic.get_width() * scale)
    pic_scaled = pygame.transform.smoothscale(pic, (pic_width, pic_height))
    win.blit(pic_scaled, (width / 2 - pic_width / 2 + 20, int(height * 0.31)))

    # --- Modified: Draw Scoreboard in top-right corner ---
    # Responsive score display (shrink mode)
    score_text = f"Score: {score}"
    # Shrink font size if window is small
    min_font_size = 14
    max_font_size = 26
    font_size = max(min_font_size, min(max_font_size, int(width * 0.025)))
    score_font_responsive = pygame.font.SysFont("comicsansms", font_size, bold=True)
    score_label = score_font_responsive.render(score_text, True, ACCENT2)
    padding = max(8, int(width * 0.012))
    win.blit(score_label, (width - score_label.get_width() - padding, padding))

    pygame.display.update()


def spacedOut(word, guessed=[]):
    """
    Return a string with guessed letters shown and unknown letters as underscores,
    with spaces between letters for readability.
    """
    return ''.join(
        x.upper() + ' ' if x.upper() in guessed else '_ ' if x != ' ' else '  '
        for x in word
    )


def buttonHit(x, y):
    """
    Check if the mouse (x,y) is over a visible button.
    If yes, return the letter and mark the button as clicked (invisible).
    """
    for i, btn in enumerate(buttons):
        bx, by, br = btn[1], btn[2], btn[3]
        if btn[4] and (x - bx) ** 2 + (y - by) ** 2 < br ** 2:
            buttons[i][4] = False  # Hide button
            return chr(btn[5])
    return None


def end(winner=False):
    """
    Show end screen and wait for user to choose to play again or quit.
    """
    global word, score
    redraw_game_window()
    pygame.time.delay(1000)

    width = win.get_width()
    height = win.get_height()

    # Draw gradient background with different colors on end screen
    for y in range(height):
        color = (
            255 - int((255 - 58) * y / height),
            int((221 - 12) * y / height),
            51 + int((163 - 51) * y / height)
        )
        pygame.draw.line(win, color, (0, y), (width, y))

    # Update score if won
    if winner:
        score += 1

    result_text = "WINNER!" if winner else "You Lost!"
    result_color = GREEN if winner else RED

    label = lost_font.render(result_text, True, result_color)
    wordTxt = lost_font.render(word.upper(), True, LIGHT_TEXT)
    wordWas = lost_font.render('The phrase was:', True, LIGHT_TEXT)
    prompt = guess_font.render("Play Again? (Y/N)", True, WHITE)

    win.blit(label, (width / 2 - label.get_width() / 2, int(height * 0.29)))
    win.blit(wordWas, (width / 2 - wordWas.get_width() / 2, int(height * 0.51)))
    win.blit(wordTxt, (width / 2 - wordTxt.get_width() / 2, int(height * 0.61)))
    win.blit(prompt, (width / 2 - prompt.get_width() / 2, int(height * 0.75)))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Play again
                    waiting = False
                    reset_game()
                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:  # Quit
                    pygame.quit()
                    sys.exit()


def reset_game():
    """
    Reset game variables and start a new round.
    """
    global limbs, guessed, word
    limbs = 0
    guessed = []
    word = random.choice(words).upper()
    setup_buttons()
    redraw_game_window()


# Load words from 'word.txt' file
with open("words.txt", "r", encoding="utf-8") as f:
    words = [line.strip().upper() for line in f if line.strip()]


def main():
    global word

    word = random.choice(words).upper()
    setup_buttons()
    redraw_game_window()

    running = True
    global limbs, guessed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                setup_buttons()
                redraw_game_window()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                letter = buttonHit(x, y)
                if letter and letter not in guessed:
                    guessed.append(letter)
                    if letter not in word:
                        limbs += 1
                    redraw_game_window()

                    # Check game end conditions
                    if limbs == max_limbs:
                        end(winner=False)
                    elif all((c in guessed or c == ' ') for c in word):
                        end(winner=True)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
