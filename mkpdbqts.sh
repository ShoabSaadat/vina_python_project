#!/usr/bin/env bash
mkdir ./ligands_pdbqts
for file in ./ligands_sdfs/*.sdf; 
do
tmp=${file%.sdf}; 
name="${tmp##*/}"; 
obabel $file -O ./ligands_pdbqts/${name}_.pdbqt -m --unique;
done;