#!/usr/bin/env python
import sys
import os
from AutoDockTools.MoleculePreparation import prepare_receptor

pdb_path = sys.argv[1]
output_pdbqt = sys.argv[2]

receptor = prepare_receptor(pdb_path)
receptor.deleteWater()
receptor.addHydrogens(polarOnly=True)
receptor.computeGasteigerCharges()
receptor.writePDBQT(output_pdbqt)
