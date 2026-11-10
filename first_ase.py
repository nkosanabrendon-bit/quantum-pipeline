from ase.build import molecule, bulk, fcc111
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from ase.filters import UnitCellFilter
from ase.io import write

# 1. A molecule: water
water = molecule("H2O")
print("Water atoms:", water.get_chemical_symbols())
print("O-H distance (angstrom):", round(water.get_distance(0, 1), 3))
print("H-O-H angle (degrees):", round(water.get_angle(1, 0, 2), 1))
write("water.xyz", water)

# 2. A crystal: copper
cu = bulk("Cu", "fcc", a=3.6)
cu.calc = EMT()
print()
print("Copper atoms in the cell:", len(cu))
print("Copper energy per atom (eV):", round(cu.get_potential_energy() / len(cu), 4))

# 3. Start with a crystal that is too big, and let ASE find the best size
cu_big = bulk("Cu", "fcc", a=3.9, cubic=True)
cu_big.calc = EMT()
e_before = cu_big.get_potential_energy()
opt = BFGS(UnitCellFilter(cu_big), logfile=None)
opt.run(fmax=0.01)
print("Energy before relaxing (eV):", round(e_before, 4))
print("Energy after relaxing (eV):", round(cu_big.get_potential_energy(), 4))
print("Relaxed lattice constant (angstrom):", round(cu_big.cell.cellpar()[0], 3), "(real copper is about 3.61)")

# 4. A surface slab, saved as a file
slab = fcc111("Cu", size=(2, 2, 3), vacuum=8.0)
write("cu_slab.cif", slab)
print()
print("Slab atoms:", len(slab))
print("Saved: water.xyz, cu_slab.cif")
