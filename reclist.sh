#!/usr/bin/env bash
for file in ./receptor/*.pdb;
do if [ -f "$file" ]; then
tmp=${file%.pdb};
name="${tmp##*/}"; 
echo $name >> reclist.txt
else
echo "No pdb files in receptor folder"
fi;
done;



