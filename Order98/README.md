# Order98

I present you my android app made in Flutter and dart programing language for CS50 final project.

#### Video Demo:  https://youtu.be/8k0w8f046UQ

#### Description:

I'm a huge fan of boardgames, one of which is "The Game". Thats a simple game where you play 98 numbered cards (from 2 to 99) on 4 card piles.
I love it so much that I wanted to have it on me and play when I want. So I thought of creating an app for that, and here we are.

### Rules:

As mentioned before you have to play 98 cards, 2 at a time on 4 card piles, two of them are in ascending and the other two are descending order. There is a twist on top of that - you can "make a save" play, that is play a card with differance of exactly 10 on stack omiting asc/desc rule. Simply put you have 46 on ascending pile, you can play anything that is higher than 46 or a card with 36 printed on it. 


### App in details

All files are in lib folder, it has a file for a class, provider and app screens.
In this app there are 3 different routes(app screens): menu_screen, new_game and how_to.

### Cards and provider

Starting with cards class to simplify their creation. This class has number and based on that it adds a color property.
Provider on the other hand has a lot of properties. Starting with deck, and card piles propetries. It has an initializer, that shuffles deck and draws 8 starting cards.
On top of that it has functions that help out with game state management like undo and restart or play.

### Routes
Menu starts as a default view, it has two buttons and an text widget to show app name. Buttons route to game and how to play.

How to is an simple "wall of text" explaining how to play.

Game screen has all logic it needs to play.
It has quite a few custom widgets I use to build app. Each of these widgets gets a provider to work with. Its required to store game state. 

In appbar there is a button to reset game state, it uses function that is created in provider class.

Below that are 4 piles where we can play cards to. Each of them accepts Cards object, if its a valid play (there is a function that handles this logic) than card is accepted and value and color of pile changes.

Cards are build with gridview widget based on list of Cards objects stored in provider hand variable. You play card with simple drag and drop action on top of one of piles above.

In bottom bar there are two buttons. Lets start with draw button. It simply draws you cards up to your hand limit, which is 8. But you need to have at most 6 cards to being able to draw (you need to play two cards first). Function that does it is in provider class.

On the left side there is Undo button, it lets you undo all your moves you did this round. It is also a function created in provider class.

On top of these functions game checks if you have any valid moves to do, if not you will get info on the bottom bar and you will have to restart game state to play again.

If you play the last of your cards game will show you win screen.

Give this game a try, its not that easy as it looks.