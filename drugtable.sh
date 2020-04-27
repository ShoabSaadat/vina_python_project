#!/usr/bin/env bash
echo "Filename Number LineNumber Occurances DrugID DrugName" >> drugtable.txt;
echo "Filename Number LineNumber Occurances DrugName" >> drugtable_byname.txt;
echo "Filename Number LineNumber Occurances DrugName" >> drugtable_bydollars.txt;
files=$(ls ./ligands_sdfs/*.sdf);
for file in $files;
do 

awk '/.*id.*/{getline;drugid=$0;getline;getline;if($0~/.*name.*/){getline;drugname=$0};print FILENAME, ++a, NR-1,NF,drugid,drugname}' $file >> drugtable.txt;
awk '/.*name.*/{getline;drugname=$0;print FILENAME, ++a, NR-1,NF,drugname}' $file >> drugtable_byname.txt;
awk '/.*\$\$\$\$.*/{getline;drugname=$0;print FILENAME, ++a, NR-1,NF,drugname}' $file >> drugtable_bydollars.txt;

done;
