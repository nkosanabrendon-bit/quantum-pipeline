import os
from ase.build import molecule

NAMES = ["H2O", "NH3", "CH4", "CO2", "C2H4", "CH3OH"]
METHOD = "B3LYP def2-SVP"      # a common, cheap choice for learning
CORES = 4

os.makedirs("jobs", exist_ok=True)
for name in NAMES:
    atoms = molecule(name)
    folder = os.path.join("jobs", name)
    os.makedirs(folder, exist_ok=True)
    lines = ["! " + METHOD, "%pal nprocs " + str(CORES) + " end", "* xyz 0 1"]
    for sym, (x, y, z) in zip(atoms.get_chemical_symbols(), atoms.get_positions()):
        lines.append("%-2s %12.6f %12.6f %12.6f" % (sym, x, y, z))
    lines.append("*")
    with open(os.path.join(folder, name + ".inp"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("Wrote", os.path.join(folder, name + ".inp"), "with", len(atoms), "atoms")

# A template SLURM script. Edit the ORCA path and any module lines for your cluster.
with open("submit_all.sh", "w") as f:
    f.write("""#!/bin/bash
# Template. Change ORCA_PATH (and add a module load line if your cluster needs one).
ORCA_PATH=/path/to/orca
for d in jobs/*/ ; do
  name=$(basename "$d")
  cat > "$d/run.sbatch" << SB
#!/bin/bash
#SBATCH --job-name=$name
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=%d
#SBATCH --output=$name.slurm.out
cd $(pwd)/$d
$ORCA_PATH $name.inp > $name.out
SB
  sbatch "$d/run.sbatch"
done
""" % CORES)
print("Wrote submit_all.sh (a template, not tested on a cluster)")
