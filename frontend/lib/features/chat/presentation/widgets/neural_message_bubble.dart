import 'package:flutter/material.dart';
import '../../../../core/theme/ethereal_theme.dart';
import '../../../../core/widgets/neo_glass_card.dart';
import '../../data/models/message_model.dart';
import 'agent_avatar.dart';

class NeuralMessageBubble extends StatelessWidget {
  final MessageModel message;
  final bool showAgent;

  const NeuralMessageBubble({
    super.key,
    required this.message,
    this.showAgent = true,
  });

  @override
  Widget build(BuildContext context) {
    final isUser = message.role == 'user';
    final agentId = message.agentUsed ?? 'symptom_analyzer';

    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment:
            isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!isUser && showAgent) ...[
            AgentAvatar(agentId: agentId, size: 32),
            const SizedBox(width: 12),
          ],
          if (isUser) const SizedBox(width: 40),
          
          Flexible(
            child: NeoGlassCard(
              padding: const EdgeInsets.all(16),
              borderRadius: 20,
              color: isUser 
                  ? EtherealTheme.royalAzure.withValues(alpha: 0.15)
                  : EtherealTheme.crystallineWhite.withValues(alpha: 0.6),
              borderColor: isUser
                  ? EtherealTheme.royalAzure.withValues(alpha: 0.3)
                  : EtherealTheme.glassBorder,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (!isUser)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 4),
                      child: Text(
                        _getAgentName(agentId),
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          color: _getAgentColor(agentId),
                          letterSpacing: 0.5,
                        ),
                      ),
                    ),
                  Text(
                    message.content,
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: EtherealTheme.midnightNavy,
                    ),
                  ),
                ],
              ),
            ),
          ),
          
          if (!isUser) const SizedBox(width: 40),
        ],
      ),
    );
  }

  String _getAgentName(String id) {
    switch (id) {
      case 'symptom_analyzer': return 'SYMPTOM ANALYZER';
      case 'disease_expert': return 'DISEASE EXPERT';
      case 'treatment_advisor': return 'TREATMENT ADVISOR';
      case 'emergency_triage': return 'EMERGENCY TRIAGE';
      default: return 'DR. HEAL AI';
    }
  }

  Color _getAgentColor(String id) {
    switch (id) {
      case 'symptom_analyzer': return EtherealTheme.symptomAnalyzerColor;
      case 'disease_expert': return EtherealTheme.diseaseExpertColor;
      case 'treatment_advisor': return EtherealTheme.treatmentAdvisorColor;
      case 'emergency_triage': return EtherealTheme.emergencyTriageColor;
      default: return EtherealTheme.royalAzure;
    }
  }
}
