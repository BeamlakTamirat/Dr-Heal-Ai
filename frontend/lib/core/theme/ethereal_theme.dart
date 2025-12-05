import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class EtherealTheme {
  // Divine Blue Palette
  static const royalAzure = Color(0xFF2563EB);
  static const electricSky = Color(0xFF3B82F6);
  static const deepIndigo = Color(0xFF4F46E5);
  static const softViolet = Color(0xFF818CF8);
  
  // Backgrounds
  static const paleAliceBlue = Color(0xFFF0F9FF);
  static const deepSpaceBlue = Color(0xFF050A14); // For dark mode fallback

  // Surfaces
  static const crystallineWhite = Color(0xFFFFFFFF);
  static const glassBorder = Color(0x33FFFFFF);
  
  // Text
  static const midnightNavy = Color(0xFF0F172A);
  static const slateBlue = Color(0xFF475569);

  // Agent Colors
  static const symptomAnalyzerColor = Color(0xFF3B82F6); // Electric Blue
  static const diseaseExpertColor = Color(0xFF7C3AED); // Deep Violet
  static const treatmentAdvisorColor = Color(0xFF10B981); // Emerald Green
  static const emergencyTriageColor = Color(0xFFEF4444); // Urgent Red

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: paleAliceBlue,
      
      // Color Scheme
      colorScheme: const ColorScheme.light(
        primary: royalAzure,
        secondary: deepIndigo,
        surface: Colors.transparent, // Important for glassmorphism
        error: emergencyTriageColor,
        onPrimary: Colors.white,
        onSurface: midnightNavy,
      ),

      // Typography
      textTheme: GoogleFonts.outfitTextTheme(
        const TextTheme(
          displayLarge: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.w700,
            color: midnightNavy,
            letterSpacing: -0.5,
          ),
          displayMedium: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.w600,
            color: midnightNavy,
            letterSpacing: -0.5,
          ),
          bodyLarge: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w400,
            color: slateBlue,
            height: 1.5,
          ),
          bodyMedium: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w400,
            color: slateBlue,
          ),
        ),
      ),

      // Component Themes
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        iconTheme: IconThemeData(color: midnightNavy),
        titleTextStyle: TextStyle(
          color: midnightNavy,
          fontSize: 20,
          fontWeight: FontWeight.w600,
          fontFamily: 'Outfit',
        ),
      ),
    );
  }

  // Gradients
  static const primaryGradient = LinearGradient(
    colors: [royalAzure, electricSky],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const glassGradient = LinearGradient(
    colors: [
      Color(0x99FFFFFF), // 60% opacity
      Color(0x66FFFFFF), // 40% opacity
    ],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
