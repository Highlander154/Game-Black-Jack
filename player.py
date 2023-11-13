class Player:
    def __init__(self, name: str, is_human: bool = True):
        self.is_human = is_human  # True if player is human player else False
        self.name = name
        self.credit = 0
        self.hand_score = 0
        self.hand = []
        self.money = 200
        self.bet = 10

    def __repr__(self):
        return self.name

    def hit_card(self, deck):
        self.hand.append(deck.deck.pop())  # pop a card from the deck and add to player hand

    def render_hand(self, surface, player_turn):
        if self.is_human:
            pos_x = 270
            pos_y = 350
            scale = 0.25
        else:
            pos_x = 270
            pos_y = 50
            scale = 0.25

        for card in self.hand:
            if not self.is_human and player_turn and self.hand.index(card) == 1:
                card.card_image = card.load_card_image(False)  # Closed Card
                card.open_card = False
            else:
                card.card_image = card.load_card_image(True)  # Open Card
                card.open_card = True
            card.render(surface, pos_x, pos_y, scale)
            pos_x += card.width * scale + 10

    def count_card_score(self):
        self.hand_score = 0

        # First check all cards except the aces for score
        for card in self.hand:
            if card.value in ['queen', 'jack', 'king'] and card.open_card:
                self.hand_score += 10
            elif card.value in [2, 3, 4, 5, 6, 7, 8, 9, 10] and card.open_card:
                self.hand_score += card.value

        # Then check aces for score
        for card in self.hand:
            if card.value == 'ace' and 0 <= self.hand_score <= 10 and card.open_card:
                self.hand_score += 11
            elif card.value == 'ace' and self.hand_score > 10 and card.open_card:
                self.hand_score += 1

        return self.hand_score
