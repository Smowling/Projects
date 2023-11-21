import project
from project import Player
import pytest
import cards

def test_Player_class_str_init(capsys):
    player1 = Player("Smow")
    card = cards.load_cards("cah_test_1.txt")
    player1.cards += card
    print(player1)
    captured = capsys.readouterr()
    assert captured.out == "Smow's cards:\n1. Another shitty year.\n"


def test_Player_class_play():
    player1 = Player("")
    card = cards.load_cards("cah_test_1.txt")
    player1.cards += card
    assert player1.play(0) == "Another shitty year."

def test_Player_score():
    player1 = Player("")
    player1.score()
    player1.score()
    player1.score()
    assert player1.points == 3


def test_load_cards():
    assert cards.load_cards("cah_test_1.txt") == ["Another shitty year."]


def test_random_black():
    assert cards.random_black([]) == "No cards left to play."
    assert cards.random_black(["Black card _."]) == ("Black card _.", 1)
    assert cards.random_black(["Black card _.", "_ is 50/50 to _"]) == ("Black card _.", 1) or ("50/50", 2)


def test_combine_cards():
    assert cards.combine_cards("Here we go, _.", ["Another shitty year."]) == "Here we go, Another shitty year."
    assert cards.combine_cards("Test my _, I test your's _.", ["Tmp.", "Assets."]) == "Test my Tmp., I test your's Assets."


def test_draw_white():
    card = cards.load_cards("cah_test_1.txt")
    assert cards.draw_white(card) == ["Another shitty year."]

def test_draw_white_2():
    card = cards.load_cards("cah_test_2.txt")
    assert cards.draw_white(card, 2) == ["A visually arresting turtleneck.", "Another shitty year."] or ["Another shitty year.", "A visually arresting turtleneck."]

def test_draw_white_3():
    card = cards.load_cards("cah_test_2.txt")
    assert cards.draw_white(card, 3) == "Not enough cards to draw from."

def test_round_winners():
    played = []
    played.append({"name":"Smow", "card":"Test card value.", "votes":3})
    played.append({"name":"C-3PO", "card":"Test card value 2.", "votes":1})
    assert project.round_winners(played) == ["Smow"]

def test_round_winners_tie():
    played = []
    played.append({"name":"Smow", "card":"Test card value.", "votes":3})
    played.append({"name":"C-3PO", "card":"Test card value 2.", "votes":3})
    assert project.round_winners(played) == ["Smow", "C-3PO"]

def test_winner():
    players = []
    players.append(Player("Smow"))
    players.append(Player("C-3PO"))
    players[0].score()
    players[0].score()
    players[1].score()
    assert project.winner(players) == ["Smow"]

def test_winner_tie():
    players = []
    players.append(Player("Smow"))
    players.append(Player("C-3PO"))
    players[0].score()
    players[0].score()
    players[1].score()
    players[1].score()
    assert project.winner(players) == ["Smow", "C-3PO"]

def test_get_players_count_min(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 3)
    assert project.get_players_count("Prompt: ") == 3

def test_get_players_count_max(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 10)
    assert project.get_players_count("Prompt: ") == 10

def test_get_players_count_out_of_range(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 0)
    monkeypatch.setattr("builtins.input", lambda _: 11)
    monkeypatch.setattr("builtins.input", lambda _: 6)
    assert project.get_players_count("Prompt: ") == 6

def test_generate_players(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Smow")
    players = []
    players = project.generate_players(1)
    assert players[0].name == "Smow"

