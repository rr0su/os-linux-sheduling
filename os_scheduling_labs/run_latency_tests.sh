#!/usr/bin/env bash
set -euo pipefail

OUTDIR=latency_results
mkdir -p "$OUTDIR"

# Experiment parameters
ITER=10s        # how long to measure in each run (change if you want longer)
INTERVAL=1000   # cyclictest interval in microseconds
PRIO=80         # RT priority for RT test

# helper to run cyclictest and save stdout
run_test() {
  local name="$1"
  echo "=== Running: $name ==="
  local out="$OUTDIR/${name// /_}.txt"
  # run cyclictest: -n (no configure), -p priority, -i interval(us), -l loops (we use time instead),
  # -D = delay until start, -v verbose, -h print histogram? We'll capture summary lines.
  sudo cyclictest -p "$PRIO" -n -i "$INTERVAL" -l 0 -m -D 0 -q --duration="$ITER" > "$out" 2>&1
  grep -E "Min:|Max:|Avg:" "$out" || true
  echo "Saved: $out"
}

# SCENARIO 1: baseline
run_test "baseline"

# SCENARIO 2: pinned to cpu0
run_test "pinned_cpu0" & pid_bg=$!
wait $pid_bg

# SCENARIO 3: background load (stress other cores)
(sudo stress --cpu "$(nproc --ignore 1)" --timeout "$ITER" &) 
run_test "with_background_load"

# SCENARIO 4: pinned while background load runs
(sudo stress --cpu "$(nproc --ignore 1)" --timeout "$ITER" &) 
taskset -c 0 sudo cyclictest -p "$PRIO" -n -i "$INTERVAL" -l 0 -m -D 0 -q --duration="$ITER" > "$OUTDIR/pinned_cpu0_with_load.txt" 2>&1
grep -E "Min:|Max:|Avg:" "$OUTDIR/pinned_cpu0_with_load.txt" || true

# SCENARIO 5: run cyclictest with explicit chrt RT priority (if you want a different variation)
sudo chrt -f "$PRIO" bash -c "cyclictest -n -i $INTERVAL -l 0 -m -D 0 -q --duration=$ITER" > "$OUTDIR/chrt_rt.txt" 2>&1
grep -E "Min:|Max:|Avg:" "$OUTDIR/chrt_rt.txt" || true

echo "All tests finished. Results in $OUTDIR/"
