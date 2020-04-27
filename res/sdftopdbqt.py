import os
import sys
import argparse



def convert(filename):
    pass

def listit(filename):
    if ifs.open(filename):
        if ofs.open("output.mol2"):
            for mol in ifs.GetOEGraphMols():
                oechem.OEWriteMolecule(ofs, mol)
        else:
            oechem.OEThrow.Fatal("Unable to create 'output.mol2'")
    else:
        oechem.OEThrow.Fatal("Unable to open 'sdf'")


parser = argparse.ArgumentParser(description='Prep ligands for AutoDock Vina')
parser.add_argument('-c',
					'--convert',
					nargs='+',
					help='Prep and convert protein receptor from sdf to PDBQT')
parser.add_argument('-l',
					'--listit',
					nargs='+',
					help='Ceate sdf name list')
args = parser.parse_args()

def main():
	if args.convert:
		convert(sys.argv[2])
	elif args.listit:
		listit(sys.argv[2])

if __name__ == '__main__': 
	main()