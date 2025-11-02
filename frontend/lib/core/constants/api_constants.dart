class ApiConstants {
  static const String baseUrl = 'http://localhost:8000';
  
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
