import 'package:equatable/equatable.dart';

class MessageModel extends Equatable {
  final String id;
  final String role;
  final String content;
  final String? agentUsed;
  final DateTime timestamp;

  const MessageModel({
    required this.id,
    required this.role,
    required this.content,
    this.agentUsed,
    required this.timestamp,
  });

  factory MessageModel.fromJson(Map<String, dynamic> json) {
    return MessageModel(
      id: json['id'] as String,
      role: json['role'] as String,
      content: json['content'] as String,
      agentUsed: json['agent_used'] as String?,
      timestamp: DateTime.parse(json['timestamp'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'role': role,
      'content': content,
      'agent_used': agentUsed,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  bool get isUser => role == 'user';
  bool get isAssistant => role == 'assistant';

  @override
  List<Object?> get props => [id, role, content, agentUsed, timestamp];
}
