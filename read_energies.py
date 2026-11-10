import glob
import os
import re
import pandas as pd

rows = []
for out in sorted(glob.glob("jobs/*/*.out")):
    if out.endswith(".slurm.out"):
        continue
    name = os.path.basename(os.path.dirname(out))
    energy, done = None, False
    for line in open(out, errors="ignore"):
        if "FINAL SINGLE POINT ENERGY" in line:
            energy = float(re.findall(r"-?\d+\.\d+", line)[-1])
        if "ORCA TERMINATED NORMALLY" in line:
            done = True
    rows.append({"molecule": name, "energy_hartree": energy, "finished_ok": done})

df = pd.DataFrame(rows)
if len(df):
    df["energy_eV"] = (df["energy_hartree"] * 27.2114).round(3)
df.to_csv("energies.csv", index=False)
print(df.to_string(index=False) if len(df) else "No finished .out files found yet.")
