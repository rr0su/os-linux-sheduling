#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import pathlib

CSV = pathlib.Path("latency_results/summary_latency.csv")
df = pd.read_csv(CSV)

# Convert strings to numeric (some may be empty)
for col in ["min_us","avg_us","max_us"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.set_index("scenario")
df = df.sort_index()

ax = df[["min_us","avg_us","max_us"]].plot(kind="bar", figsize=(10,6))
ax.set_ylabel("Latency (microseconds)")
ax.set_title("Cyclictest latency summary per scenario")
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
out_png = "latency_results/latency_summary.png"
plt.savefig(out_png)
print("Saved graph to", out_png)
