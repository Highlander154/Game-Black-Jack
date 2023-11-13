from settings import *
from random import shuffle


class Card:

    def __init__(self, suit, value):
        self.__suit = suit
        self.__value = value
        self.open_card = True
        self.card_image = self.load_card_image(self.open_card)

    def __repr__(self):
        return f"{self.__value} of {self.__suit}"

    @property
    def suit(self):
        return self.__suit

    @property
    def value(self):
        return self.__value

    @property
    def width(self):
        return self.card_image.get_width()

    @property
    def height(self):
        return self.card_image.get_height()

    def load_card_image(self, open_card):
        if open_card:
            card_image = pygame.image.load(f'img/{self.__value}_of_{self.__suit}.png').convert_alpha()
        else:
            card_image = pygame.image.load('img/back.png').convert_alpha()
        return card_image

    def render(self, surface, pos_x, pos_y, scale: float = 1):
        # scale card image
        card_image = pygame.transform.scale(self.card_image, (int(self.card_image.get_width() * scale),
                                                              int(self.card_image.get_height() * scale)))
        # render the card to the screen
        surface.blit(card_image, (pos_x, pos_y))


class Deck:
    def __init__(self):
        self.__suits = ['hearts', 'spades', 'diamonds', 'clubs']
        self.__values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king', 'ace']
        self.__deck = []
        self.create()
        self.shuffle()

        self.pos_x = 10
        self.pos_y = 10

    @property
    def suits(self):
        return self.__suits

    @property
    def values(self):
        return self.__values

    @property
    def deck(self):
        return self.__deck

    def create(self):
        for suit in self.__suits:
            for value in self.__values:
                self.__deck.append(Card(suit, value))

    def shuffle(self):
        shuffle(self.__deck)

    def cards(self):
        return self.__deck

    def render_default_deck(self, surface):
        """ Renders a full deck of cards (not shuffled) """

        surface.fill(DARK_GREY)
        scale = 0.16

        for s, suit in enumerate(self.suits):
            for v, value in enumerate(self.values):
                card = Card(suit=suit, value=value)
                card.render(surface, self.pos_x, self.pos_y, scale)

                self.pos_x += card.width * scale + 10  # new card positions at x = card width + 10

            self.pos_x = 10  # New row starts at x = 10
            self.pos_y += card.height * scale + 10  # New row start at y + card height + 10

        self.pos_y = 10  # Reset original y position
        self.pos_x = 10  # Reset original x position

    def render_current_deck(self, surface):
        """ Renders a full deck of cards (not shuffled) """

        surface.fill(DARK_GREY)
        scale = 0.1

        for i in range(len(self.suits)):
            for j in range(len(self.values)):
                card_number = i * len(self.values) + j
                card = self.deck[card_number]
                card.render(surface, self.pos_x, self.pos_y, scale)

                self.pos_x += card.width * scale + 10  # new card positions at x = card width + 10

            self.pos_x = 10  # New row starts at x = 10
            self.pos_y += card.height * scale + 10  # New row start at y + card height + 10

        self.pos_y = 10  # Reset original y position
        self.pos_x = 10  # Reset original x position


