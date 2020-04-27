1. Installing needed packages: ---------------
---
sudo apt update
sudo apt upgrade
sudo apt install autodock-vina
sudo apt install pymol / chimera
sudo apt install openbabel
sudo apt install unzip
---
#Also, install autodock tools on computer

#Now get template project scaffold ----------
---
wget https://de.cyverse.org/dl/d/AC88DABD-6FD2-45F2-8AF4-8241395C035D/vina_prep.zip
unzip vina_prep.zip
mv ./vina_prep ./Vina_Project
rm vina_prep.zip 
cd Vina_Project
---

2a. Getting ligands as pdbqt
#Ideally get from zinc as pdbqt
#Else learn to convert from sdf to multiple pdbqt files-- Following code will generate pdbqts for all single or combined sdfs

for file in ./ligands_sdfs/*.sdf; 
do
tmp=${file%.sdf}; 
name="${tmp##*/}"; 
obabel $file -O ${name}_.pdbqt -m --unique;
done;
mkdir ./ligands_pdbqts
mv *.pdbqt ./ligands_pdbqts/


2b. Creation of Drug Table from all SDFs to finally correlate each ligand with original drug name:
---
echo "Filename Number LineNumber Occurances DrugID DrugName" >> drugtable.txt drugtable_byname.txt drugtable_bydollars.txt;
files=$(ls ./ligands_sdfs/*.sdf);
for file in $files;
do 

awk '/.*id.*/{getline;drugid=$0;getline;getline;if($0~/.*name.*/){getline;drugname=$0};print FILENAME, ++a, NR-1,NF,drugid,drugname}' $file >> drugtable.txt;
awk '/.*name.*/{getline;drugname=$0;print FILENAME, ++a, NR-1,NF,drugname}' $file >> drugtable_byname.txt;
awk '/.*\$\$\$\$.*/{getline;drugname=$0;print FILENAME, ++a, NR-1,NF,drugname}' $file >> drugtable_bydollars.txt;

done;
--

3. Getting and preparing protein
#protein as receptor_1.pdb

Prepare:
---
grep ATOM ./receptor/receptor_1.pdb > ./receptor/receptor.pdb #Get all atoms only
---
#Learn about other steps using openbabel from youtube
#Convert to pdbqt using autodock tools
#Get search area using autodock_tools or chimera

4. Now your main directory should have following files:
./vina
./vina_split
./receptor/receptor.pdbqt
./ligands_pdbqt/(multiple ligands).pdbqt
./ligands_sdfs/(multiple ligands).sdfs
./grid.txt #from autodock tools
./res


5. Update the seach parameters of the protein and Run following command with changes to search area:
---
receptorfilename="receptor_VP1";
gridfilename=./grid_VP1a.txt;

size_x=$(awk '/.*npts.*/{print $2}' ${gridfilename});
size_y=$(awk '/.*npts.*/{print $3}' ${gridfilename});
size_z=$(awk '/.*npts.*/{print $4}' ${gridfilename});

center_x=$(awk '/.*center.*/{print $2}' ${gridfilename});
center_y=$(awk '/.*center.*/{print $3}' ${gridfilename});
center_z=$(awk '/.*center.*/{printf \\n $4}' ${gridfilename});

mkdir outs_${receptorfilename};
for file in ./ligands_pdbqts/*; 
do tmp=${file%.pdbqt}; 
name="${tmp##*/}";
vina --receptor ./receptor/${receptorfilename}.pdbqt --ligand "$file" --out ./outs_${receptorfilename}/${name}_out.pdbqt --log ./outs_${receptorfilename}/${name}.log --exhaustiveness 8 --center_x ${center_x} --center_y ${center_y} --center_z ${center_z} --size_x ${size_x} --size_y ${size_y} --size_z ${size_z};
done;

#Generate Results:
echo "Filename Mode Affinity Dist_From_RMSD_lb Best_Mode_RMSD_ub" >> results_${receptorfilename}.txt;
for file in ./outs_${receptorfilename}/*.log;
do tmp=${file%.log};
name="${tmp##*/}"; 
awk '/^[-+]+$/{getline;print FILENAME,$0}' $file >> temp;  
done; 
sort temp -nk 3 >> results_${receptorfilename}.txt; 
rm temp;

---

