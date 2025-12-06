import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../../../../core/theme/ethereal_theme.dart';
import '../../../../core/widgets/neo_glass_card.dart';
import '../../data/models/message_model.dart';
import 'agent_identity_header.dart';

class EnhancedMessageBubble extends StatelessWidget {
  final MessageModel message;

  const EnhancedMessageBubble({
    super.key,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    final isUser = message.role == 'user';

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!isUser) ...[
            _buildAvatar(context, isUser),
            const SizedBox(width: 12),
          ],
          // Use Flexible for user messages, Expanded for AI messages (wider)
          isUser
              ? Flexible(
                  child: _buildMessageContent(context, isUser),
                )
              : Expanded(
                  child: _buildMessageContent(context, isUser),
                ),
          if (isUser) ...[
            const SizedBox(width: 12),
            _buildAvatar(context, isUser),
          ],
        ],
      ),
    );
  }

  Widget _buildMessageContent(BuildContext context, bool isUser) {
    return Column(
      crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
      children: [
        // Agent Identity Header (only for AI messages)
        if (!isUser && message.agentUsed != null) ...[
          AgentIdentityHeader(agentName: message.agentUsed!),
          const SizedBox(height: 8),
        ],
        
        // Message Content
        NeoGlassCard(
          color: isUser
              ? EtherealTheme.royalAzure.withValues(alpha: 0.15)
              : Colors.white.withValues(alpha: 0.7),
          borderColor: isUser
              ? EtherealTheme.royalAzure.withValues(alpha: 0.3)
              : EtherealTheme.slateBlue.withValues(alpha: 0.2),
          padding: const EdgeInsets.all(16),
          child: isUser
              ? Text(
                  message.content,
                  style: const TextStyle(
                    color: EtherealTheme.midnightNavy,
                    fontSize: 15,
                    height: 1.5,
                  ),
                )
              : MarkdownBody(
                  data: message.content,
                  styleSheet: MarkdownStyleSheet(
                    p: const TextStyle(
                      color: EtherealTheme.midnightNavy,
                      fontSize: 15,
                      height: 1.6,
                    ),
                    h1: const TextStyle(
                      color: EtherealTheme.midnightNavy,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      height: 1.4,
                    ),
                    h2: const TextStyle(
                      color: EtherealTheme.midnightNavy,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      height: 1.4,
                    ),
                    h3: const TextStyle(
                      color: EtherealTheme.royalAzure,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      height: 1.4,
                    ),
                    strong: const TextStyle(
                      color: EtherealTheme.midnightNavy,
                      fontWeight: FontWeight.bold,
                    ),
                    em: TextStyle(
                      color: EtherealTheme.slateBlue,
                      fontStyle: FontStyle.italic,
                    ),
                    listBullet: const TextStyle(
                      color: EtherealTheme.royalAzure,
                      fontSize: 15,
                    ),
                    code: TextStyle(
                      backgroundColor: EtherealTheme.royalAzure.withValues(alpha: 0.1),
                      color: EtherealTheme.deepIndigo,
                      fontFamily: 'monospace',
                      fontSize: 14,
                    ),
                    blockquote: TextStyle(
                      color: EtherealTheme.slateBlue,
                      fontStyle: FontStyle.italic,
                    ),
                    blockquoteDecoration: BoxDecoration(
                      color: EtherealTheme.royalAzure.withValues(alpha: 0.05),
                      borderRadius: BorderRadius.circular(8),
                      border: Border(
                        left: BorderSide(
                          color: EtherealTheme.royalAzure,
                          width: 3,
                        ),
                      ),
                    ),
                  ),
                ),
        ),
        
        // Timestamp
        Padding(
          padding: const EdgeInsets.only(top: 4, left: 8, right: 8),
          child: Text(
            _formatTime(message.timestamp),
            style: TextStyle(
              color: EtherealTheme.slateBlue.withValues(alpha: 0.6),
              fontSize: 11,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildAvatar(BuildContext context, bool isUser) {
    if (isUser) {
      return Container(
        width: 36,
        height: 36,
        decoration: BoxDecoration(
          gradient: EtherealTheme.primaryGradient,
          shape: BoxShape.circle,
          boxShadow: [
            BoxShadow(
              color: EtherealTheme.royalAzure.withValues(alpha: 0.3),
              blurRadius: 8,
              spreadRadius: 1,
            ),
          ],
        ),
        child: const Icon(
          Icons.person_rounded,
          color: Colors.white,
          size: 20,
        ),
      );
    }

    // AI Avatar
    final agentColor = _getAgentColor(message.agentUsed);
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        color: agentColor,
        shape: BoxShape.circle,
        boxShadow: [
          BoxShadow(
            color: agentColor.withValues(alpha: 0.3),
            blurRadius: 8,
            spreadRadius: 1,
          ),
        ],
      ),
      child: Icon(
        _getAgentIcon(message.agentUsed),
        color: Colors.white,
        size: 20,
      ),
    );
  }

  Color _getAgentColor(String? agentName) {
    if (agentName == null) return EtherealTheme.royalAzure;
    final name = agentName.toLowerCase();
    
    if (name.contains('symptom')) return EtherealTheme.symptomAnalyzerColor;
    if (name.contains('disease')) return EtherealTheme.diseaseExpertColor;
    if (name.contains('treatment')) return EtherealTheme.treatmentAdvisorColor;
    if (name.contains('emergency')) return EtherealTheme.emergencyTriageColor;
    
    return EtherealTheme.royalAzure;
  }

  IconData _getAgentIcon(String? agentName) {
    if (agentName == null) return Icons.medical_services_rounded;
    final name = agentName.toLowerCase();
    
    if (name.contains('symptom')) return Icons.analytics_rounded;
    if (name.contains('disease')) return Icons.science_rounded;
    if (name.contains('treatment')) return Icons.medication_rounded;
    if (name.contains('emergency')) return Icons.emergency_rounded;
    
    return Icons.medical_services_rounded;
  }

  String _formatTime(DateTime timestamp) {
    final hour = timestamp.hour.toString().padLeft(2, '0');
    final minute = timestamp.minute.toString().padLeft(2, '0');
    return '$hour:$minute';
  }
}
