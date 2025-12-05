import 'package:flutter/material.dart';
import '../../../../core/theme/ethereal_theme.dart';

class AgentAvatar extends StatelessWidget {
  final String agentId;
  final double size;

  const AgentAvatar({
    super.key,
    required this.agentId,
    this.size = 40,
  });

  @override
  Widget build(BuildContext context) {
    final agentData = _getAgentData(agentId);
    
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: agentData.color.withValues(alpha: 0.1),
        shape: BoxShape.circle,
        border: Border.all(
          color: agentData.color.withValues(alpha: 0.5),
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: agentData.color.withValues(alpha: 0.2),
            blurRadius: 10,
            spreadRadius: 2,
          ),
        ],
      ),
      child: Icon(
        agentData.icon,
        color: agentData.color,
        size: size * 0.6,
      ),
    );
  }

  ({Color color, IconData icon}) _getAgentData(String id) {
    switch (id) {
      case 'symptom_analyzer':
        return (
          color: EtherealTheme.symptomAnalyzerColor,
          icon: Icons.remove_red_eye_rounded,
        );
      case 'disease_expert':
        return (
          color: EtherealTheme.diseaseExpertColor,
          icon: Icons.psychology_rounded,
        );
      case 'treatment_advisor':
        return (
          color: EtherealTheme.treatmentAdvisorColor,
          icon: Icons.spa_rounded,
        );
      case 'emergency_triage':
        return (
          color: EtherealTheme.emergencyTriageColor,
          icon: Icons.warning_rounded,
        );
      default:
        return (
          color: EtherealTheme.royalAzure,
          icon: Icons.medical_services_rounded,
        );
    }
  }
}
