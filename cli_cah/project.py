import cards
import random


class Player:
    _ai_names = ["C-3P0", "R2-D2", "BD-1", "R5-D4", "The Iron Giant",
                "Marvin", "T-800", "The Tin Man", "Wall-e", "Eve"]
    def __init__(self, name):
        if name == "" and len(self._ai_names) > 0:
            self.name = random.choice(self._ai_names)
            self._ai_names.remove(self.name)
            self.ai = True
        else:
            self.name = name
            self.ai = False
        self.cards = []
        self.points = 0

    def __str__(self):
        value = f"{self.name}'s cards:"
        for idx, card in enumerate(self.cards):
            value += f"\n{idx+1}. {card}"
        return value

    def play(self, n=0):
        if len(self.cards) == 0:
            return "No more cards to play."
        if n == 0 and self.ai == True:
            return self.cards.pop(random.randrange(len(self.cards)))
        else:
            return self.cards.pop(n-1)

    def score(self):
        self.points += 1



def main():
    cards_white = cards.load_cards("cah_white_cards.txt")
    cards_black = cards.load_cards("cah_black_cards.txt")

    players = generate_players(get_players_count("Players count (3-10): "))

    for player in players:
        player.cards += cards.draw_white(cards_white, 10)

    while True:
        try:
            rounds = int(input("Number of rounds: "))
            if rounds > 0 and rounds <= len(cards_black):
                break
            else:
                raise ValueError
        except:
            print(f"Input number bigger than 0 and lower than {len(cards_black)+1}")

    for round in range(rounds):
        black, white_n = cards.random_black(cards_black)
        print("------------------------------")
        print(f"Round {round+1}. Fill blank(s) in: {black}")
        played = []

        for player in players:
            cards_played = []
            for idx in range(white_n):
                if player.ai == True:
                    cards_played.append(player.play())
                else:
                    print(player)
                    card = int(-1)
                    while card < 0 or card > len(player.cards):
                        try:
                            card = int(input(f"Pick {idx+1} card to play: "))
                            if card < 0 or card > len(player.cards):
                                print(f"You don't have card with {card} index.")
                        except:
                            card = int(-1)
                            print("Please choose by card id.")
                    cards_played.append(player.play(card))

            player.cards += cards.draw_white(cards_white, white_n)
            tmp = {"name": player.name, "card": cards.combine_cards(black, cards_played), "votes": 0}
            played.append(tmp)

        played = sorted(played, key=lambda play: play["card"])
        for idx, play in enumerate(played):
            print(f"{idx+1}. {play['card']}")

        for player in players:
            if player.ai == True:
                while True:
                    choice = random.randrange(len(played))
                    if player.name != played[choice]["name"]:
                        played[choice]["votes"] += 1
                        break
            else:
                while True:
                    try:
                        choice = int(input(f"{player.name} pick a winning card: "))
                        if choice > 0 and choice <= len(played) and player.name != played[choice-1]["name"]:
                            played[choice-1]["votes"] += 1
                            break
                        else:
                            raise ValueError
                    except:
                        print(f"Please input number from 1 to {len(played)} and don't pick yourself.")

        round_winner = round_winners(played)
        for player in players:
            if player.name in round_winner:
                player.score()
    print("------------------------------")
    print("Final score: ")
    for player in players:
        print(f"{player.name} with score of {player.points} points.")

    win = winner(players)
    print("------------------------------")
    for w in win:
        print(f"Winner is: {w}")
    print("------------------------------")






def round_winners(played):
    winners = []
    score = 0
    for play in played:
        if score < play["votes"]:
            score = int(play["votes"])
    for play in played:
        if score == play["votes"]:
            winners.append(play["name"])
    return winners


def winner(players):
    winners = []
    score = 0
    for player in players:
        if score < player.points:
            score = int(player.points)
    for player in players:
        if score == player.points:
            winners.append(player.name)
    return winners


def get_players_count(prompt):
    while True:
        try:
            n = int(input(prompt))
        except ValueError:
            pass
        if 2 < n < 11:
            return n


def generate_players(n):
    players = []
    for i in range(n):
        name = input("Insert player's name, leave blank for AI: ")
        players.append(Player(name))
    return players





if __name__ == "__main__":
    main()