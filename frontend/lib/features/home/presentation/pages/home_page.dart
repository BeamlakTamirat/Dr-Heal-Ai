import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/ethereal_theme.dart';
import '../../../../core/widgets/particle_background.dart';
import '../../../../core/widgets/neo_glass_card.dart';
import '../widgets/bio_status_widget.dart';
import '../widgets/agent_grid_widget.dart';
import '../../../auth/presentation/providers/auth_provider.dart';

class HomePage extends ConsumerStatefulWidget {
  const HomePage({super.key});

  @override
  ConsumerState<HomePage> createState() => _HomePageState();
}

class _HomePageState extends ConsumerState<HomePage> {
  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);

    return Scaffold(
      body: ParticleBackground(
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'WELCOME BACK',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: EtherealTheme.royalAzure,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1.5,
                          ),
                        ),
                        Text(
                          authState.value?.name ?? 'Patient',
                          style: Theme.of(context).textTheme.displayLarge,
                        ),
                      ],
                    ),
                    NeoGlassCard(
                      onTap: () async {
                        await ref.read(authProvider.notifier).logout();
                        if (context.mounted) {
                          context.go('/login');
                        }
                      },
                      padding: const EdgeInsets.all(12),
                      borderRadius: 12,
                      child: const Icon(
                        Icons.logout_rounded,
                        color: EtherealTheme.royalAzure,
                      ),
                    ),
                  ],
                ),
                
                const SizedBox(height: 32),
                
                // Bio Status
                const BioStatusWidget(),
                
                const SizedBox(height: 32),
                
                // Agents Grid
                const AgentGridWidget(),
                
                const SizedBox(height: 32),
                
                // Active Sessions / History
                Text(
                  "ACTIVE SESSIONS",
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.2,
                  ),
                ),
                const SizedBox(height: 16),
                _buildSessionCard(context),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSessionCard(BuildContext context) {
    return NeoGlassCard(
      onTap: () => context.push('/conversations'),
      padding: const EdgeInsets.all(20),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: EtherealTheme.royalAzure.withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: const Icon(
              Icons.chat_bubble_outline_rounded,
              color: EtherealTheme.royalAzure,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  "Recent Consultation",
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                    color: EtherealTheme.midnightNavy,
                  ),
                ),
                Text(
                  "Tap to view history",
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ],
            ),
          ),
          const Icon(
            Icons.arrow_forward_ios_rounded,
            size: 16,
            color: EtherealTheme.slateBlue,
          ),
        ],
      ),
    );
  }
}
