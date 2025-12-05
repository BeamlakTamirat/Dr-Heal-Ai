import 'package:dio/dio.dart';
import '../../../../core/network/dio_client.dart';
import '../../../../core/constants/api_constants.dart';
import '../models/chat_response.dart';
import '../models/conversation_model.dart';

class ChatService {
  final DioClient _dioClient;

  ChatService(this._dioClient);

  Future<ChatResponse> sendMessage({
    required String query,
    String? conversationId,
  }) async {
    try {
      print('🔵 [CHAT] Sending message to: ${ApiConstants.chat}');
      print('🔵 [CHAT] Query: $query');
      print('🔵 [CHAT] ConversationId: $conversationId');
      
      final response = await _dioClient.dio.post(
        ApiConstants.chat,
        data: {
          'query': query,
          if (conversationId != null) 'conversation_id': conversationId,
        },
      );

      print('🟢 [CHAT] Response: ${response.data}');
      return ChatResponse.fromJson(response.data);
    } on DioException catch (e) {
      print('🔴 [CHAT] DioException: ${e.type}');
      print('🔴 [CHAT] Response data: ${e.response?.data}');
      print('🔴 [CHAT] Status code: ${e.response?.statusCode}');
      throw _handleError(e);
    }
  }

  Future<List<ConversationModel>> getConversations({
    int limit = 50,
    int offset = 0,
  }) async {
    try {
      final response = await _dioClient.dio.get(
        ApiConstants.conversations,
        queryParameters: {
          'limit': limit,
          'offset': offset,
        },
      );

      return (response.data as List)
          .map((json) => ConversationModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<ConversationDetailModel> getConversation(String conversationId) async {
    try {
      final response = await _dioClient.dio.get(
        '${ApiConstants.conversations}/$conversationId',
      );

      return ConversationDetailModel.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<void> deleteConversation(String conversationId) async {
    try {
      await _dioClient.dio.delete(
        '${ApiConstants.conversations}/$conversationId',
      );
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  String _handleError(DioException error) {
    if (error.response != null) {
      final data = error.response!.data;
      if (data is Map<String, dynamic> && data.containsKey('detail')) {
        return data['detail'] as String;
      }
      return 'Server error: ${error.response!.statusCode}';
    }

    if (error.type == DioExceptionType.connectionTimeout ||
        error.type == DioExceptionType.receiveTimeout) {
      return 'Connection timeout. Please check your internet connection.';
    }

    if (error.type == DioExceptionType.connectionError) {
      return 'No internet connection. Please check your network.';
    }

    return 'An unexpected error occurred. Please try again.';
  }
}
