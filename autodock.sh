#!/usr/bin/env bash
mkdir outs_$1;
for file in ./ligands_pdbqts/*; 
do tmp=${file%.pdbqt}; 
name="${tmp##*/}";
if [ -f /usr/bin/vina ]; then
vina --receptor ./receptor/$1.pdbqt --ligand "$file" --out ./outs_$1/${name}_out.pdbqt --log ./outs_$1/${name}.log --exhaustiveness $8 --size_x $2 --size_y $3 --size_z $4 --center_x $5 --center_y $6 --center_z $7;
else
./vina --receptor ./receptor/$1.pdbqt --ligand "$file" --out ./outs_$1/${name}_out.pdbqt --log ./outs_$1/${name}.log --exhaustiveness $8 --size_x $2 --size_y $3 --size_z $4 --center_x $5 --center_y $6 --center_z $7;
fi
done;