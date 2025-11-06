import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../theme/app_theme.dart';

enum AgentType {
  symptomAnalyzer,
  diseaseExpert,
  treatmentAdvisor,
  emergencyTriage,
  unknown,
}

class AgentBadge extends StatelessWidget {
  final String? agentName;
  final bool isActive;
  final double size;

  const AgentBadge({
    super.key,
    this.agentName,
    this.isActive = false,
    this.size = 48,
  });

  AgentType _getAgentType() {
    if (agentName == null) return AgentType.unknown;

    final name = agentName!.toLowerCase();
    if (name.contains('symptom')) return AgentType.symptomAnalyzer;
    if (name.contains('disease')) return AgentType.diseaseExpert;
    if (name.contains('treatment')) return AgentType.treatmentAdvisor;
    if (name.contains('emergency')) return AgentType.emergencyTriage;
    return AgentType.unknown;
  }

  Color _getAgentColor() {
    switch (_getAgentType()) {
      case AgentType.symptomAnalyzer:
        return AppTheme.symptomAnalyzer;
      case AgentType.diseaseExpert:
        return AppTheme.diseaseExpert;
      case AgentType.treatmentAdvisor:
        return AppTheme.treatmentAdvisor;
      case AgentType.emergencyTriage:
        return AppTheme.emergencyTriage;
      case AgentType.unknown:
        return AppTheme.primary;
    }
  }

  IconData _getAgentIcon() {
    switch (_getAgentType()) {
      case AgentType.symptomAnalyzer:
        return Icons.medical_information_outlined;
      case AgentType.diseaseExpert:
        return Icons.science_outlined;
      case AgentType.treatmentAdvisor:
        return Icons.medication_outlined;
      case AgentType.emergencyTriage:
        return Icons.emergency_outlined;
      case AgentType.unknown:
        return Icons.smart_toy_outlined;
    }
  }

  String _getAgentLabel() {
    switch (_getAgentType()) {
      case AgentType.symptomAnalyzer:
        return 'Symptom Analyzer';
      case AgentType.diseaseExpert:
        return 'Disease Expert';
      case AgentType.treatmentAdvisor:
        return 'Treatment Advisor';
      case AgentType.emergencyTriage:
        return 'Emergency Triage';
      case AgentType.unknown:
        return 'AI Assistant';
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = _getAgentColor();
    final icon = _getAgentIcon();
    final label = _getAgentLabel();

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
              width: size,
              height: size,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: [color, color.withOpacity(0.7)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                boxShadow: [
                  BoxShadow(
                    color: color.withOpacity(0.4),
                    blurRadius: 20,
                    spreadRadius: isActive ? 4 : 0,
                  ),
                ],
              ),
              child: Icon(icon, color: Colors.white, size: size * 0.5),
            )
            .animate(onPlay: (controller) => controller.repeat())
            .shimmer(duration: 2000.ms, color: Colors.white.withOpacity(0.3))
            .then()
            .scale(
              duration: 1000.ms,
              begin: const Offset(1, 1),
              end: const Offset(1.05, 1.05),
              curve: Curves.easeInOut,
            )
            .then()
            .scale(
              duration: 1000.ms,
              begin: const Offset(1.05, 1.05),
              end: const Offset(1, 1),
              curve: Curves.easeInOut,
            ),
        if (isActive) ...[
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(
              color: color.withOpacity(0.2),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: color.withOpacity(0.4), width: 1),
            ),
            child: Text(
              label,
              style: TextStyle(
                color: color,
                fontSize: 12,
                fontWeight: FontWeight.w600,
              ),
            ),
          ).animate().fadeIn(duration: 300.ms).slideY(begin: -0.2, end: 0),
        ],
      ],
    );
  }
}
