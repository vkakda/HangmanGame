# Hangman Game

A modern, visually appealing Hangman game built with Python and Pygame.

## Features
- Responsive UI: Buttons and layout adapt to window resizing.
- Colorful, interactive interface with gradient backgrounds and vibrant button colors.
- Smooth, scalable hangman images.
- Keyboard and mouse support for guessing letters.
- Displays win/lose messages and the correct word at the end.
- Easy to add your own word list via `words.txt`.

## Requirements
- Python 3.x
- Pygame

## Setup
1. Install Python 3.x from [python.org](https://www.python.org/downloads/).
2. Install Pygame:
   ```sh
   pip install pygame
   ```
3. Ensure you have the following files in the same directory:
   - `hangman.py` (main game script)
   - `words.txt` (list of words/phrases, one per line)
   - `hangman0.png` to `hangman6.png` (hangman images for each stage)

## How to Play
- Run the game:
  ```sh
  python hangman.py
  ```
- Click on the letter buttons or use your keyboard to guess letters.
- The game ends when you either guess the word or run out of attempts.
- Press any key to play again after a win or loss.

## Customization
- **Word List:** Edit `words.txt` to add or remove words/phrases.
- **Images:** Replace `hangman0.png` to `hangman6.png` for custom hangman graphics.

## Graphical Representation

Below is a sample of how the game window and hangman graphics might look during gameplay:

```
+-------------------------------+
|         HANGMAN GAME          |
|-------------------------------|
|   | [A] [B] [C] ... [Z]       |
|                               |
|    ______                           |
|  |/      |                    |
|  |      ( )                   |
|  |      /|\                  |
|  |      / \                  |
|  |                            |
| _|___                         |
|                               |
|  _ _ _ _   _ _ _ _           |
|                               |
        |
+-------------------------------+
```

- The hangman image updates as incorrect guesses are made.
- Letter buttons are displayed in vibrant colors and are clickable.
- The word/phrase is shown as underscores, revealing correct guesses.
- The background features a smooth color gradient for a modern look.

You can further customize the graphics by editing the hangman images (`hangman0.png` to `hangman6.png`) and adjusting the color scheme in the code.

## Credits
- Developed as a project for my college - SRGC, Muzaffarnagar.
- Inspired by classic Hangman games, with modern UI enhancements.

---
Enjoy playing Hangman!
