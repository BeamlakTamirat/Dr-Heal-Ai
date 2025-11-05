import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/providers/dio_provider.dart';
import '../../data/models/message_model.dart';
import '../../data/models/conversation_model.dart';
import '../../data/services/chat_service.dart';

final chatServiceProvider = Provider<ChatService>((ref) {
  final dioClient = ref.watch(dioClientProvider);
  return ChatService(dioClient);
});

class ChatState {
  final String? currentConversationId;
  final List<MessageModel> messages;
  final bool isLoading;
  final String? error;
  final String? currentAgent;

  const ChatState({
    this.currentConversationId,
    this.messages = const [],
    this.isLoading = false,
    this.error,
    this.currentAgent,
  });

  ChatState copyWith({
    String? currentConversationId,
    List<MessageModel>? messages,
    bool? isLoading,
    String? error,
    String? currentAgent,
  }) {
    return ChatState(
      currentConversationId: currentConversationId ?? this.currentConversationId,
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      currentAgent: currentAgent ?? this.currentAgent,
    );
  }
}

class ChatNotifier extends StateNotifier<ChatState> {
  final ChatService _chatService;

  ChatNotifier(this._chatService) : super(const ChatState());

  Future<void> sendMessage(String query) async {
    final userMessage = MessageModel(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      role: 'user',
      content: query,
      timestamp: DateTime.now(),
    );

    state = state.copyWith(
      messages: [...state.messages, userMessage],
      isLoading: true,
      error: null,
    );

    try {
      final response = await _chatService.sendMessage(
        query: query,
        conversationId: state.currentConversationId,
      );

      final aiMessage = MessageModel(
        id: response.messageId,
        role: 'assistant',
        content: response.response,
        agentUsed: response.agentUsed,
        timestamp: DateTime.now(),
      );

      state = state.copyWith(
        currentConversationId: response.conversationId,
        messages: [...state.messages, aiMessage],
        isLoading: false,
        currentAgent: response.agentUsed,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
      rethrow;
    }
  }

  Future<void> loadConversation(String conversationId) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final conversation = await _chatService.getConversation(conversationId);

      state = state.copyWith(
        currentConversationId: conversation.id,
        messages: conversation.messages,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
      rethrow;
    }
  }

  void startNewConversation() {
    state = const ChatState();
  }
}

final chatProvider = StateNotifierProvider<ChatNotifier, ChatState>((ref) {
  final chatService = ref.watch(chatServiceProvider);
  return ChatNotifier(chatService);
});

final conversationsProvider = FutureProvider<List<ConversationModel>>((ref) async {
  final chatService = ref.watch(chatServiceProvider);
  return await chatService.getConversations();
});
