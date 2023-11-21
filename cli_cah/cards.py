import random

def load_cards(file):
    cards = []
    with open(file) as lines:
        for line in lines:
            cards.append(line.strip())
    return cards


def random_black(black_cards):
    if len(black_cards) != 0:
        card = random.choice(black_cards)
        black_cards.remove(card)
        return card, card.count("_")
    else:
        return "No cards left to play."


def draw_white(white_cards, n=1):
    cards = []
    if n <= len(white_cards):
        for _ in range(n):
            card = random.choice(white_cards)
            white_cards.remove(card)
            cards.append(card)
        return cards
    else:
        return "Not enough cards to draw from."


def combine_cards(black_card, white_cards):
    card = black_card
    for white_card in white_cards:
        card = card.replace("_", white_card, 1)
    card = card.replace("..", ".")
    return card



