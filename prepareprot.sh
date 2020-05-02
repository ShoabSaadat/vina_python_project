#!/usr/bin/env bash
mkdir ./receptor/rawpdbs
if [ -f ./receptor/rawpdbs/$1_raw.pdb ]; then
rm ./receptor/$1.pdb
else
mv ./receptor/$1.pdb ./receptor/rawpdbs/$1_raw.pdb
fi

#egrep '(REMARK|ATOM)' ./receptor/$1_modified.pdb > ./receptor/$1.pdb #modified is preprocessed by pymol in python
#rm ./receptor/$1_modified.pdb
mv ./receptor/$1_modified.pdb ./receptor/$1.pdb

if [ -f $HOME/mgltools/bin/pythonsh ] && [ $2 == 2 ]; then
echo "MGL Tools found. Using Autodock tools to process the receptor."
#source ./mgltoolspath.sh #Doesnt work when a new terminal opens, ideally update ~/.bash_profile
$HOME/mgltools/bin/pythonsh prepare_receptor4.py -r ./receptor/$1.pdb -o ./receptor/$1.pdbqt -A bonds_hydrogens -U nphs_lps_waters_nonstdres -v
else
echo "Using Open Babel to process the receptor."

if [ -f /usr/bin/obabel ]; then
echo "Finding openbabel..."
alias obabel="/usr/bin/obabel" #Just resetting obabel alias just in case
/usr/bin/obabel ./receptor/$1.pdb -xhn -O ./receptor/$1.pdbqt;
else
echo "Sorry. No openbabel installation found on this system. Install that first."
fi
fi