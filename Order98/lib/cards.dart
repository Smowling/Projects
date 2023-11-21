import 'package:flutter/material.dart';

class Cards{
  late int cardNumber;
  late Color cardColor;
  // late IconData cardIcon;

  Cards(int number){
    cardNumber = number;
    // switch set color
    switch (number) {
      case < 10: {
        cardColor = Colors.grey.shade300;
        break;
      }
      case < 20: {
        cardColor = Colors.indigo;
        break;
      }
      case < 30: {
        cardColor = Colors.blue;
        break;
      }
      case < 40: {
        cardColor = Colors.blueGrey;
        break;
      }
      case < 50: {
        cardColor = Colors.brown;
        break;
      }
      case < 60: {
        cardColor = Colors.deepOrange;
        break;
      }
      case < 70: {
        cardColor = Colors.lightGreen;
        break;
      }
      case < 80: {
        cardColor = Colors.deepPurple;
        break;
      }
      case < 90: {
        cardColor = Colors.purple;
        break;
      }

      default: cardColor = Colors.lightBlue;
    }
    // switch set icon
    // switch (number % 10){
    //   case 0: cardIcon = Icons.circle;
    //   case 1: cardIcon = Icons.circle_outlined;
    //   case 2: cardIcon = Icons.square;
    //   case 3: cardIcon = Icons.square_outlined;
    //   case 4: cardIcon = Icons.pix;
    //   case 5: cardIcon = Icons.power_input;
    //   case 6: cardIcon = Icons.key;
    //   case 7: cardIcon = Icons.keyboard_capslock;
    //   case 8: cardIcon = Icons.ac_unit;
    //   case 9: cardIcon = Icons.yard;
    //   default: cardIcon = Icons.circle_outlined;
    // }
  }

}