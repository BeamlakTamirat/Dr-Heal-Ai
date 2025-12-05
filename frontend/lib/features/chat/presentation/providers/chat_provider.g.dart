// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'chat_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

String _$chatServiceHash() => r'5b5933a8537c34f91b86a525762a3cecc98027e2';

/// See also [chatService].
@ProviderFor(chatService)
final chatServiceProvider = AutoDisposeProvider<ChatService>.internal(
  chatService,
  name: r'chatServiceProvider',
  debugGetCreateSourceHash:
      const bool.fromEnvironment('dart.vm.product') ? null : _$chatServiceHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
typedef ChatServiceRef = AutoDisposeProviderRef<ChatService>;
String _$conversationsHash() => r'768befc539a9aa6fbcf1856fbe779c02400e3982';

/// See also [conversations].
@ProviderFor(conversations)
final conversationsProvider =
    AutoDisposeFutureProvider<List<ConversationModel>>.internal(
  conversations,
  name: r'conversationsProvider',
  debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
      ? null
      : _$conversationsHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
typedef ConversationsRef
    = AutoDisposeFutureProviderRef<List<ConversationModel>>;
String _$chatHash() => r'3ba2daffb516f0f77d82c3f2961adf21f3e39a4c';

/// See also [Chat].
@ProviderFor(Chat)
final chatProvider = AutoDisposeNotifierProvider<Chat, ChatState>.internal(
  Chat.new,
  name: r'chatProvider',
  debugGetCreateSourceHash:
      const bool.fromEnvironment('dart.vm.product') ? null : _$chatHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

typedef _$Chat = AutoDisposeNotifier<ChatState>;
// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member, deprecated_member_use_from_same_package
