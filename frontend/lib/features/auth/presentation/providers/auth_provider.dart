import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../../../core/providers/dio_provider.dart';
import '../../data/models/user_model.dart';
import '../../data/services/auth_service.dart';

part 'auth_provider.g.dart';

@riverpod
AuthService authService(AuthServiceRef ref) {
  final dioClient = ref.watch(dioClientProvider);
  return AuthService(dioClient);
}

@riverpod
class Auth extends _$Auth {
  @override
  FutureOr<UserModel?> build() async {
    return _checkAuthStatus();
  }

  Future<UserModel?> _checkAuthStatus() async {
    try {
      final authService = ref.read(authServiceProvider);
      return await authService.getProfile();
    } catch (e) {
      return null;
    }
  }

  Future<void> login({
    required String email,
    required String password,
  }) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final authService = ref.read(authServiceProvider);
      final response = await authService.login(
        email: email,
        password: password,
      );
      return response.user;
    });
  }

  Future<void> register({
    required String email,
    required String password,
    String? name,
  }) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final authService = ref.read(authServiceProvider);
      final response = await authService.register(
        email: email,
        password: password,
        name: name,
      );
      return response.user;
    });
  }

  Future<void> logout() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final authService = ref.read(authServiceProvider);
      await authService.logout();
      return null;
    });
  }
}
