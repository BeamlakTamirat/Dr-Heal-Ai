import 'dart:math';
import 'package:flutter/material.dart';
import '../theme/ethereal_theme.dart';

class ParticleBackground extends StatefulWidget {
  final Widget child;
  final int numberOfParticles;

  const ParticleBackground({
    super.key,
    required this.child,
    this.numberOfParticles = 30,
  });

  @override
  State<ParticleBackground> createState() => _ParticleBackgroundState();
}

class _ParticleBackgroundState extends State<ParticleBackground>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late List<Particle> _particles;
  final Random _random = Random();

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();

    _particles = List.generate(
      widget.numberOfParticles,
      (index) => Particle(_random),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Base Background Color
        Container(color: EtherealTheme.paleAliceBlue),
        
        // Animated Particles
        AnimatedBuilder(
          animation: _controller,
          builder: (context, child) {
            return CustomPaint(
              painter: ParticlePainter(
                particles: _particles,
                controllerValue: _controller.value,
              ),
              size: Size.infinite,
            );
          },
        ),
        
        // Content
        widget.child,
      ],
    );
  }
}

class Particle {
  late double x;
  late double y;
  late double speed;
  late double theta;
  late double radius;

  Particle(Random random) {
    x = random.nextDouble();
    y = random.nextDouble();
    speed = random.nextDouble() * 0.2 + 0.1;
    theta = random.nextDouble() * 2 * pi;
    radius = random.nextDouble() * 2 + 1;
  }

  void update() {
    x += cos(theta) * speed * 0.005;
    y += sin(theta) * speed * 0.005;

    if (x < 0 || x > 1 || y < 0 || y > 1) {
      theta += pi; 
    }
  }
}

class ParticlePainter extends CustomPainter {
  final List<Particle> particles;
  final double controllerValue;

  ParticlePainter({
    required this.particles,
    required this.controllerValue,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = EtherealTheme.royalAzure.withValues(alpha: 0.15)
      ..style = PaintingStyle.fill;

    final linePaint = Paint()
      ..color = EtherealTheme.royalAzure.withValues(alpha: 0.05)
      ..strokeWidth = 1;

    for (var i = 0; i < particles.length; i++) {
      var particle = particles[i];
      particle.update();

      var dx = particle.x * size.width;
      var dy = particle.y * size.height;

      canvas.drawCircle(Offset(dx, dy), particle.radius, paint);

      // Draw connections
      for (var j = i + 1; j < particles.length; j++) {
        var other = particles[j];
        var otherDx = other.x * size.width;
        var otherDy = other.y * size.height;

        var distance = sqrt(pow(dx - otherDx, 2) + pow(dy - otherDy, 2));

        if (distance < 150) {
          canvas.drawLine(Offset(dx, dy), Offset(otherDx, otherDy), linePaint);
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
