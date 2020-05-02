#!/usr/bin/env bash
mkdir ./ligands_pdbqts
for file in ./ligands_sdfs/*.sdf; 
do
tmp=${file%.sdf}; 
name="${tmp##*/}"; 

if [ -f $HOME/mgltools/bin/pythonsh ] && [ $1 == 2 ]; then
obabel $file -O ./ligands_pdbqts/${name}_.pdb -m --unique;
for pdbligand in ./ligands_pdbqts/*.pdb
do
tmp2=${pdbligand%.pdb}; 
name2="${tmp2##*/}"; 

$HOME/mgltools/bin/pythonsh prepare_ligand4.py -l $pdbligand -o ./ligands_pdbqts/$name2.pdbqt -A 'hydrogens_bonds' -U 'nphs_lps'
done;
rm $(ls ./ligands_pdbqts/*.pdb)

elif [ $1 == 1 ]; then
obabel $file -O ./ligands_pdbqts/${name}_.pdbqt -m --unique;

else
echo "Incorrect input. Please choose 1 or 2 as options"
fi
done;