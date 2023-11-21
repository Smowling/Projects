import 'package:flutter/material.dart';
import 'package:Order98/how_to.dart';
import 'package:Order98/new_game.dart';

class MenuScreen extends StatefulWidget {
  const MenuScreen({super.key});

  @override
  State<MenuScreen> createState() => _MenuScreenState();
}

class _MenuScreenState extends State<MenuScreen> {
  @override
  Widget build(BuildContext context) {
    return Material(
      child: Container(
        width: double.infinity,
        color: const Color.fromARGB(255, 8, 135, 160),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const Column(
              children: [
                 Text(
                  "Order98",
                  style: TextStyle(
                    color: Colors.black,
    
                    fontSize: 50,
                    fontWeight: FontWeight.normal,
                  ),
                ),
              ],
            ),
            Column(
              children: [
                ElevatedButton(
                  onPressed: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (BuildContext context) {
                          return const NewGame();
                        },
                      ),
                    );
                  },
                  child: const Text('Play'),
                ),
                ElevatedButton(
                  onPressed: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (BuildContext context) {
                          return const HowToPlay();
                        },
                      ),
                    );
                  },
                  child: const Text('How to play'),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
