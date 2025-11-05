class ChatResponse {
  final String conversationId;
  final String messageId;
  final String response;
  final String agentUsed;

  const ChatResponse({
    required this.conversationId,
    required this.messageId,
    required this.response,
    required this.agentUsed,
  });

  factory ChatResponse.fromJson(Map<String, dynamic> json) {
    return ChatResponse(
      conversationId: json['conversation_id'] as String,
      messageId: json['message_id'] as String,
      response: json['response'] as String,
      agentUsed: json['agent_used'] as String,
    );
  }
}
