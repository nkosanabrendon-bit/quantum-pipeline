#!/bin/bash
# Template. Change ORCA_PATH (and add a module load line if your cluster needs one).
ORCA_PATH=/path/to/orca
for d in jobs/*/ ; do
  name=$(basename "$d")
  cat > "$d/run.sbatch" << SB
#!/bin/bash
#SBATCH --job-name=$name
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4
#SBATCH --output=$name.slurm.out
cd $(pwd)/$d
$ORCA_PATH $name.inp > $name.out
SB
  sbatch "$d/run.sbatch"
done
