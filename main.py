import sys
from time import sleep
from pygame.locals import *
from player import *
from title_screen import *

# Initialize pygame
pygame.init()
pygame.font.init()

# setup clock
clock = pygame.time.Clock()

# setup screen
screen = pygame.display.set_mode(WIN_SIZE)  # returns pygame surface object)
pygame.display.set_caption(f'Black Jack - v{ver} {date}')  # set the window name
pygame.display.set_icon(ICON)
background_color = GREEN

# game variables
bank = Player(name='Bank', is_human=False)
player = Player(name='Player 1', is_human=True)
bank_hand_score = 0
player_hand_score = 0
game_running = True
game_state = 0  # 0 - Start Screen, 1 - Game
frame = 0
deck = Deck()  # Create a deck of cards object
title_screen = TitleScreen(screen)  # Creates an title screen object
player_turn = True  # Human player starts the game
msg = ''
bank_has_black_jack = False
player_has_black_jack = False
second_card_open = False


# functions
def draw_new_card(is_human):
    pygame.display.update()
    sleep(0.5)
    if is_human:
        player.hit_card(deck)
        player.render_hand(surface=screen, player_turn=player_turn)
    else:
        bank.hit_card(deck)
        bank.render_hand(surface=screen, player_turn=player_turn)
    pygame.display.update()


def setup_round():
    # Deal First Card
    draw_new_card(is_human=True)  # Player Card
    draw_new_card(is_human=False)  # Bank Card

    # Deal Second Card
    draw_new_card(is_human=True)  # Player Card
    draw_new_card(is_human=False)  # Bank Card
    bank.hand[1].open_card = False  # 2nd bank card is closed


def render_table():
    screen.fill(background_color)  # Feel background with solid color
    # Draw the card deal areas for bank and player
    pygame.draw.rect(surface=screen, color=WHITE, rect=(240, 20, 730, 250), width=10, border_radius=10)  # bank
    pygame.draw.rect(surface=screen, color=WHITE, rect=(240, 320, 730, 250), width=10, border_radius=10)  # player
    # Render the current game scores
    render_game_scores()


def render_game_scores():

    # calculate scores
    bank_score = bank.count_card_score()
    player_score = player.count_card_score()

    # Fonts
    score_font = pygame.font.SysFont('Consolas', 28, True)
    bet_font = pygame.font.SysFont('consolas', 18, True)

    # Bank Info
    bank_name = score_font.render(f'{bank.name}', True, WHITE)
    bank_score = score_font.render(f'Score: {bank_score}', True, WHITE)
    bank_name_rect = bank_name.get_rect(topleft=(20, 20))
    bank_score_rect = bank_score.get_rect(topright=(1180, 20))
    screen.blit(bank_name, bank_name_rect)
    screen.blit(bank_score, bank_score_rect)

    # Player info
    player_name = score_font.render(f'{player.name}', True, WHITE)
    player_score = score_font.render(f'Score: {player_score}', True, WHITE)
    player_name_rect = player_name.get_rect(topleft=(20, 320))
    player_score_rect = player_score.get_rect(topright=(1180, 320))
    screen.blit(player_name, player_name_rect)
    screen.blit(player_score, player_score_rect)

    # Player money
    font_color = RED if player.money < 0 else WHITE
    player_money = bet_font.render(f'Money: €{int(player.money)}', True, font_color)
    player_money_rect = player_money.get_rect(topright=(1180, 525))
    screen.blit(player_money, player_money_rect)

    # Player bet
    player_bet = bet_font.render(f'next bet: €{int(player.bet)}', True, WHITE)
    player_bet_rect = player_bet.get_rect(topright=(1180, 550))
    screen.blit(player_bet, player_bet_rect)


def render_message(message: str):
    # Font for game messages
    message_font = pygame.font.SysFont('Consolas', 32, True)
    message_text = message_font.render(message, True, RED)
    message_text_rect = message_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
    screen.blit(message_text, message_text_rect)


# Game Loop
while game_running:  # Game Loop

    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False

        # Change from player to CPU (manual)
        if event.type == KEYDOWN:

            if event.key == K_SPACE:
                # if game_state == 0:
                    # player.money -= player.bet
                    # render_table()
                    # setup_round()  # deal bank and player cards
                    # bank_hand_score = bank.count_card_score()
                    # player_hand_score = player.count_card_score()
                    # game_state = 1

                if game_state == 1:
                    if player_turn:
                        player.hit_card(deck)
                        player_hand_score = player.count_card_score()

                elif game_state == 0 or game_state == 3:  # End state
                    frame = 0  # reset the frames
                    player.money -= player.bet  # Place the bet
                    deck = Deck()  # Create a new deck of cards object
                    player_turn = True  # Human player always starts the game
                    bank_has_black_jack = False  # reset bank black jack state
                    player_has_black_jack = False  # reset player black jack state
                    second_card_open = False  # Bank 2nd card is closed
                    player.hand = []  # empty the player hand
                    bank.hand = []  # Empty the bank hand
                    player.count_card_score()  # reset the player score
                    bank.count_card_score()  # reset the bank score
                    render_table()  # render the game environment
                    setup_round()  # Setup the new round
                    game_state = 1  # skip the intro
                    msg = ''  # reset msg to display

            if game_state == 1 and (event.key == K_p or event.key == K_RETURN):
                if player_turn:
                    player_turn = False
                    bank.hand[1].open_card = True
                    second_card_open = True

            if event.key == K_RIGHTBRACKET or event.key == K_EQUALS:
                if player.bet <= 90:
                    player.bet += 10

            if event.key == K_LEFTBRACKET or event.key == K_MINUS:
                if player.bet >= 20:
                    player.bet -= 10

            if event.key == K_BACKSPACE:
                game_state = 0
                frame = 0

    # renders the background
    render_table()

    # TITLE SCREEN - GAME STATE 0
    if game_state == 0:
        title_screen.display(game_state=game_state, frame=frame)

    # GAME SCREEN - GAME STATE 1
    # GAME LOGIC COMES HERE
    if game_state in [1, 2, 3]:

        # Render CPU Hand
        bank.render_hand(surface=screen, player_turn=player_turn)

        # Render Player Hand
        player.render_hand(surface=screen, player_turn=player_turn)

        if game_state == 1:

            if player_turn:
                player_hand_score = player.count_card_score()

                if player_hand_score > 21:
                    game_state = 2
                    msg = "Player hand score over 21, You LOSE!"

                elif len(player.hand) == 2 and player_hand_score == 21:
                    player_has_black_jack = True
                    player_turn = False  # bank is next!
                    msg = "Player has BLACK JACK!"

                elif player_hand_score == 21:
                    player_turn = False  # bank is next!
                    msg = "Player has 21!"

            elif not player_turn:
                bank_hand_score = bank.count_card_score()

                # Bank hand score > 21
                if bank_hand_score > 21:
                    game_state = 2
                    msg = "Bank hand score over 21, You WIN!"
                    player.money += 2 * player.bet
                    player.count_card_score()

                # Bank has Black Jack
                elif len(bank.hand) == 2 and bank_hand_score == 21:
                    bank_has_black_jack = True
                    game_state = 2
                    msg = "Bank has BLACK JACK!"

                # Bank stands when hand score greater than or equal to 17
                elif bank_hand_score >= 17:
                    game_state = 2

                # Bank draws card when hand score smaller than or equal to 16
                elif bank_hand_score < player_hand_score and bank_hand_score <= 16:
                    draw_new_card(is_human=False)
                    bank_hand_score = bank.count_card_score()

        if game_state == 2:

            if bank_has_black_jack and player_has_black_jack:
                msg = "Player and Bank both have BLACK JACK, It's a TIE!"
                player.money += 1.5 * player.bet

            elif bank_has_black_jack and not player_has_black_jack:
                msg = "Bank has Black Jack! You LOSE!"

            elif player_has_black_jack and not bank_has_black_jack:
                msg = "Player has Black Jack! You WIN!"
                player.money += 2.5 * player.bet

            elif player_hand_score == bank_hand_score and player_hand_score <= 21:
                msg = "Player and Bank score equal, It's a TIE!"
                player.money += player.bet

            elif player_hand_score < bank_hand_score <= 21:
                msg = "Bank scores higher, You LOSE!"

            elif bank_hand_score < player_hand_score <= 21:
                msg = "Bank scores lower, You WIN!"
                player.money += 2 * player.bet

            game_state = 3

        if game_state in [1, 2, 3]:
            render_message(msg)

    # FPS timer
    clock.tick(FPS)  # maintain 'FPS' frames per second

    # Update the screen
    pygame.display.update()

    frame += 1

pygame.quit()
sys.exit('\nProgrammed terminated by user')
