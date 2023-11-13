from random import choice, randint
from settings import *
from deck import Deck, Card


class TitleScreen:
    pygame.font.init()

    welcome_font_1 = pygame.font.SysFont('Consolas', 128, True)
    welcome_text_1 = welcome_font_1.render('Black Jack', True, GREEN)
    welcome_text_rect_1 = welcome_text_1.get_rect(center=(WIN_WIDTH // 2, 175))

    welcome_font_2 = pygame.font.SysFont('Consolas', 32, True)
    welcome_text_2 = welcome_font_2.render(f"Press 'space' to begin", True, GREEN)
    welcome_text_rect_2 = welcome_text_2.get_rect(center=(WIN_WIDTH // 2, 250))

    def __init__(self, surface):
        self.deck = Deck()
        self.deck.shuffle()
        self.surface = surface
        self.card_list = []

    def display(self, game_state, frame):

        # Setup cards for BLACK JACK logo
        card1 = Card('spades', 'ace')
        card1.card_image = pygame.transform.rotate(card1.card_image, 5)
        card2 = Card('spades', 'jack')
        card2.card_image = pygame.transform.rotate(card2.card_image, -20)

        if frame % 60 == 0 and len(self.deck.cards()) > 0:
            new_card = self.deck.cards().pop()
            self.card_list.append(new_card)
            new_card.delta_x = choice([-2, -1, 1, 2])
            new_card.delta_y = choice([-2, -1, 1, 2])

            # scale the card image
            new_card.card_image = pygame.transform.scale(new_card.card_image,
                                                         (int(new_card.card_image.get_width() * 0.1),
                                                          int(new_card.card_image.get_height() * 0.1)))

            # create rect for card on random starting location on screen
            new_card.card_rect = new_card.card_image.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 100))

        if game_state == 0:  # 0 - Title Screen
            self.surface.fill(DARK_GREY)  # Background color for Title Screen

            # render the card animation on the title screen
            for card in self.card_list:
                self.surface.blit(card.card_image, card.card_rect)
                card.card_rect.right += card.delta_x
                card.card_rect.bottom += card.delta_y

                # when card reaches the bottom or top side of the screen inverse delta_y
                if card.card_rect.bottom >= WIN_HEIGHT or card.card_rect.top <= 0:
                    card.delta_y *= -1

                # when card reaches the left or right side of the screen inverse delta_x
                if card.card_rect.right >= WIN_WIDTH or card.card_rect.left <= 0:
                    card.delta_x *= -1

                if card.card_rect.top <= TitleScreen.welcome_text_rect_1.bottom \
                        and (card.card_rect.right >= TitleScreen.welcome_text_rect_1.left
                             or card.card_rect.left <= TitleScreen.welcome_text_rect_1.right):
                    card.delta_y *= -1

                if card.card_rect.bottom <= TitleScreen.welcome_text_rect_1.top \
                        and (card.card_rect.right >= TitleScreen.welcome_text_rect_1.left
                             or card.card_rect.left <= TitleScreen.welcome_text_rect_1.right):
                    card.delta_y *= -1

                if card.card_rect.right >= TitleScreen.welcome_text_rect_1.left \
                        and (card.card_rect.bottom <= TitleScreen.welcome_text_rect_1.top
                             or card.card_rect.top >= TitleScreen.welcome_text_rect_1.bottom):
                    card.delta_x *= -1

                if card.card_rect.left <= TitleScreen.welcome_text_rect_1.right \
                        and (card.card_rect.bottom <= TitleScreen.welcome_text_rect_1.top
                             or card.card_rect.top >= TitleScreen.welcome_text_rect_1.bottom):
                    card.delta_x *= -1

            # blit the Title Page text
            self.surface.blit(TitleScreen.welcome_text_1, TitleScreen.welcome_text_rect_1)
            self.surface.blit(TitleScreen.welcome_text_2, TitleScreen.welcome_text_rect_2)

            card1.render(surface=self.surface, pos_x=480, pos_y=300, scale=0.3)
            card2.render(surface=self.surface, pos_x=510, pos_y=320, scale=0.3)
