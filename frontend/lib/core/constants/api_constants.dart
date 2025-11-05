import 'dart:io';

class ApiConstants {
  // Auto-detect the correct base URL
  static String get baseUrl {
    if (Platform.isAndroid) {
      return 'http://192.168.1.100:8000'; // CHANGE THIS TO YOUR IP
    } else if (Platform.isIOS) {
      return 'http://localhost:8000';
    } else {
      return 'http://localhost:8000';
    }
  }
  
  // Auth Endpoints
  static const String login = '/api/auth/login';
  static const String register = '/api/auth/register';
  static const String me = '/api/auth/me';
  
  // Conversation Endpoints
  static const String conversations = '/api/conversations';
  static const String chat = '/api/conversations/chat';
  
  // Medical History Endpoints
  static const String medicalHistory = '/api/medical-history';
}
