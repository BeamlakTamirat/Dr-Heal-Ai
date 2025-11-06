import 'dart:io';

class ApiConstants {
  // Production URL from Railway (update after deployment)
  static const String _productionUrl = 'https://dr-heal-ai-production.up.railway.app';
  
  // Auto-detect the correct base URL
  static String get baseUrl {
    if (Platform.isAndroid || Platform.isIOS) {
      // Use production URL for mobile devices
      // TODO: Update this URL after Railway deployment
      return _productionUrl;
    } else {
      // Use localhost for desktop/web development
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
