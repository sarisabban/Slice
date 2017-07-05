#!/usr/bin/python3

import os , sys

def Slice(PDB_ID , Chain , From , To):
	''' This function downloads a spesific protein from RCSB and isolates a specific user defined continuous sequence from it '''
	''' Generates the structure.pdb file '''
	#Get the protein
	os.system('wget http://www.rcsb.org/pdb/files/' + PDB_ID + '.pdb')
	pdb = open(PDB_ID + '.pdb' , 'r')
	#Isolate the structure
	structure = open('structure.pdb' , 'w')
	count = 0
	num = 0
	AA2 = None
	for line in pdb:
		if not line.startswith('ATOM'):				#Ignore all lines that do not start with ATOM
			continue
		if not line.split()[4] == Chain:			#Ignore all lines that do not have the specified chain (column 5)
			continue
		if str(From) <= line.split()[5] <= str(To):		#Find all residues within the user specified location
			count += 1					#Sequencially number atoms
			AA1 = line[23:27]				#Sequencially number residues
			if not AA1 == AA2:
				num += 1
			#Update each line of the file to have its atoms and residues sequencially labeled, as well as being in chain A
			final_line = line[:7] + '{:4d}'.format(count) + line[11:17] + line[17:21] + 'A' + '{:4d}'.format(num) + line[26:]
			AA2 = AA1
			structure.write(final_line)			#Write to new file called structure.pdb
	structure.close()
	os.remove(PDB_ID + '.pdb')					#Keep working directory clean, remove the protein's original file
#----------------------------------------------------------------------------------------------------------------------------
Protein		= sys.argv[1]
Chain		= sys.argv[2]
From		= sys.argv[3]
To		= sys.argv[4]

Slice(Protein , Chain , From , To)
