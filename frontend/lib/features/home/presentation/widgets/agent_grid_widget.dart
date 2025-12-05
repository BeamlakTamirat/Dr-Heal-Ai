import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/ethereal_theme.dart';
import '../../../../core/widgets/neo_glass_card.dart';

class AgentGridWidget extends StatelessWidget {
  const AgentGridWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          "AI SPECIALISTS",
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            fontWeight: FontWeight.bold,
            letterSpacing: 1.2,
          ),
        ),
        const SizedBox(height: 16),
        GridView.count(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisCount: 2,
          mainAxisSpacing: 16,
          crossAxisSpacing: 16,
          childAspectRatio: 1.1,
          children: [
            _buildAgentCard(
              context,
              "Dr. Heal",
              "General",
              Icons.medical_services_rounded,
              EtherealTheme.royalAzure,
              "symptom_analyzer",
            ),
            _buildAgentCard(
              context,
              "Cardio",
              "Heart",
              Icons.favorite_rounded,
              EtherealTheme.emergencyTriageColor,
              "emergency_triage",
            ),
            _buildAgentCard(
              context,
              "Neuro",
              "Brain",
              Icons.psychology_rounded,
              EtherealTheme.diseaseExpertColor,
              "disease_expert",
            ),
            _buildAgentCard(
              context,
              "Wellness",
              "Care",
              Icons.spa_rounded,
              EtherealTheme.treatmentAdvisorColor,
              "treatment_advisor",
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildAgentCard(
    BuildContext context,
    String name,
    String role,
    IconData icon,
    Color color,
    String agentId,
  ) {
    return NeoGlassCard(
      onTap: () {
        // Navigate to chat with specific agent context if needed
        // For now, just open chat
        context.push('/chat'); 
      },
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: color, size: 32),
          ),
          const SizedBox(height: 12),
          Text(
            name,
            style: const TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 16,
              color: EtherealTheme.midnightNavy,
            ),
          ),
          Text(
            role,
            style: const TextStyle(
              fontSize: 12,
              color: EtherealTheme.slateBlue,
            ),
          ),
        ],
      ),
    );
  }
}
