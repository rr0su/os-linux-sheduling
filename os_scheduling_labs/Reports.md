### Title
Linux Scheduling Latency Benchmark

### Objective
To evaluate timer latency across different scheduling conditions.

### Method
Used cyclictest with baseline, pinned, background load, and RT priority. Data parsed and plotted using Python.

### Results
Include `summary_latency.csv` and the `latency_summary.png` graph.

### Analysis
- Baseline latency was moderate (X µs avg, Y µs max).
- Pinned execution reduced jitter due to improved cache locality.
- Background load increased max latency by Z%.
- RT scheduling improved determinism but reduced fairness.

### Conclusion
Low-latency performance is achieved by CPU pinning + RT scheduling, but must be balanced with fairness and resource availability.
