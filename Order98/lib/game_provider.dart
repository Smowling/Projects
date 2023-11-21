import 'package:flutter/material.dart';
import 'package:Order98/cards.dart';

class GameProvider extends ChangeNotifier {
  List<int> deck = <int>[for (var i = 2; i < 100; i++) i];
  List<Cards> hand = <Cards>[];
  List<Cards> tempHand = <Cards>[];

  int asc1 = 1;
  int asc2 = 1;
  int desc1 = 100;
  int desc2 = 100;

  int tempAsc1 = 1;
  int tempAsc2 = 1;
  int tempDesc1 = 100;
  int tempDesc2 = 100;

  Color descColor1 = const Color.fromARGB(255, 47, 172, 122);
  Color descColor2 = const Color.fromARGB(255, 47, 172, 122);
  Color ascColor1 = const Color.fromARGB(255, 69, 96, 194);
  Color ascColor2 = const Color.fromARGB(255, 69, 96, 194);

  Color tempDescColor1 = const Color.fromARGB(255, 47, 172, 122);
  Color tempDescColor2 = const Color.fromARGB(255, 47, 172, 122);
  Color tempAscColor1 = const Color.fromARGB(255, 69, 96, 194);
  Color tempAscColor2 = const Color.fromARGB(255, 69, 96, 194);

  GameProvider() {
    deck.shuffle();
    draw();
  }

  void draw() {
    while (hand.length < 8 && deck.isNotEmpty) {
      hand.add(Cards(deck.removeLast()));
    }
    tempAsc1 = asc1;
    tempAscColor1 = ascColor1;
    tempAsc2 = asc2;
    tempAscColor2 = ascColor2;
    tempDesc1 = desc1;
    tempDescColor1 = descColor1;
    tempDesc2 = desc2;
    tempDescColor2 = descColor2;

    tempHand.clear();
    tempHand.addAll(hand);

    notifyListeners();
  }

  void undo() {
    asc1 = tempAsc1;
    ascColor1 = tempAscColor1;
    asc2 = tempAsc2;
    ascColor2 = tempAscColor2;
    desc1 = tempDesc1;
    descColor1 = tempDescColor1;
    desc2 = tempDesc2;
    descColor2 = tempDescColor2;

    hand.clear();
    hand.addAll(tempHand);
    notifyListeners();
  }

  void restart() {
    deck = <int>[for (var i = 2; i < 100; i++) i];
    deck.shuffle();
    hand.clear();
    tempHand.clear();
    draw();
    asc1 = 1;
    asc2 = 1;
    desc1 = 100;
    desc2 = 100;

    tempAsc1 = 1;
    tempAsc2 = 1;
    tempDesc1 = 100;
    tempDesc2 = 100;

    descColor1 = const Color.fromARGB(255, 47, 172, 122);
    descColor2 = const Color.fromARGB(255, 47, 172, 122);
    ascColor1 = const Color.fromARGB(255, 69, 96, 194);
    ascColor2 = const Color.fromARGB(255, 69, 96, 194);

    tempDescColor1 = const Color.fromARGB(255, 47, 172, 122);
    tempDescColor2 = const Color.fromARGB(255, 47, 172, 122);
    tempAscColor1 = const Color.fromARGB(255, 69, 96, 194);
    tempAscColor2 = const Color.fromARGB(255, 69, 96, 194);
  }

  void play(Cards card) {
    hand.remove(card);
    notifyListeners();
  }
}
