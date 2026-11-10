#!/bin/bash
ORCA=~/orca/orca_6_1_1_macosx_intel_openmpi411/orca
cd ~/ase_project
for d in jobs/*/ ; do
  name=$(basename "$d")
  cd "$d"
  grep -v '%pal' $name.inp > ${name}_serial.inp
  echo "Running $name ..."
  $ORCA ${name}_serial.inp > $name.out
  cd ~/ase_project
done
echo "All done"
