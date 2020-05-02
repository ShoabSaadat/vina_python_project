import os
import sys
from pathlib import Path
import argparse
import subprocess
import shlex
from pymol.cgo import *
from pymol import cmd
import pymol
import math
import webbrowser
#subprocess.call(shlex.split('./test.sh param1 param2')) #reference it in sh as $1 onwards
#subprocess.call(['./test.sh'])

def mkreclist(): #The list is made on present pdbs in receptor folder
    reclist = []
    subprocess.call(['./reclist.sh'])
    with open("reclist.txt", 'r+') as file_in:
        for line in file_in:
            reclist.append(line[:-1]) #escape newline character
        reclist = list(set(reclist)) #getting uniques
    with open("reclist.txt", "w") as file_out:
            for item in reclist:
                file_out.write("%s\n" % item)
    return reclist
 
def results(whichones, reclist):   
    #Handle arguments --
    if whichones == "all":
        for receptor in reclist:
            subprocess.call(shlex.split(f'./results.sh {receptor}'))
        print ('Result files created...')
    elif whichones in reclist:
        subprocess.call(shlex.split(f'./results.sh {whichones}'))
    else:
        print ('You have not provided correct receptor name. \nEnter "all" as an argument for all receptor results or \ntype one of the following receptor names after -r argument: ')
        print(reclist)
    
def drugtable(whichones):
    if whichones == "all":
        subprocess.call(['./drugtable.sh'])
        print ('Job done...')
    else:
        print ("Try giving the 'all' argument...")

def mkpdbqts(whichones):
    if whichones == "all":
        algchoice = input(
        '''How would you like to prepare your ligands: 
        1. Use Open Babel (Fast)
        2. Use Autodock Tools (Best from protein ligands)

        Choose the option 1 or 2: '''
        )
        subprocess.call(shlex.split(f'./mkpdbqts.sh {algchoice}'))
        
        print ('Process has been run.')
    else:
        print ("Try giving the 'all' argument...")

def download(whichones):
    if whichones == "all":
        subprocess.call(['./download.sh'])
        print ('\n----------------\nVina_Project folder downloaded. Please cd into that folder now.')
    else:
        print ("Try giving the 'all' argument...")

def setup(whichones):
    if whichones == "all":
        subprocess.call(['./setup.sh'])
        print ('Job done...')
    else:
        print ("Try giving the 'all' argument...")

def get_residue_text(receptor):
    residues = input(
    f'''\nFor protein receptor: {receptor},
Kindly write the important residues around which you would like your search grid box to be located. 
Residues can be based on the literature study or fetched from pocket analyzing softwares, such as, CASTp, PASS, Pocket-Finder, PocketPicker etc.
Enter the residue numbers seperated by space like "6 12 50"

Type here: '''
        )
    residuestring = ""
    for res in residues.split(' '):
        residuestring += 'resi '+res+ ' + '
    residuestring = residuestring.strip()[:-1].strip()
    return residuestring

def makegrid(whichones, reclist):
    extending = input("How wide the box extensions (Default is 5 angstroms) need to be?: ")
    try:
        extending = int(extending)
    except ValueError:
        try:
            extending = int(float(extending))
        except ValueError:
            extending = 5
            print("Your input is not a number. It's a string. We chose 5 angstrom for your receptor.\n")

    if whichones == "all":
        for receptor in reclist:
            residuestring = get_residue_text(receptor)
            cmd.load('./receptor/'+receptor+'.pdbqt')
            cmd.select("boxselection", (residuestring))

            with open("grid_"+receptor+".txt", "w") as file_out:
                file_out.write(getgridfile(receptor, "boxselection", extending))
            print("\n", getgridfile(receptor, "boxselection", extending), "\n", f"Successfully created grid file for {receptor}.... \n")
    elif whichones in reclist:
        residuestring = get_residue_text(whichones)
        cmd.load('./receptor/'+whichones+'.pdbqt')
        cmd.select("boxselection", (residuestring))

        with open("grid_"+whichones+".txt", "w") as file_out:
            file_out.write(getgridfile(whichones, "boxselection", extending))
        print("\n", getgridfile(whichones, "boxselection", extending), "\n", f"Successfully created grid file for {whichones}.... \n")
    else:
        print ('You have not provided correct receptor name. \nEnter "all" as an argument for all receptor results or \ntype one of the following receptor names after -r argument: ')
        print(reclist)

# getbox from cavity residues that reported in papers 
def getgridfile(receptor, selection = "(sele)", extending = 5.0): 
	cmd.hide("spheres")
	cmd.show("spheres", selection)                                                                                                
	([minX, minY, minZ],[maxX, maxY, maxZ]) = cmd.get_extent(selection)
	minX = minX - float(extending)
	minY = minY - float(extending)
	minZ = minZ - float(extending)
	maxX = maxX + float(extending)
	maxY = maxY + float(extending)
	maxZ = maxZ + float(extending)

	SizeX = maxX - minX
	SizeY = maxY - minY
	SizeZ = maxZ - minZ
	CenterX =  (maxX + minX)/2
	CenterY =  (maxY + minY)/2
	CenterZ =  (maxZ + minZ)/2

	AutoDockBox =f'''-------- AutoDock Grid Map for {receptor} --------
spacing 0.375 # spacing (A)
npts {SizeX/0.375:.3f} {SizeY/0.375:.3f} {SizeZ/0.375:.3f}
gridcenter {CenterX:.3f} {CenterY:.3f} {CenterZ:.3f}'''
	return AutoDockBox

def prepareprot_scaffold(preload, presave, receptor, postload, postsave, algchoice):
    canproceed = False

    cmd.load(preload+receptor+postload)
    all_chains = cmd.get_chains(receptor)
    print(f'Which chains would you like to keep for protein {receptor}. It has following chains: ', all_chains)
    selectedchain = input("Type the chain names seperated by space, \nif you want all chains, type 'all': ")
    chainstoremove = set(all_chains) - set(selectedchain.split(' '))
    if set(selectedchain.split(' ')).issubset(set(all_chains)):
        for chain in chainstoremove:
            cmd.remove('chain ' + chain)
            print(f'Chain {chain} removed.')
        canproceed = True
    elif selectedchain == 'all':
        print('All chains selected.')
        canproceed = True
    else:
        print('Wrong chain selection. Type it like "A B 6" if you have three chains named A, B and 6')
    
    if canproceed:
        cmd.remove('resn HOH')
        #cmd.h_add(selection='acceptors or donors')
        cmd.save(presave+receptor+postsave)
        subprocess.call(shlex.split(f'./prepareprot.sh {receptor} {algchoice}'))

def prepareprot(whichones, reclist):
    algchoice = input(
    '''How would you like to prepare your ligands: 
1. Use Open Babel (Fast)
2. Use Autodock Tools (Best from protein ligands)

Choose the option 1 or 2: '''
        )

    if whichones == "all":
        for receptor in reclist:
            if Path('./receptor/rawpdbs/'+receptor+'_raw.pdb').exists():
                processchoice = input("You have already processed the raw pdb, want to re-process? \nType 'raw' to re-process raw pdb or 'new' to process already processed file.\nType here: ")
                if processchoice == "new":
                    prepareprot_scaffold('./receptor/', './receptor/', receptor, '.pdb', '_modified.pdb', algchoice)
                else:
                    prepareprot_scaffold('./receptor/rawpdbs/', './receptor/', receptor, '_raw.pdb', '_modified.pdb', algchoice)
            else:
                prepareprot_scaffold('./receptor/', './receptor/', receptor, '.pdb', '_modified.pdb', algchoice)
        print ('Protein pdbqt file prepared...')
    elif whichones in reclist:
        if Path('./receptor/rawpdbs/'+whichones+'_raw.pdb').exists():
            processchoice = input("You have already processed the raw pdb, want to re-process? \nType 'raw' to re-process raw pdb or 'new' to process already processed file.\nType here: ")
            if processchoice == "new":
                prepareprot_scaffold('./receptor/', './receptor/', whichones, '.pdb', '_modified.pdb', algchoice)
            else:
                prepareprot_scaffold('./receptor/rawpdbs/', './receptor/', whichones, '_raw.pdb', '_modified.pdb', algchoice)
        else:
            prepareprot_scaffold('./receptor/', './receptor/', whichones, '.pdb', '_modified.pdb', algchoice)
    else:
        print ('You have not provided correct receptor name. \nEnter "all" as an argument for all receptor results or \ntype one of the following receptor names after -pp argument: ')
        print(reclist)
    
def autodock(whichones, reclist):
    exhaustiveness = input("What should be the exhaustiveness (Default is 8) level ?: ")
    try:
        exhaustiveness = int(exhaustiveness)
    except ValueError:
        try:
            exhaustiveness = int(float(exhaustiveness))
        except ValueError:
            exhaustiveness = 8
            print("Your input is not a number. It's a string. We chose 8 for the exhaustiveness.\n")

    if whichones == "all":
        for receptor in reclist:
            alllines=[]
            with open(f'grid_{receptor}.txt') as f:
                alllines = [line.split() for line in f]
            size_x = alllines[2][1]
            size_y = alllines[2][2]
            size_z = alllines[2][3]
            center_x = alllines[3][1]
            center_y = alllines[3][2]
            center_z = alllines[3][3]
            subprocess.call(shlex.split(f'./autodock.sh {receptor} {size_x} {size_y} {size_z} {center_x} {center_y} {center_z} {exhaustiveness}'))
        print ('Autodock Job done...')
    elif whichones in reclist:
        subprocess.call(shlex.split(f'./autodock.sh {whichones} {size_x} {size_y} {size_z} {center_x} {center_y} {center_z} {exhaustiveness}'))
    else:
        print ('You have not provided correct receptor name. \nEnter "all" as an argument for all receptor results or \ntype one of the following receptor names after -ad argument: ')
        print(reclist)

def get_search_query():
    searchquery = input(
    f'''\nYou can search for a certain kind of ligands using this tool.

Type search term here: '''
        )
    searchstring = ""
    for term in searchquery.split(' '):
        searchstring += term+'%20'
    searchstring = searchstring.strip()[:-3].strip()
    return searchstring

def searchchembl():
    searchstring = get_search_query()
    searchlink = f"https://www.ebi.ac.uk/chembl/g/#search_results/all/query={searchstring}"
    webbrowser.open(searchlink) 

def info(reclist):
    with open("README.md", 'r') as file_in:
        mytext =""
        for line in file_in:
            mytext = mytext + str(line)
        print (mytext)
    
    print ('Dear User, \n')
    print ('You have following receptors in your receptor folder:')
    print (reclist,)
    print ('\n')
    print (
            '''Useful commands: 
            -s = Setup a linux system, 
            -d = Download setup files,
            -sc = Search Chembl database for ligands,
            -pp = Prepare protein receptors, 
            -p = Make pdbqts of all ligands, 
            -g = Create grid-box file for automatic site identification for docking by providing key amino acid residue numbers.
            -ad = Do autodock process, 
            -r = Compile results, 
            -dt = Make drug table for comparison,
            -i = Help and folder info. 
            You can add all / a receptor as addon parameters for specific action. \n'''
                        )

parser = argparse.ArgumentParser(description='Central commands for AutoDock Vina')
parser.add_argument('-r',
					'--results',
					nargs='+',
					help='Create results files')
parser.add_argument('-dt',
					'--drugtable',
					nargs='+',
					help='Create drugtable files')
parser.add_argument('-p',
					'--mkpdbqts',
					nargs='+',
					help='Create pdbqt files')
parser.add_argument('-d',
					'--download',
					nargs='+',
					help='Create all files')
parser.add_argument('-s',
					'--setup',
					nargs='+',
					help='Setup the system')
parser.add_argument('-pp',
					'--prepareprot',
					nargs='+',
					help='Prepare receptor proteins')
parser.add_argument('-ad',
					'--autodock',
					nargs='+',
					help='Prepare receptor proteins')
parser.add_argument('-g',
					'--makegrid',
					nargs='+',
					help='Create grid box file for docking site')
parser.add_argument('-sc',
					'--searchchembl',
                    action='store_true',
					help='Search chembl database')
parser.add_argument('-i',
					'--info',
                    action='store_true',
					help='Get info and help')
args = parser.parse_args()

def main():
	if args.results:
		reclist = mkreclist()
		results(sys.argv[2], reclist)
	elif args.drugtable:
		drugtable(sys.argv[2])
	elif args.mkpdbqts:
		mkpdbqts(sys.argv[2])
	elif args.download:
		download(sys.argv[2])
	elif args.setup:
		setup(sys.argv[2])
	elif args.prepareprot:
		reclist = mkreclist()
		prepareprot(sys.argv[2], reclist)
	elif args.autodock:
		reclist = mkreclist()
		autodock(sys.argv[2], reclist)
	elif args.info:
		reclist = mkreclist()
		info(reclist)
	elif args.makegrid:
		reclist = mkreclist()
		makegrid(sys.argv[2], reclist)
	elif args.searchchembl:
		searchchembl()

if __name__ == '__main__': 
	main()