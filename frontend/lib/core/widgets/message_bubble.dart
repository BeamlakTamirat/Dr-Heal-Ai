import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:intl/intl.dart';
import '../theme/app_theme.dart';
import '../../features/chat/data/models/message_model.dart';

class MessageBubble extends StatelessWidget {
  final MessageModel message;
  final bool showAgent;

  const MessageBubble({
    super.key,
    required this.message,
    this.showAgent = true,
  });

  Color _getAgentColor() {
    if (message.agentUsed == null) return AppTheme.primary;

    final agent = message.agentUsed!.toLowerCase();
    if (agent.contains('symptom')) return AppTheme.symptomAnalyzer;
    if (agent.contains('disease')) return AppTheme.diseaseExpert;
    if (agent.contains('treatment')) return AppTheme.treatmentAdvisor;
    if (agent.contains('emergency')) return AppTheme.emergencyTriage;
    return AppTheme.primary;
  }

  String _formatTime(DateTime time) {
    return DateFormat('HH:mm').format(time);
  }

  @override
  Widget build(BuildContext context) {
    final isUser = message.isUser;
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final agentColor = _getAgentColor();

    return Padding(
      padding: EdgeInsets.only(
        left: isUser ? 48 : 0,
        right: isUser ? 0 : 48,
        bottom: 16,
      ),
      child: Column(
        crossAxisAlignment: isUser
            ? CrossAxisAlignment.end
            : CrossAxisAlignment.start,
        children: [
          // Agent indicator for AI messages
          if (!isUser && showAgent && message.agentUsed != null) ...[
            Padding(
              padding: const EdgeInsets.only(left: 12, bottom: 8),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    width: 8,
                    height: 8,
                    decoration: BoxDecoration(
                      color: agentColor,
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    message.agentUsed!,
                    style: TextStyle(
                      color: agentColor,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
          ],

          // Message bubble
          GestureDetector(
                onLongPress: () {
                  Clipboard.setData(ClipboardData(text: message.content));
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: const Text('Message copied to clipboard'),
                      duration: const Duration(seconds: 2),
                      behavior: SnackBarBehavior.floating,
                      backgroundColor: agentColor,
                    ),
                  );
                },
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: isUser
                        ? AppTheme.primaryGradient
                        : LinearGradient(
                            colors: [
                              isDark
                                  ? AppTheme.darkGlassBackground
                                  : AppTheme.lightGlassBackground,
                              isDark
                                  ? AppTheme.darkGlassBackground
                                  : AppTheme.lightGlassBackground,
                            ],
                          ),
                    borderRadius: BorderRadius.only(
                      topLeft: const Radius.circular(20),
                      topRight: const Radius.circular(20),
                      bottomLeft: Radius.circular(isUser ? 20 : 4),
                      bottomRight: Radius.circular(isUser ? 4 : 20),
                    ),
                    border: Border.all(
                      color: isUser
                          ? Colors.transparent
                          : (isDark
                                ? AppTheme.darkGlassBorder
                                : AppTheme.lightGlassBorder),
                      width: 1.5,
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: isUser
                            ? AppTheme.primary.withOpacity(0.3)
                            : (isDark ? Colors.black26 : Colors.black12),
                        blurRadius: 12,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        message.content,
                        style: TextStyle(
                          color: isUser
                              ? Colors.white
                              : (isDark
                                    ? Colors.white
                                    : const Color(0xFF0F172A)),
                          fontSize: 15,
                          height: 1.5,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            _formatTime(message.timestamp),
                            style: TextStyle(
                              color: isUser
                                  ? Colors.white70
                                  : (isDark ? Colors.white54 : Colors.black54),
                              fontSize: 11,
                            ),
                          ),
                          if (isUser) ...[
                            const SizedBox(width: 4),
                            Icon(Icons.check, size: 14, color: Colors.white70),
                          ],
                        ],
                      ),
                    ],
                  ),
                ),
              )
              .animate()
              .fadeIn(duration: 300.ms)
              .slideY(begin: 0.3, end: 0, curve: Curves.easeOutCubic),
        ],
      ),
    );
  }
}
