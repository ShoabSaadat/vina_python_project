#!/usr/bin/env bash
export receptorfilename="receptor_VP1";
echo "Filename Mode Affinity Dist_From_RMSD_lb Best_Mode_RMSD_ub" >> results_$1.txt;
for file in ./outs_$1/*.log;
do tmp=${file%.log};
name="${tmp##*/}"; 
awk '/^[-+]+$/{getline;print FILENAME,$0}' $file >> temp;  
done; 
sort temp -nk 3 >> results_$1.txt; 
rm temp;
