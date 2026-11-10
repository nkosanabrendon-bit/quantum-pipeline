# Quantum Pipeline (ASE + ORCA)

A small pipeline that builds molecules with ASE, writes ORCA input files, runs the calculations, and collects the energies into a table.

ORCA is not included. It is free for academic use after registering on the ORCA forum and accepting its license. This was run with ORCA 6.1.1 (macOS Intel build).

## Steps
1. make_orca_jobs.py builds 6 molecules with ASE (H2O, NH3, CH4, CO2, C2H4, CH3OH) and writes one ORCA input file for each in jobs/NAME/NAME.inp. Method: B3LYP def2-SVP.
2. run_all_local.sh runs every input one after another on 1 core (a local stand-in for a cluster).
3. read_energies.py reads FINAL SINGLE POINT ENERGY from each output file and saves energies.csv.
4. first_ase.py is a first ASE warm-up (water, copper crystal, relaxation with the toy EMT calculator).

## Results (single-point energies, B3LYP/def2-SVP, 1 core)

| Molecule | Energy (hartree) |
|---|---|
| CH4 | -40.452 |
| NH3 | -56.473 |
| C2H4 | -78.473 |
| H2O | -76.321 |
| CH3OH | -115.565 |
| CO2 | -188.360 |

## Honest limits
- These are single-point energies on starting shapes from ASE. The shapes were not optimized with this method.
- The method choice (B3LYP def2-SVP) was picked for learning. It was not checked for these molecules, and the energies were not compared with published reference values.
- Running water twice gave -76.321274 and -76.321226 hartree from the same input. The cause was not investigated.
- Only 1 core was used. The 4-core input (%pal nprocs 4) needs a matching OpenMPI version, and it was not tested.
- submit_all.sh is a SLURM template. It was NOT tested on a real cluster, and the ORCA path in it is a placeholder.
- Molecules only. Battery crystals need periodic calculations, which this pipeline does not do.
