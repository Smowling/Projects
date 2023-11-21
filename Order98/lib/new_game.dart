import 'package:flutter/material.dart';
import 'package:Order98/game_provider.dart';
import 'package:provider/provider.dart';
import 'cards.dart';

class NewGame extends StatefulWidget {
  const NewGame({super.key});

  @override
  State<NewGame> createState() => _NewGameState();
}

class _NewGameState extends State<NewGame> {
  @override
  Widget build(BuildContext context) {
    return Consumer<GameProvider>(
      builder: (context, gameProviderModel, child) => Material(
        type: MaterialType.transparency,
        child: Scaffold(
          backgroundColor: Colors.blueAccent.shade100,
          appBar: AppBar(
            automaticallyImplyLeading: false,
            shadowColor: Colors.black,
            elevation: 8,
            centerTitle: true,
            title: const Text("Order98"),
            backgroundColor: Colors.blueGrey,
            actions: [
              GestureDetector(
                onTap: () {
                  showDialog(
                    context: context,
                    builder: (context) => AlertDialog(
                      title: const Text("Restart game?"),
                      content: const Text(
                          "Are you sure you want to restart current game state?"),
                      actions: [
                        TextButton(
                            onPressed: () {
                              Navigator.of(context).pop();
                            },
                            child: const Text("Cancel")),
                        TextButton(
                          onPressed: () {
                            gameProviderModel.restart();
                            Navigator.of(context).pop();
                          },
                          child: const Text("Restart!"),
                        )
                      ],
                    ),
                  );
                },
                child: const Icon(Icons.restart_alt),
              ),
            ],
          ),
          body:
              (gameProviderModel.hand.isEmpty && gameProviderModel.deck.isEmpty)
                  ? _winScreen(gameProviderModel)
                  : Column(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Column(
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              children: [
                                _buildDragTargetDesc1(gameProviderModel),
                                _buildDragTargetDesc2(gameProviderModel),
                              ],
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              children: [
                                _buildDragTargetAsc2(gameProviderModel),
                                _buildDragTargetAsc1(gameProviderModel),
                              ],
                            ),
                          ],
                        ),
                        _buildHand(gameProviderModel),
                      ],
                    ),
          bottomNavigationBar: (_checkGameOver(gameProviderModel))
              ? BottomAppBar(
                  elevation: 5,
                  height: 50.0,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text(
                          "No more available moves. ${(gameProviderModel.deck.length + gameProviderModel.hand.length)} cards left.")
                    ],
                  ),
                )
              : BottomAppBar(
                  elevation: 5,
                  height: 50.0,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      InkWell(
                        onTap: () {
                          gameProviderModel.undo();
                        },
                        child: const Text("Undo"),
                      ),
                      Text("Deck: ${gameProviderModel.deck.length}"),
                      InkWell(
                        onTap: () {
                          if (gameProviderModel.hand.length < 7) {
                            gameProviderModel.draw();
                          } else {
                            {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: const Text(
                                    'You need to play two cards before draw.',
                                    style: TextStyle(fontSize: 20),
                                  ),
                                  duration: const Duration(milliseconds: 2000),
                                  width: double
                                      .maxFinite, // Width of the SnackBar.
                                  padding: const EdgeInsets.symmetric(
                                    horizontal:
                                        8.0, // Inner padding for SnackBar content.
                                  ),
                                  behavior: SnackBarBehavior.floating,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(10.0),
                                  ),
                                ),
                              );
                            }
                          }
                        },
                        child: const Text("Draw cards"),
                      ),
                    ],
                  ),
                ),
        ),
      ),
    );
  }
}

bool _checkCardAsc(int next, int old) {
  return (next > old || old - next == 10);
}

bool _checkCardDesc(int next, int old) {
  return (old > next || next - old == 10);
}

bool _checkGameOver(GameProvider controller) {
  List<bool> playable = <bool>[];
  for (int i = 0; i < controller.hand.length; i++) {
    if ((_checkCardAsc(controller.hand[i].cardNumber, controller.asc1) ||
            _checkCardAsc(controller.hand[i].cardNumber, controller.asc2) ||
            _checkCardDesc(controller.hand[i].cardNumber, controller.desc1) ||
            _checkCardDesc(controller.hand[i].cardNumber, controller.desc2)) ==
        true) {
      // debugPrint(playable.toString());
      playable.add(true);
      break;
    } else {
      // debugPrint(playable.toString());
      playable.add(false);
    }
  }

  if ((playable.every((card) => card == false)) &&
      (controller.hand.length > 6)) {
    return true;
  } else if ((playable.every((card) => card == false)) &&
      (controller.deck.isEmpty && controller.hand.isNotEmpty)) {
    return true;
  } else {
    return false;
  }

  // return ((playable.every((card) => card == false)) &&
  //     (controller.hand.length > 6));
}

Widget _buildDragTargetAsc1(GameProvider controller) {
  return DragTarget<Cards>(
    builder: (
      BuildContext context,
      List<dynamic> accepted,
      List<dynamic> rejected,
    ) {
      return Container(
        decoration: BoxDecoration(
          color: controller.ascColor1,
          border: Border.all(
            width: 2,
          ),
          borderRadius: BorderRadius.circular(4),
          boxShadow: [
            BoxShadow(
              color: controller.ascColor1,
              spreadRadius: 2,
              blurRadius: 4,
              offset: const Offset(0, 0), // changes position of shadow
            ),
          ],
        ),
        margin: const EdgeInsets.all(10),
        height: 150.0,
        width: 120.0,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.arrow_upward),
            Text("${controller.asc1}"),
          ],
        ),
      );
    },
    onAccept: (Cards data) {
      if (_checkCardAsc(data.cardNumber, controller.asc1)) {
        controller.asc1 = data.cardNumber;
        controller.ascColor1 = data.cardColor;
        controller.play(data);
      }
    },
  );
}

Widget _buildDragTargetAsc2(GameProvider controller) {
  return DragTarget<Cards>(
    builder: (
      BuildContext context,
      List<dynamic> accepted,
      List<dynamic> rejected,
    ) {
      return Container(
        decoration: BoxDecoration(
          color: controller.ascColor2,
          border: Border.all(
            width: 2,
          ),
          borderRadius: BorderRadius.circular(4),
          boxShadow: [
            BoxShadow(
              color: controller.ascColor2,
              spreadRadius: 2,
              blurRadius: 4,
              offset: const Offset(0, 0), // changes position of shadow
            ),
          ],
        ),
        margin: const EdgeInsets.all(10),
        height: 150.0,
        width: 120.0,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.arrow_upward),
            Text("${controller.asc2}"),
          ],
        ),
      );
    },
    onAccept: (Cards data) {
      if (_checkCardAsc(data.cardNumber, controller.asc2)) {
        controller.asc2 = data.cardNumber;
        controller.ascColor2 = data.cardColor;
        controller.play(data);
      }
    },
  );
}

Widget _buildDragTargetDesc1(GameProvider controller) {
  return DragTarget<Cards>(
    builder: (
      BuildContext context,
      List<dynamic> accepted,
      List<dynamic> rejected,
    ) {
      return Container(
        decoration: BoxDecoration(
          color: controller.descColor1,
          border: Border.all(
            width: 2,
          ),
          borderRadius: BorderRadius.circular(4),
          boxShadow: [
            BoxShadow(
              color: controller.descColor1,
              spreadRadius: 2,
              blurRadius: 4,
              offset: const Offset(0, 0), // changes position of shadow
            ),
          ],
        ),
        margin: const EdgeInsets.all(10),
        height: 150.0,
        width: 120.0,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.arrow_downward),
            Text("${controller.desc1}"),
          ],
        ),
      );
    },
    onAccept: (Cards data) {
      if (_checkCardDesc(data.cardNumber, controller.desc1)) {
        controller.desc1 = data.cardNumber;
        controller.descColor1 = data.cardColor;
        controller.play(data);
      }
    },
  );
}

Widget _buildDragTargetDesc2(GameProvider controller) {
  return DragTarget<Cards>(
    builder: (
      BuildContext context,
      List<dynamic> accepted,
      List<dynamic> rejected,
    ) {
      return Container(
        decoration: BoxDecoration(
          color: controller.descColor2,
          border: Border.all(
            width: 2,
          ),
          borderRadius: BorderRadius.circular(4),
          boxShadow: [
            BoxShadow(
              color: controller.descColor2,
              spreadRadius: 2,
              blurRadius: 4,
              offset: const Offset(0, 0), // changes position of shadow
            ),
          ],
        ),
        margin: const EdgeInsets.all(10),
        height: 150.0,
        width: 120.0,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.arrow_downward),
            Text("${controller.desc2}"),
          ],
        ),
      );
    },
    onAccept: (Cards data) {
      if (_checkCardDesc(data.cardNumber, controller.desc2)) {
        controller.desc2 = data.cardNumber;
        controller.descColor2 = data.cardColor;
        controller.play(data);
      }
    },
  );
}

Widget _buildHand(GameProvider controller) {
  return GridView.count(
    physics: const NeverScrollableScrollPhysics(),
    crossAxisCount: 4,
    shrinkWrap: true,
    padding: const EdgeInsets.all(10),
    crossAxisSpacing: 5,
    mainAxisSpacing: 5,
    childAspectRatio: 2 / 3,
    children: List.generate(controller.hand.length, (index) {
      return Draggable<Cards>(
        data: controller.hand[index],
        childWhenDragging: Container(),
        feedback: Container(
          decoration: BoxDecoration(
            color: controller.hand[index].cardColor,
            border: Border.all(
              width: 2,
            ),
            borderRadius: BorderRadius.circular(12),
          ),
          margin: const EdgeInsets.all(5.0),
          height: 120,
          width: 80,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Text(
                controller.hand[index].cardNumber.toString(),
                style: const TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.normal,
                  decoration: TextDecoration.none,
                  color: Colors.black,
                ),
              ),
              // Icon(controller.hand[index].cardIcon),
            ],
          ),
        ),
        child: Container(
          decoration: BoxDecoration(
            color: controller.hand[index].cardColor,
            border: Border.all(
              width: 2,
            ),
            borderRadius: BorderRadius.circular(12),
          ),
          margin: const EdgeInsets.all(5.0),
          height: 80,
          width: 45,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Text(
                controller.hand[index].cardNumber.toString(),
                style: const TextStyle(
                  fontSize: 30,
                  decoration: TextDecoration.none,
                  color: Colors.black,
                ),
              ),
              // Icon(controller.hand[index].cardIcon),
            ],
          ),
        ),
      );
    }),
  );
}

Widget _winScreen(GameProvider controller) {
  return Column(
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    crossAxisAlignment: CrossAxisAlignment.center,
    children: [
      const Center(
        child: Text(
          "You did it!",
          style: TextStyle(
            fontSize: 50,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      TextButton(
        style: TextButton.styleFrom(
          textStyle: const TextStyle(fontSize: 30),
        ),
        onPressed: () {
          controller.restart();
        },
        child: const Text('Play again.'),
      )
    ],
  );
}
