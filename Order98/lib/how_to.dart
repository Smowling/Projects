import 'package:flutter/material.dart';

class HowToPlay extends StatefulWidget {
  const HowToPlay({super.key});

  @override
  State<HowToPlay> createState() => _HowToPlayState();
}

class _HowToPlayState extends State<HowToPlay> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.grey.shade300,
        child: Center(
          child: FractionallySizedBox(
            widthFactor: 0.9,
            heightFactor: 1,
            child: Container(
              color: Colors.grey.shade300,
              child: const Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Text(
                      "In Order98 each player starts with 8 cards in their hand, and four piles: two showing 1 and an up arrow and two showing 100 and a down arrow."),
                  Text(
                      "On a turn, a player must play at least two cards from their hand onto one or more piles, with cards on the 1 piles being placed in ascending order and cards on the 100 piles being placed in descending order."),
                  Text(
                      "One tricky aspect of the game is that you can play a card exactly 10 higher/lower than the top card of a discard pile even when you would normally have to play in a descending/ascending order, e.g., if a 100 discard pile is topped with an 87, you can play any card lower than 87 or you can play the 97."),
                  Text(
                      "After a player plays at least two cards from hand, they refill their hand from the deck."),
                  Text("If you play all 98 cards, you win!"),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
