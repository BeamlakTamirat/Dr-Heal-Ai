import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import '../../../../core/theme/ethereal_theme.dart';
import '../../../../core/widgets/neo_glass_card.dart';

class BioStatusWidget extends StatefulWidget {
  const BioStatusWidget({super.key});

  @override
  State<BioStatusWidget> createState() => _BioStatusWidgetState();
}

class _BioStatusWidgetState extends State<BioStatusWidget> {
  late Timer _timer;
  final List<double> _heartRatePoints = List.filled(30, 0.5);
  final Random _random = Random();
  int _heartRate = 72;
  String _stressLevel = "Normal";

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(milliseconds: 100), (timer) {
      if (mounted) {
        setState(() {
          // Simulate heart beat wave
          double newValue = 0.5;
          if (timer.tick % 10 == 0) {
            newValue = 0.9; // Peak
          } else if (timer.tick % 10 == 1) {
            newValue = 0.1; // Trough
          } else {
            newValue = 0.5 + (_random.nextDouble() * 0.1 - 0.05); // Noise
          }

          _heartRatePoints.removeAt(0);
          _heartRatePoints.add(newValue);

          // Update stats occasionally
          if (timer.tick % 50 == 0) {
            _heartRate = 70 + _random.nextInt(10);
          }
        });
      }
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return NeoGlassCard(
      padding: const EdgeInsets.all(20),
      child: Row(
        children: [
          // Heart Rate Graph
          Expanded(
            flex: 2,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "BIO-METRICS",
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: EtherealTheme.royalAzure,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.5,
                  ),
                ),
                const SizedBox(height: 10),
                SizedBox(
                  height: 60,
                  child: CustomPaint(
                    painter: HeartRatePainter(points: _heartRatePoints),
                    size: Size.infinite,
                  ),
                ),
              ],
            ),
          ),
          
          // Stats
          Expanded(
            flex: 1,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                _buildStatItem("HEART RATE", "$_heartRate BPM", EtherealTheme.emergencyTriageColor),
                const SizedBox(height: 10),
                _buildStatItem("STRESS", _stressLevel, EtherealTheme.treatmentAdvisorColor),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatItem(String label, String value, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 10,
            fontWeight: FontWeight.bold,
            color: EtherealTheme.slateBlue,
          ),
        ),
        Text(
          value,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }
}

class HeartRatePainter extends CustomPainter {
  final List<double> points;

  HeartRatePainter({required this.points});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = EtherealTheme.emergencyTriageColor
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    final path = Path();
    final widthStep = size.width / (points.length - 1);

    for (var i = 0; i < points.length; i++) {
      final x = i * widthStep;
      final y = size.height - (points[i] * size.height);
      if (i == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
