import 'package:flutter/material.dart';
import '../../../../core/theme/ethereal_theme.dart';
import '../../../../core/widgets/neo_glass_card.dart';

class NeuralChatInput extends StatefulWidget {
  final Function(String) onSend;
  final bool isLoading;

  const NeuralChatInput({
    super.key,
    required this.onSend,
    this.isLoading = false,
  });

  @override
  State<NeuralChatInput> createState() => _NeuralChatInputState();
}

class _NeuralChatInputState extends State<NeuralChatInput> {
  final _controller = TextEditingController();
  final _focusNode = FocusNode();
  bool _isFocused = false;

  @override
  void initState() {
    super.initState();
    _focusNode.addListener(() {
      setState(() {
        _isFocused = _focusNode.hasFocus;
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  void _handleSend() {
    if (_controller.text.trim().isEmpty) return;
    widget.onSend(_controller.text.trim());
    _controller.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: NeoGlassCard(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        borderRadius: 30,
        color: _isFocused
            ? EtherealTheme.crystallineWhite.withValues(alpha: 0.9)
            : EtherealTheme.crystallineWhite.withValues(alpha: 0.6),
        borderColor: _isFocused
            ? EtherealTheme.royalAzure.withValues(alpha: 0.5)
            : EtherealTheme.glassBorder,
        child: Row(
          children: [
            // Neural Pulse Icon (Animated when loading)
            AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: widget.isLoading
                    ? EtherealTheme.royalAzure.withValues(alpha: 0.1)
                    : Colors.transparent,
                shape: BoxShape.circle,
              ),
              child: widget.isLoading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: EtherealTheme.royalAzure,
                      ),
                    )
                  : const Icon(
                      Icons.auto_awesome_rounded,
                      color: EtherealTheme.royalAzure,
                      size: 20,
                    ),
            ),
            
            const SizedBox(width: 12),
            
            // Text Field
            Expanded(
              child: TextField(
                controller: _controller,
                focusNode: _focusNode,
                style: const TextStyle(
                  color: EtherealTheme.midnightNavy,
                  fontSize: 16,
                ),
                decoration: const InputDecoration(
                  hintText: "Describe your symptoms...",
                  hintStyle: TextStyle(
                    color: EtherealTheme.slateBlue,
                    fontSize: 14,
                  ),
                  border: InputBorder.none,
                  enabledBorder: InputBorder.none,
                  focusedBorder: InputBorder.none,
                  contentPadding: EdgeInsets.zero,
                ),
                onSubmitted: (_) => _handleSend(),
              ),
            ),
            
            // Send Button
            IconButton(
              onPressed: widget.isLoading ? null : _handleSend,
              icon: Icon(
                Icons.arrow_upward_rounded,
                color: _controller.text.isEmpty
                    ? EtherealTheme.slateBlue.withValues(alpha: 0.5)
                    : EtherealTheme.royalAzure,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
