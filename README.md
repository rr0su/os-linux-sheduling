# 🧠 Scheduling Mini Project  
### **Latency Benchmarking & Scheduling Analysis (Linux / WSL2 / Ubuntu)**

---

## 🎯 Objective

Measure and compare **CPU scheduling latency** under different scenarios (baseline, pinned, background load, RT priority, etc.) using `cyclictest`, visualize results, and analyze how Linux scheduling policies affect performance and responsiveness.

---

## 🧩 Overview

**Goal:** Evaluate how CPU affinity, background load, and real-time priority affect timer latency.

**Tools used:**
- `cyclictest` (from `rt-tests`) — measures latency of periodic tasks  
- `stress` — generates CPU load  
- `taskset` / `chrt` — control CPU affinity and scheduling policy  
- `perf` — optional deeper scheduling trace  
- `Python (pandas, matplotlib)` — for CSV parsing and graph plotting  

---

## ⚙️ Environment Setup

Run these once:

```bash
sudo apt update
sudo apt install -y rt-tests stress taskset python3 python3-pip linux-tools-common linux-tools-$(uname -r) perf
pip3 install pandas matplotlib
```




Check environment info (for report):
```bash
uname -a
lscpu | grep 'Model name'
nproc
```
------------------

📂 Project Structure
Day17_Scheduling_Project/
│
├── run_latency_tests.sh        # Runs all benchmark scenarios
├── parse_cyclic_outputs.py     # Extracts min/avg/max latency from outputs
├── plot_latency.py             # Generates bar chart (latency_summary.png)
│
└── latency_results/
    ├── baseline.txt
    ├── pinned_cpu0.txt
    ├── with_background_load.txt
    ├── pinned_cpu0_with_load.txt
    ├── chrt_rt.txt
    ├── summary_latency.csv
    └── latency_summary.png
    
--------------------------------------------

🧪 Step-by-Step Procedure
1️⃣ Run All Benchmarks
```bash
chmod +x run_latency_tests.sh
sudo ./run_latency_tests.sh
```
This creates the folder latency_results/ containing text outputs for each scenario.


2️⃣ Parse Results into CSV
```bash
chmod +x parse_cyclic_outputs.py
./parse_cyclic_outputs.py
```

➡ Produces: latency_results/summary_latency.csv


3️⃣ Generate Graph
```bash
chmod +x plot_latency.py
./plot_latency.py
```

➡ Produces: latency_results/latency_summary.png

4️⃣ (Optional) Capture Scheduler Trace
```bash
sudo perf sched record -a sleep 10
sudo perf sched latency > latency_results/perf_sched_latency.txt
```

📊 Expected Results (Example)
| Scenario              | Min (µs) | Avg (µs) | Max (µs) |
| --------------------- | -------- | -------- | -------- |
| baseline              | 5        | 8        | 25       |
| pinned_cpu0           | 3        | 6        | 18       |
| with_background_load  | 7        | 15       | 60       |
| pinned_cpu0_with_load | 5        | 10       | 40       |
| chrt_rt               | 2        | 3        | 10       |

📈 See the generated graph in latency_results/latency_summary.png.

--------------------

🧠 Analysis Guidelines

Write this section in your report (200–400 words):
    .Effect of CPU pinning: Did latency variance (max) reduce? Why?
    .Effect of background load: How much did max latency rise?
    .Effect of RT priority: How does SCHED_FIFO/SCHED_RR scheduling improve determinism?
    .Trade-offs: Low latency vs fairness vs throughput.
    .If CONFIG_PREEMPT or low-latency kernel used: Note differences.
    
  Example key findings:
           .Pinned threads → better cache locality, lower jitter.
          .Background load → higher scheduling delays.
          .RT policy → near-constant latency but starves normal tasks.

📘 Deliverables
| File                        | Description                  |
| --------------------------- | ---------------------------- |
| `run_latency_tests.sh`      | Benchmark automation         |
| `latency_results/*.txt`     | Raw cyclictest logs          |
| `summary_latency.csv`       | Parsed latency data          |
| `latency_summary.png`       | Graph visualization          |
| `report.md` or `report.pdf` | Final analysis & conclusions |

