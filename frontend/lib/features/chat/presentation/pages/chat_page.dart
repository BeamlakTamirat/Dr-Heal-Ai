import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_theme.dart';
import '../../../../core/widgets/animated_background.dart';
import '../../../../core/widgets/agent_badge.dart';
import '../../../../core/widgets/message_bubble.dart';
import '../../../../core/widgets/chat_input.dart';
import '../providers/chat_provider.dart';

class ChatPage extends ConsumerStatefulWidget {
  final String? conversationId;

  const ChatPage({super.key, this.conversationId});

  @override
  ConsumerState<ChatPage> createState() => _ChatPageState();
}

class _ChatPageState extends ConsumerState<ChatPage> {
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();

    // Load existing conversation if ID provided
    if (widget.conversationId != null) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        ref
            .read(chatProvider.notifier)
            .loadConversation(widget.conversationId!);
      });
    }
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      Future.delayed(const Duration(milliseconds: 300), () {
        if (_scrollController.hasClients) {
          _scrollController.animateTo(
            _scrollController.position.maxScrollExtent,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeOut,
          );
        }
      });
    }
  }

  Future<void> _handleSendMessage(String message) async {
    try {
      await ref.read(chatProvider.notifier).sendMessage(message);
      _scrollToBottom();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to send message: ${e.toString()}'),
            backgroundColor: AppTheme.danger,
            action: SnackBarAction(
              label: 'Retry',
              textColor: Colors.white,
              onPressed: () => _handleSendMessage(message),
            ),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final chatState = ref.watch(chatProvider);

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () => context.pop(),
        ),
        title: const Text('Dr.Heal AI'),
        centerTitle: true,
        actions: [
          if (chatState.currentConversationId != null)
            IconButton(
              icon: const Icon(Icons.more_vert_rounded),
              onPressed: () {
                // Show options menu
              },
            ),
        ],
      ),
      body: AnimatedBackground(
        child: Column(
          children: [
            // Agent Badge (floating)
            if (chatState.currentAgent != null)
              Padding(
                padding: const EdgeInsets.all(16),
                child: AgentBadge(
                  agentName: chatState.currentAgent,
                  isActive: chatState.isLoading,
                  size: 56,
                ),
              ),

            // Messages List
            Expanded(
              child: chatState.messages.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.chat_bubble_outline,
                            size: 80,
                            color:
                                Theme.of(context).brightness == Brightness.dark
                                ? Colors.white24
                                : Colors.black26,
                          ),
                          const SizedBox(height: 24),
                          Text(
                            'Start a conversation',
                            style: Theme.of(context).textTheme.displayMedium
                                ?.copyWith(
                                  color:
                                      Theme.of(context).brightness ==
                                          Brightness.dark
                                      ? Colors.white54
                                      : Colors.black54,
                                ),
                          ),
                          const SizedBox(height: 8),
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 48),
                            child: Text(
                              'Describe your symptoms and our AI agents will assist you',
                              textAlign: TextAlign.center,
                              style: Theme.of(context).textTheme.bodyMedium
                                  ?.copyWith(
                                    color:
                                        Theme.of(context).brightness ==
                                            Brightness.dark
                                        ? Colors.white38
                                        : Colors.black38,
                                  ),
                            ),
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      controller: _scrollController,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                      itemCount: chatState.messages.length,
                      itemBuilder: (context, index) {
                        final message = chatState.messages[index];
                        return MessageBubble(message: message, showAgent: true);
                      },
                    ),
            ),

            // Error Display
            if (chatState.error != null)
              Container(
                padding: const EdgeInsets.all(16),
                color: AppTheme.danger.withValues(alpha: 0.1),
                child: Row(
                  children: [
                    const Icon(Icons.error_outline, color: AppTheme.danger),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        chatState.error!,
                        style: const TextStyle(color: AppTheme.danger),
                      ),
                    ),
                    TextButton(
                      onPressed: () {
                        // Retry last message
                      },
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),

            // Chat Input
            ChatInput(
              onSend: _handleSendMessage,
              isLoading: chatState.isLoading,
            ),
          ],
        ),
      ),
    );
  }
}
