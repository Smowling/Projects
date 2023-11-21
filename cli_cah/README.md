# Cards Against Humanity we have at home.
### Video DEMO: https://youtu.be/8KibTHl5Yd0
### Description:
#### I present to you The Cards Against Humanity game, runned in CLI with integrated AI that plays it with or for you. You can create from 3 to 10 players, you define how much rounds (black cards) do you want to play and off you go, have fun.
#### The idea for this project started while I was playing this game with friends of mine and I thought to myself - it would be cool to see some randomly created card combos in CAH game. I figured it shouldnt be that hard, so I downloaded cards from creators website and moved on with it as my final project for CS50Python.
## Files Overview
### 1. project.py
#### Its the main project file uses cards and random modules, it contains main function and Player class. Beside that in here are few complementary functions that smoothes out code readability.
#### Player class is used to handle players properties as name, cards in hand, points and if its an AI or not. It also has init and str methods to initialize and print players hand. On top of that there are play (to play a card) and score (to increase players points) functions.
#### Main function contains all game logic, it uses additional functions to handle some of it.
#### Logic goes like that:
#### 1. Loading cards to memory.
#### 2. Generating players list, count and players names are based on input while promped. You can leave blank name to create AI player. After creation all of them get hand of 10 cards.
#### 3. Geting number of rounds from user, no more than amount of black cards in file.
#### 4. With all that setup we can start a round loop. In which firstly we random black card to fill by players. Than we go through players list and make them to play a card or cards (if player is AI it is choosed by random) if black card requires more than one. All of these are saved as array of dicts containing players name, filled black card and votes=0. After all cards are picked program draws missing cards for players. Later all of these are sorted and printed for players to vote for (players can't vote on theirs card, AI votes by random). After voting program updates players points using score class function and that ends round loop, it loops n times, defined by user earlier.
#### 5. Program prints players final score and winner or winners if they have the same, highest score and this ends main.
#### Later in file we have complementary functions like round_winners and winners used to get winners. After this we get_players_count that returns number of players that is int bigger that 2 and lower than 11. And lastly generate_players that returns array of initialized Player objects.
### 2. cards.py
#### This module uses random module and contains 4 functions used to handle operations with cards.
#### load_cards(file) returns loaded file as array, its used to load black and white cards.
#### random_black(black_card) returns tuple of randomized black card and count of blanks to fill.
#### draw_white(card, n) returns array of white cards, by default it returns 1 card.
#### combine_cards(black, white[]) returnes combined black card with filled blank spots using array of white cards. It also replace .. with single .
### 3. test_project.py
#### File contains 17 tests using pytest functionality. Each of the functions explained above have defined at least one test to check if it works correctly.
#### Most of them are pretty self explenatory, few of them uses monkeypatch as argument and its .setattr function that is used to emulate users input.
### 4. cah_*.txt
#### Beside all of .py files there are few text files containing cards. Few of them are used in tests, cah_black_cards.txt and cah_white_cards.txt are main cards files used by program.