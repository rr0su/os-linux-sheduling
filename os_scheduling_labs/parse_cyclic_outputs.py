#!/usr/bin/env python3
import re, sys, pathlib, csv

OUTDIR = pathlib.Path("latency_results")
CSV = OUTDIR / "summary_latency.csv"

pattern_min = re.compile(r"Min:\s*([0-9.]+)")
pattern_avg = re.compile(r"Avg:\s*([0-9.]+)")
pattern_max = re.compile(r"Max:\s*([0-9.]+)")

rows = []
for f in sorted(OUTDIR.glob("*.txt")):
    text = f.read_text()
    name = f.stem
    # Look for lines like: Min: 4us, Avg: 8us, Max: 20us
    # We'll try to find values with units and convert to microseconds
    def find_val(pat):
        m = pat.search(text)
        if not m:
            return None
        val = float(m.group(1))
        return val
    minv = find_val(re.compile(r"Min:\s*([0-9.]+)\s*(us|ms|ns)?"))
    avgv = find_val(re.compile(r"Avg:\s*([0-9.]+)\s*(us|ms|ns)?"))
    maxv = find_val(re.compile(r"Max:\s*([0-9.]+)\s*(us|ms|ns)?"))
    # Fallback: try generic pattern
    if minv is None or avgv is None or maxv is None:
        # search lines with Min/Avg/Max together
        for line in text.splitlines():
            if "Min:" in line and "Avg:" in line and "Max:" in line:
                # extract numbers
                nums = re.findall(r"([\d.]+)\s*(us|ms|ns)?", line)
                if nums and len(nums) >= 3:
                    def to_us(pair):
                        val, unit = pair
                        val = float(val)
                        if unit == 'ms': return val * 1000.0
                        if unit == 's': return val * 1e6
                        if unit == 'ns': return val / 1000.0
                        return val
                    try:
                        minv = to_us(nums[0])
                        avgv = to_us(nums[1])
                        maxv = to_us(nums[2])
                    except:
                        pass
                break
    rows.append((name, minv if minv else "", avgv if avgv else "", maxv if maxv else ""))

with open(CSV, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["scenario","min_us","avg_us","max_us"])
    for r in rows:
        w.writerow(r)

print("Wrote:", CSV)
