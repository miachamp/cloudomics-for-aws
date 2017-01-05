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
#sys.path.append(dir_path+"/Code/")
#DATA=dir_path+"/mdc002"

DATA=glob.glob(os.path.join(dir_path, 'cloud*'))
DATA=str(DATA).replace('\'','').replace('[','').replace(']','')
#print DATA

#if not os.path.exists('outputs'):
#   os.mkdir(DATA+"/outputs")
#else:
#   []
   
#outputs=(dir_path+"/outputs")

import GTFparser
from GTFparser import gtf_reader
from operator import itemgetter
import itertools as IT
from itertools import groupby
import CSVcmpre
from CSVcmpre import CmpreVar, CmpreVar_reader, CmpreVar_reporter, PeakParser, summary
################################################################################

####  Grep regions of interest from Tumor me enrichment data
####  Identify Tumor-unique, RNA-unique variations ############   

#### Get Delta Regions for NvsT epigenetic changes across all samples ##########

TumData=[]
NormData=[]

   
for Tumor_Me_file in glob.glob(os.path.join(DATA, 'T*peak*.csv')):
   (PATH, TmeFILENAME)=os.path.split(Tumor_Me_file)
   (Shortname, Extension)=os.path.splitext(TmeFILENAME)
   Short_tag=Shortname.strip().split(".")
   tag=str(Short_tag[0])
   
   with open(Tumor_Me_file, 'r') as TumMefile:
      next(TumMefile)
      for TumMefile_line in TumMefile:
         TumMefile_line=str(TumMefile_line).strip().rstrip().split("\t")
         TumMefn_line=PeakParser(TumMefile_line)
         TumDataRes=(TumMefn_line.gene, int(TumMefn_line.region))
         if TumDataRes not in TumData:
            TumData.append(TumDataRes)
         else:
            []
   
   for Normal_Me_file in glob.glob(os.path.join(DATA, 'N*'+tag[1:]+'*peak*.csv')):
      (PATH, NmeFILENAME)=os.path.split(Normal_Me_file)

      with open(Normal_Me_file, 'r') as NormMefile:
         next(NormMefile)
         for NormMefile_line in NormMefile:
            NormMefile_line=str(NormMefile_line).strip().rstrip().split("\t")
            NormMefn_line=PeakParser(NormMefile_line)
            NormDataRes=(NormMefn_line.gene, int(NormMefn_line.region))
            if NormDataRes not in NormData:
               NormData.append(NormDataRes)

pklngout=(DATA+"/AllNormVTumPeakDelta.txt")
with open(pklngout, 'w') as pklngout_handle:
   outheader=("Gene\tDeltaPeakRegion")
   pklngout_handle.write(outheader+"\n")
   
   TumResult={}
   NormResult=[]
   for Tgene, Tpeaktotal in summary(TumData, key=itemgetter(0), value=itemgetter(1)):
      Tres_row="%s\t%d" % (Tgene, Tpeaktotal)
      TumResult[Tgene]=Tpeaktotal
      
   for Ngene, Npeaktotal in summary(NormData, key=itemgetter(0), value=itemgetter(1)):
      Nres_row="%s\t%d" % (Ngene, Npeaktotal)
      Map=TumResult.get(Ngene)
      if Map is None:
         Map="0"
      else:
         Map
      Map=int(Map)
      Npeaktotal=int(Npeaktotal)
      DeltaPeak=abs(Map-Npeaktotal)
      pklngout_handle.write(Ngene+"\t"+str(DeltaPeak)+"\n")
 
############# Parse Counts of potentially novel transcripts ####################

for Tumor_Trx_file in glob.glob(os.path.join(DATA, 'T*transcripts.gtf')):
   (PATH, TTrxFILENAME)=os.path.split(Tumor_Trx_file)
   (Shortname, Extension)=os.path.splitext(TTrxFILENAME)
   Short_tag=Shortname.strip().split(".")
   tag=str(Short_tag[0])   
   Tumor_Trx_outfile=DATA+'/T'+tag[1:]+'.tranxONLY.gtf'
   gtf_reader(Tumor_Trx_file, Tumor_Trx_outfile)
         
   for Normal_Trx_file in glob.glob(os.path.join(DATA, 'N*'+tag[1:]+'*transcripts.gtf')):
      (PATH, NTrxFILENAME)=os.path.split(Normal_Trx_file)
      Normal_Trx_outfile=DATA+'/N'+tag[1:]+'.tranxONLY.gtf'
      gtf_reader(Normal_Trx_file, Normal_Trx_outfile)

