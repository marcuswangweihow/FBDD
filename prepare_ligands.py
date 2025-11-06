import os
from openbabel import openbabel, pybel

#=================================================
# Setup folders and directories
#=================================================
PATH = r"C:\Users\Admin\Documents\Documents\Misc\FBDD project\4MZI - Crystal structure of a human mutant p53\Ligands"
out_ligand_dir = os.path.join(PATH, "ligands_pdbqt")
os.makedirs(out_ligand_dir, exist_ok=True)

#=================================================
# Merge non-polar hydrogens
#=================================================
def merge_nonpolar_h(mol):

    for atom in list(mol):
        if atom.atomicnum == 1:
            bonded_atoms = [nbr for nbr in openbabel.OBAtomAtomIter(atom.OBAtom)]
            
            if all(nbr.GetAtomicNum() == 6 for nbr in bonded_atoms):
                mol.OBMol.DeleteAtom(atom.OBAtom)
                
    return mol

#=================================================
# Loop over all SDF files in folder
#=================================================
sdf_files = [f for f in os.listdir(PATH) if f.lower().endswith(".sdf")]

# global counter for unique ligand names
ligand_counter = 1

for sdf_file in sdf_files:
    sdf_path = os.path.join(PATH, sdf_file)
    
    for mol in pybel.readfile("sdf", sdf_path):
        
        # Add all hydrogens
        mol.addh()
        
        # Assign Gasteiger charges
        mol.calccharges(model="gasteiger")
        
        # Merge non-polar H
        mol = merge_nonpolar_h(mol)
        
        # Count rotatable bonds
        rotatable_bonds = mol.OBMol.NumRotors()
        
        # Write pdbqt
        ligand_name = f"ligand_{ligand_counter:04d}.pdbqt"
        
        out_path = os.path.join(out_ligand_dir, ligand_name)
        mol.write("pdbqt", out_path, overwrite=True)
        
        # print(f"{ligand_name}: {rotatable_bonds} rotatable bonds, TORSDOF={rotatable_bonds}")

        # Counter to monitor progress is no. of files are large
        if ligand_counter % 200 == 0:
            print(f"Just finished processing {ligand_counter} ligands")
        
        ligand_counter += 1

print('All ligands prepared')
