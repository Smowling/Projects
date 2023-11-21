import 'package:flutter/material.dart';
import 'package:Order98/game_provider.dart';
import 'package:Order98/menu_screen.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context)=>GameProvider()),
      ],
      child: MaterialApp(
        title: 'Order 98',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromARGB(172, 255, 255, 255)),
          useMaterial3: true,
        ),
        home: const MenuScreen(),
      ),
    );
  }
}