import os
import sys
from pathlib import Path
import argparse
import subprocess
import shlex
from pymol.cgo import *
from pymol import cmd
import pymol
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
        subprocess.call(['./mkpdbqts.sh'])
        print ('Job done...')
    else:
        print ("Try giving the 'all' argument...")

def download(whichones):
    if whichones == "all":
        subprocess.call(['./download.sh'])
        print ('Job done...')
    else:
        print ("Try giving the 'all' argument...")

def setup(whichones):
    if whichones == "all":
        subprocess.call(['./setup.sh'])
        print ('Job done...')
    else:
        print ("Try giving the 'all' argument...")

def prepareprot_scaffold(preload, presave, receptor, postload, postsave):
    cmd.load(preload+receptor+postload)
    cmd.remove('resn HOH')
    cmd.h_add(selection='acceptors or donors')
    cmd.save(presave+receptor+postsave)
    subprocess.call(shlex.split(f'./prepareprot.sh {receptor}'))

def prepareprot(whichones, reclist):
    if whichones == "all":
        for receptor in reclist:
            if Path('./receptor/rawpdbs/'+receptor+'_raw.pdb').exists():
                processchoice = input("You have already processed the raw pdb, want to re-process? \nType 'raw' to re-process raw pdb or 'new' to process already processed file.\nType here: ")
                if processchoice == "new":
                    prepareprot_scaffold('./receptor/', './receptor/', receptor, '.pdb', '_modified.pdb')
                else:
                    prepareprot_scaffold('./receptor/rawpdbs/', './receptor/', receptor, '_raw.pdb', '_modified.pdb')
            else:
                prepareprot_scaffold('./receptor/', './receptor/', receptor, '.pdb', '_modified.pdb')
        print ('Protein pdbqt file prepared...')
    elif whichones in reclist:
        if Path('./receptor/rawpdbs/'+whichones+'_raw.pdb').exists():
            processchoice = input("You have already processed the raw pdb, want to re-process? \nType 'raw' to re-process raw pdb or 'new' to process already processed file.\nType here: ")
            if processchoice == "new":
                prepareprot_scaffold('./receptor/', './receptor/', whichones, '.pdb', '_modified.pdb')
            else:
                prepareprot_scaffold('./receptor/rawpdbs/', './receptor/', whichones, '_raw.pdb', '_modified.pdb')
        else:
            prepareprot_scaffold('./receptor/', './receptor/', whichones, '.pdb', '_modified.pdb')
    else:
        print ('You have not provided correct receptor name. \nEnter "all" as an argument for all receptor results or \ntype one of the following receptor names after -pp argument: ')
        print(reclist)
    
def autodock(whichones, reclist):

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
            subprocess.call(shlex.split(f'./autodock.sh {receptor} {size_x} {size_y} {size_z} {center_x} {center_y} {center_z}'))
        print ('Autodock Job done...')
    elif whichones in reclist:
        subprocess.call(shlex.split(f'./autodock.sh {whichones} {size_x} {size_y} {size_z} {center_x} {center_y} {center_z}'))
    else:
        print ('You have not provided correct receptor name. \nEnter "all" as an argument for all receptor results or \ntype one of the following receptor names after -ad argument: ')
        print(reclist)

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
            -s = setup a linux system, 
            -d = download setup files, 
            -pp = prepare protein receptors, 
            -p = make pdbqts of all ligands, 
            -ad = do autodock process, 
            -r = compile results, 
            -dt = make drug table for comparison, 
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

if __name__ == '__main__': 
	main()