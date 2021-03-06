#!/usr/bin/env python
#Mia D. Champion
#OMICSLander v1.0 August, 2015

""" 
OMICS-LANDER: Cloud-application for Identification of Genomic Regions of Epigenomic and Co/Post-Transcriptional Deregulation

"""

import sys, os, re, glob
import pandas as pd
pd.set_option('display.max_rows', None)
import Utils
from Utils import Build_Matrix

################################################################################
dir_path = ("/home/hadoop/")
sys.path.append(dir_path+"/Code/")
CODE=dir_path+"/Code"

DATA=glob.glob(os.path.join(dir_path, 'cloud*'))
DATA=str(DATA).replace('\'','').replace('[','').replace(']','')

############################ Annotate GeneList_File#############################
GeneList_file=(DATA+"/MatrixGeneList.txt")

for TrxCntInFile in glob.glob(os.path.join(DATA, '*TrxCount.txt')):
   (PATH, TxINFILENAME)=os.path.split(TrxCntInFile)
   (Shortname, Extension)=os.path.splitext(TxINFILENAME)
   Short_tag=Shortname.strip().split(".")
   intag=str(Short_tag[0])
   
   Build_Matrix(GeneList_file, TrxCntInFile, intag)
   
for PkCntInFile in glob.glob(os.path.join(DATA, 'AllNormVTumPeakDelta.txt')):
   (PATH, PkINFILENAME)=os.path.split(PkCntInFile)
   (Shortname, Extension)=os.path.splitext(PkINFILENAME)
   Short_tag=Shortname.strip().split(".")
   intag=str(Short_tag[0])
   
   Build_Matrix(GeneList_file, PkCntInFile, intag)
    
   
################## Process Data for Heatmap ####################################
"""
GeneList_file=(DATA+"/MatrixGeneList.txt")    
for InFile in glob.glob(os.path.join(DATA, 'Pairwise_*_DESeqForHeatMap.txt')):
    (PATH, INFILENAME)=os.path.split(InFile)
    (Shortname, Extension)=os.path.splitext(INFILENAME)
    Short_tag=Shortname.strip().split("_")
    intag=str(Short_tag[1])
   
    Build_HM_Matrix(GeneList_file, InFile, intag)
"""    
################################################################################

