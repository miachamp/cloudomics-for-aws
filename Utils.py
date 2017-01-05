#!/usr/bin/env python
##Mia D. Champion
#OMICSLander v1.0 August, 2015

import os, sys, re
import glob

dir_path = ("/home/hadoop/")
sys.path.append(dir_path+"/Code/")
DATA=glob.glob(os.path.join(dir_path, 'cloud*'))
DATA=str(DATA).replace('\'','').replace('[','').replace(']','')

####################### Build Matrix ###########################################

def Build_Matrix(GeneList_file, InFile, intag):
    masterGenes=[]
    with open(GeneList_file) as MasterGenes:
	masterGenes=[]
	for line in MasterGenes:
		line=line.rstrip()
		vals=line.split("\t")
		gn1=str(vals[0]).strip().rstrip()
		if gn1 not in masterGenes:
		    masterGenes.append(gn1)
    
    out_filename=InFile+'.'+'output'
    out_file=open(out_filename,'w')
    
    isolate_file=open(InFile)
    isolate_lines=isolate_file.readlines()
    
    GENEs={}
    #out_file.write(">"+ intag+"\n")
    for line in isolate_lines:
	x=line.split("\t")
	gn2=str(x[0:1]).strip().rstrip().replace("[","").replace("]","").replace("\'","").replace("\\n","")
	count=str(x[1:2]).strip().rstrip().replace("[","").replace("]","").replace("\'","").replace("\\n","")
	GENEs[gn2]=count
	
    for gene in masterGenes:
	Map=GENEs.get(gene)
	if Map is not None:
	    out_file.write(str(Map)+"\n")
	else:
	    out_file.write("0"+"\n")
    isolate_file.close()
    out_file.close()

################################################################################

