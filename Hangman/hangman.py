import pygame
from pygame import mixer
from sys import exit
from random import choice

# Set up the word to guess from the start
choices = ['Banana', 'Pera', 'Manzana', 'Cereza', 'Kiwi', 'Mango', 'Limon', 'Melon', 'Sandia', 'Frambuesa', 'Tomate',
           'Tuna', 'Melocoton', 'Fresa', 'Arandano', 'Pimiento', 'Pitahaya', 'Guayaba', 'Calabaza', 'Pepino', 'Cacao']
secret_word = choice(choices).lower()

# game initial state
word_completion = '_' * len(secret_word)
guessed_letters = ''
wrong_letters = ''
# Number of attempts before the game ends
tries = 6

# Player input string
user_text = ''
guess = ''

# flag to loop the game
game_active = True


# Render the word completion
def display_guess(completion):
    correct_surface = game_font.render('Palabra: ', False, 'Black')
    guess_surface = game_font.render(completion, False, 'Brown')
    screen.blit(correct_surface, (30, 160))
    screen.blit(guess_surface, (30, 225))


# Used to update the player text input
def display_input(character):
    input_surface = game_font.render('Ingresa una letra:', False, 'White')
    character_surface = game_font.render(character, False, 'Yellow')
    screen.blit(input_surface, (30, 360))
    screen.blit(character_surface, (30, 410))


# The game background
def display_interface():
    # convert image to an easier render format
    green_surface = pygame.image.load("./GFX/Yellow_Background.png").convert()
    blue_surface = pygame.image.load("./GFX/Blue_Background.png").convert()
    screen.blit(green_surface, (0, 0))
    screen.blit(blue_surface, (0, 320))

    # Wrong guess section
    wrong_surface = game_font.render('Letras incorrectas', False, (255, 25, 48))
    wrong_letters_surface = game_font.render(wrong_letters, False, (255, 25, 48))
    wrong_rectangle = wrong_surface.get_rect(center=(300, 50))
    screen.blit(wrong_surface, wrong_rectangle)
    screen.blit(wrong_letters_surface, (30, 100))

    # Copyright - Oscar Moyeda
    credits_surface = generic_font.render('Hecho por Oscar Moyeda', False, 'Black')
    screen.blit(credits_surface, (720, 480))


def update_hanged_state(number_tries):
    # Mapping the hangman stages
    hanged_stages = {
        5: './GFX/Hanged_Stage1.png',
        4: './GFX/Hanged_Stage2.png',
        3: './GFX/Hanged_Stage3.png',
        2: './GFX/Hanged_Stage4.png',
        1: './GFX/Hanged_Stage5.png',
        0: './GFX/Hanged_Stage6.png',
    }

    if number_tries == 6:
        shrek_surface = pygame.Surface((255, 255), pygame.SRCALPHA)
        shrek_surface.fill((0, 0, 0, 0))
    else:
        shrek_surface = pygame.image.load(hanged_stages.get(number_tries, './GFX/Shrek.png')).convert_alpha()

    pole_surface = pygame.image.load("./GFX/Pole.png").convert_alpha()
    screen.blit(pole_surface, (600, 12))
    screen.blit(shrek_surface, (600, 50))


def game_over_screen(message, background, state_image, word):
    # Load the assets
    game_over_background = pygame.image.load(background).convert()
    game_over_message = game_font.render(message, False, 'Black')
    game_over_image = pygame.image.load(state_image).convert_alpha()
    space_surface = pygame.image.load("./GFX/space_bar.png").convert_alpha()
    space_text = game_font.render('ESPACIO', False, 'Black')
    play_again_text = game_font.render('¿Seguir jugando? Presiona', False, 'Black')

    # Display assets on screen
    screen.blit(game_over_background, (0, 0))
    screen.blit(game_over_message, (400, 40))
    screen.blit(game_over_image, (400, 100))
    screen.blit(space_surface, (280, 356))
    screen.blit(space_text, (400, 390))
    screen.blit(play_again_text, (150, 320))

    # Show the complete word
    word_message = game_font.render('Palabra:', False, 'Black')
    word_complete = game_font.render(word, False, 'Black')
    screen.blit(word_message, (30, 140))
    screen.blit(word_complete, (30, 180))

    # Credits - Oscar Moyeda
    credits_surface = generic_font.render('Hecho por Oscar Moyeda', False, 'Black')
    github_text = generic_font.render('Visita mi GitHub: 0scarMoyeda', False, 'Blue')
    screen.blit(credits_surface, (120, 480))
    screen.blit(github_text, (660, 480))


# Start game frame
pygame.init()

# Screen size and settings
screen = pygame.display.set_mode((1024, 512))
pygame.display.set_caption('Ahorcado')
icon_image = pygame.image.load("./GFX/Shrek_Lose.png")
pygame.display.set_icon(icon_image)
# Clock used to run the game at X fps
clock = pygame.time.Clock()

# Font family for the game (they can only be initialized after pygame.init())
game_font = pygame.font.Font('./GFX/Press_Start_2P/PressStart2P-Regular.ttf', 30)
generic_font = pygame.font.Font(None, 28)

# Background music
background_music = mixer.Sound('./SFX/All Star.mp3')
correct_sound = mixer.Sound('./SFX/Correct.mp3')
incorrect_sound = mixer.Sound('./SFX/Incorrect.mp3')
background_music.play(-1)

while True:
    # Run the game until QUIT [x] button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Get player character input
        # In main game screen
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_SPACE:
                    user_text = ''
                elif event.key == pygame.K_RETURN:
                    guess = user_text
                    user_text = ''
                else:
                    user_text = event.unicode.lower()
        # Game over screen
        else:
            # Restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                # Restart game settings
                secret_word = choice(choices).lower()
                word_completion = '_' * len(secret_word)
                guessed_letters = ''
                wrong_letters = ''
                tries = 6

    # Main game state
    if game_active:
        # If the word was completed
        if '_' not in word_completion:
            game_active = False
        # If the player runs out of tries
        elif tries <= 0:
            game_active = False

        # Render to the frame
        display_interface()
        display_guess(word_completion)
        display_input(user_text)
        update_hanged_state(tries)

        # Game
        # If the player already guessed or tried the letter
        if guess in guessed_letters or guess in wrong_letters:
            pass
        # If the letter is not in the secret word
        elif guess not in secret_word:
            wrong_letters += ' ' + guess
            tries -= 1
            incorrect_sound.play()
        # If the letter is indeed in the word and not guessed before
        else:
            guessed_letters += ' ' + guess
            for index in range(len(secret_word)):
                if secret_word[index] == guess:
                    word_completion = word_completion[:index] + guess + word_completion[index + 1:]
            correct_sound.play()

        # Restart the guess every attempt
        guess = ''

    else:
        if '_' not in word_completion:
            game_over_screen("Ganaste", './GFX/Green_Background.png', './GFX/Shrek_Win.png', secret_word)
        elif tries <= 0:
            game_over_screen("Perdiste", './GFX/Red_Background.png', './GFX/Shrek_Lose.png', secret_word)

    # Update screen every time
    pygame.display.update()

    # make the game run and update at max 60 frame rate
    clock.tick(60)
