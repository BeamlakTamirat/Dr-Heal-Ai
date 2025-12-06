import 'package:flutter/material.dart';
import '../../../../core/theme/ethereal_theme.dart';

class AgentIdentityHeader extends StatelessWidget {
  final String agentName;

  const AgentIdentityHeader({
    super.key,
    required this.agentName,
  });

  @override
  Widget build(BuildContext context) {
    final agentInfo = _getAgentInfo(agentName);

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            agentInfo.color.withValues(alpha: 0.1),
            agentInfo.color.withValues(alpha: 0.05),
          ],
        ),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: agentInfo.color.withValues(alpha: 0.3),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: agentInfo.color,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: agentInfo.color.withValues(alpha: 0.4),
                  blurRadius: 8,
                  spreadRadius: 1,
                ),
              ],
            ),
            child: Icon(
              agentInfo.icon,
              color: Colors.white,
              size: 16,
            ),
          ),
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                agentInfo.displayName,
                style: const TextStyle(
                  color: EtherealTheme.midnightNavy,
                  fontWeight: FontWeight.bold,
                  fontSize: 13,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                agentInfo.specialty,
                style: TextStyle(
                  color: agentInfo.color,
                  fontSize: 11,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  _AgentInfo _getAgentInfo(String agentName) {
    final name = agentName.toLowerCase();
    
    if (name.contains('symptom')) {
      return _AgentInfo(
        displayName: 'Dr. Symptom Analyzer',
        specialty: 'Symptom Analysis',
        icon: Icons.analytics_rounded,
        color: EtherealTheme.symptomAnalyzerColor,
      );
    } else if (name.contains('disease')) {
      return _AgentInfo(
        displayName: 'Dr. Disease Expert',
        specialty: 'Disease Information',
        icon: Icons.science_rounded,
        color: EtherealTheme.diseaseExpertColor,
      );
    } else if (name.contains('treatment')) {
      return _AgentInfo(
        displayName: 'Dr. Treatment Advisor',
        specialty: 'Treatment Guidance',
        icon: Icons.medication_rounded,
        color: EtherealTheme.treatmentAdvisorColor,
      );
    } else if (name.contains('emergency')) {
      return _AgentInfo(
        displayName: 'Dr. Emergency Triage',
        specialty: 'Emergency Assessment',
        icon: Icons.emergency_rounded,
        color: EtherealTheme.emergencyTriageColor,
      );
    }
    
    // Default
    return _AgentInfo(
      displayName: 'Dr. Heal AI',
      specialty: 'Medical Assistant',
      icon: Icons.medical_services_rounded,
      color: EtherealTheme.royalAzure,
    );
  }
}

class _AgentInfo {
  final String displayName;
  final String specialty;
  final IconData icon;
  final Color color;

  _AgentInfo({
    required this.displayName,
    required this.specialty,
    required this.icon,
    required this.color,
  });
}
