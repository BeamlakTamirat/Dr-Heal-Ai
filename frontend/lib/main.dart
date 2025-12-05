import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme/ethereal_theme.dart';
import 'core/router/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  );

  runApp(const ProviderScope(child: DrHealApp()));
}

class DrHealApp extends ConsumerWidget {
  const DrHealApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);

    return MaterialApp.router(
      title: 'Dr.Heal AI',
      debugShowCheckedModeBanner: false,
      theme: EtherealTheme.lightTheme,
      darkTheme: EtherealTheme.lightTheme, // Force light mode for now as per design
      themeMode: ThemeMode.light,
      routerConfig: router,
    );
  }
}
