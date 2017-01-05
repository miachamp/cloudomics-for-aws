#!/usr/bin/env python
#Mia D. Champion
#OMICSLander v1.0 August, 2015

""" 
OMICS-LANDER: Cloud-application for Identification of Genomic Regions of Epigenomic and Co/Post-Transcriptional Deregulation

"""

import sys, os, re, glob
import pandas as pd
pd.set_option('display.max_rows', None)

################################################################################
dir_path = ("/home/hadoop/")
sys.path.append(dir_path+"/Code/")

DATA=glob.glob(os.path.join(dir_path, 'cloud*'))
DATA=str(DATA).replace('\'','').replace('[','').replace(']','')

################################################################################

################################################################################
############ get transcript counts N vs T across all samples ###################

for Tumor_Trx_outfile in glob.glob(os.path.join(DATA, 'T*tranxONLY.gtf')):
   (PATH, TTrxoutFILENAME)=os.path.split(Tumor_Trx_outfile)
   (Shortname, Extension)=os.path.splitext(TTrxoutFILENAME)
   Short_tag=Shortname.strip().split(".")
   tag=str(Short_tag[0])   
   
   header_row=['gene', 'transcripts']
   reportIN = pd.read_csv(Tumor_Trx_outfile,delim_whitespace=True,names=header_row, usecols=['gene', 'transcripts'])
   new_reportIN=reportIN.drop_duplicates()
   
   Tcount=new_reportIN.groupby(['gene']).size()
   Tcount.to_csv(DATA+"/TumTrxCount.txt", sep='\t', encoding='utf-8') 
   
   for Normal_Trx_outfile in glob.glob(os.path.join(DATA, 'N*'+tag[1:]+'*tranxONLY.gtf')):
      nheader_row=['gene', 'transcripts']
      nreportIN = pd.read_csv(Normal_Trx_outfile,delim_whitespace=True,names=header_row, usecols=['gene', 'transcripts'])
      Nnew_reportIN=nreportIN.drop_duplicates()
   
      Ncount=Nnew_reportIN.groupby(['gene']).size()
      Ncount.to_csv(DATA+"/NormTrxCount.txt", sep='\t', encoding='utf-8') 


    
