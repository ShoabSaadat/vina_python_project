__________________________________________________
Copyright License

Copyright (c) 2020 Shoab Saadat [dr.shoaibsaadat@gmail.com]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
__________________________________________________

# Help File
I explain the steps to follow in order to get the docking pipeline flowing:

## 1. Get yourself a linux system with python3 installed
```
sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install pip-python3
```

## 2. Prepare the linux system using my python-tool
Make sure you have autodock_python.py in the current folder
```
python3 autodock_python.py -s all
```

## 3. Download typical directory structure for docking
It creates a directory named Vina_Project and takes you in it.
```
python3 autodock_python.py -d all
```

## 4. Prepare protein receptor
Now you will be in Vina_Project folder, here, put your receptor_xyz.pdb file in receptor folder to start
```
python3 autodock_python.py -pp [receptor_name] / ["all"]
```
It is a powerful protein preparation app which uses one of the following two systems base on availability on your system:
- Pymol with openbabel
In this case, it uses pymol to remove water molecules and add polar hydrogen while using openbabel for the charge addition and pdbqt conversion.
- MGLTools and Audodock Tools
This is an advanced conversion tool. It automatically removes water, adds hydrogen, merges nonpolar hydrogen charges, merges lone-pairs, remove chains composed entirely of residues of types other than the standard 20 amino acids, and adds gasteiger charges to the peptide molecule.

Now you should have the following files:
- ./vina
- ./vina_split
- ./receptor/receptor_xyz.pdb (Use it to prepare and make a pdbqt file using autodock-tools. Keep it here even if you make a pdbqt)
- ./ligands_sdfs/xyz.sdfs (Put your drug sdfs here)
- ./grid.txt (make from autodock tools and simply saving the gridbox output. Make sure to give it same name as your receptor)
- ./res (resources folder)
- ./ligands_pdbqt/ (Just a folder, will be populated after next step)

## 5. Create PDBQTs from all ligands
It offers two options for ligand processing.
- Using Open babel
- Using Autodock Tools
It automatically removes water, adds hydrogen, merges nonpolar hydrogen charges and merges lone-pairs. before using it, make sure you have sdf files in ligands_sdfs folder.
```
python3 autodock_python.py -p all
```

## 6. Create a grid file for search box
Using this command, you can provide residue numbers of the most important amino acids in your receptor protein and it will create a search box grid file around those receptors. Residues can be based on the literature study or fetched from pocket analyzing softwares, such as, CASTp, PASS, Pocket-Finder, PocketPicker etc. When asked, residue numbers should be entered as seperated by space like "6 12 50".
```
python3 autodock_python.py -g [receptor_name] / ["all"]
```
This will create a text file with a prefix of "grid_" in the main app directory. This file will be later used automatically for the subsequent docking step.

## 7. Start the AutoDock process
It does it for any pdbqt receptor in receptor folder and all ligand pdbqts in ligands_pdbqts folder
```
python3 autodock_python.py -ad [receptor_name] / ["all"]
```

## 8. Create result files
It creates a results file for each receptor with finalized info
```
python3 autodock_python.py -r [receptor_name] / ["all"]
```

## 9. Make lookup drug table files
It creates three kinds of drugtables to compare results with actual ligand details
```
python3 autodock_python.py -dt [receptor_name] / ["all"]
```

Note: With each command, you can use all or a certain receptor name. At any time if you want to know the receptor names for more targetted commands, type python3 autodock_python.py -i
