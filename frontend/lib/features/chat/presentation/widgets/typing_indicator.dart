import 'package:flutter/material.dart';
import '../../../../core/theme/ethereal_theme.dart';
import '../../../../core/widgets/neo_glass_card.dart';

class TypingIndicator extends StatefulWidget {
  final String agentName;

  const TypingIndicator({
    super.key,
    this.agentName = 'Dr. Heal AI',
  });

  @override
  State<TypingIndicator> createState() => _TypingIndicatorState();
}

class _TypingIndicatorState extends State<TypingIndicator>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final agentInfo = _getAgentInfo(widget.agentName);

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Agent Avatar
          Container(
            width: 36,
            height: 36,
            decoration: BoxDecoration(
              color: agentInfo.color,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: agentInfo.color.withValues(alpha: 0.3),
                  blurRadius: 8,
                  spreadRadius: 1,
                ),
              ],
            ),
            child: Icon(
              agentInfo.icon,
              color: Colors.white,
              size: 20,
            ),
          ),
          const SizedBox(width: 12),

          // Typing Bubble
          Flexible(
            child: NeoGlassCard(
              color: Colors.white.withValues(alpha: 0.7),
              borderColor: agentInfo.color.withValues(alpha: 0.2),
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Agent Name
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        agentInfo.icon,
                        size: 14,
                        color: agentInfo.color,
                      ),
                      const SizedBox(width: 6),
                      Text(
                        agentInfo.displayName,
                        style: TextStyle(
                          color: agentInfo.color,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Animated Dots
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: List.generate(3, (index) {
                      return AnimatedBuilder(
                        animation: _controller,
                        builder: (context, child) {
                          final delay = index * 0.2;
                          final value = (_controller.value - delay) % 1.0;
                          final scale = value < 0.5
                              ? 1.0 + (value * 0.6)
                              : 1.3 - ((value - 0.5) * 0.6);

                          return Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 3),
                            child: Transform.scale(
                              scale: scale,
                              child: Container(
                                width: 8,
                                height: 8,
                                decoration: BoxDecoration(
                                  color: agentInfo.color.withValues(
                                    alpha: 0.3 + (scale - 1.0) * 0.7,
                                  ),
                                  shape: BoxShape.circle,
                                ),
                              ),
                            ),
                          );
                        },
                      );
                    }),
                  ),
                  const SizedBox(height: 4),

                  // Status Text
                  Text(
                    'Analyzing your query...',
                    style: TextStyle(
                      color: EtherealTheme.slateBlue.withValues(alpha: 0.7),
                      fontSize: 11,
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ],
              ),
            ),
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
        icon: Icons.analytics_rounded,
        color: EtherealTheme.symptomAnalyzerColor,
      );
    } else if (name.contains('disease')) {
      return _AgentInfo(
        displayName: 'Dr. Disease Expert',
        icon: Icons.science_rounded,
        color: EtherealTheme.diseaseExpertColor,
      );
    } else if (name.contains('treatment')) {
      return _AgentInfo(
        displayName: 'Dr. Treatment Advisor',
        icon: Icons.medication_rounded,
        color: EtherealTheme.treatmentAdvisorColor,
      );
    } else if (name.contains('emergency')) {
      return _AgentInfo(
        displayName: 'Dr. Emergency Triage',
        icon: Icons.emergency_rounded,
        color: EtherealTheme.emergencyTriageColor,
      );
    }

    return _AgentInfo(
      displayName: 'Dr. Heal AI',
      icon: Icons.medical_services_rounded,
      color: EtherealTheme.royalAzure,
    );
  }
}

class _AgentInfo {
  final String displayName;
  final IconData icon;
  final Color color;

  _AgentInfo({
    required this.displayName,
    required this.icon,
    required this.color,
  });
}
