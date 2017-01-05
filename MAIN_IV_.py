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
CODE=dir_path+"/Code"

DATA=glob.glob(os.path.join(dir_path, 'cloud*'))
DATA=str(DATA).replace('\'','').replace('[','').replace(']','')

################################################################################
# Build matrices of DESeq and epigenetic outputs for R visualization 
################################################################################

# parse gene and geneId # from genecount orig file

GeneIdMap={}
origGeneCount=(DATA+'/myGeneCounts.txt')
with open(origGeneCount, 'r') as ogcFN_handle:
   for line in ogcFN_handle:
      line=str(line).strip().rstrip().split("\t")
      GeneName=str(line[0]).strip().rstrip()
      GeneId=str(line[1]).strip().rstrip()
      GeneIdMap[GeneId]=GeneName
  
#process replicate DESeq 
  
DESeqReplxout=(DATA+"/ReplicatesForHeatmap.txt")
DESeqReplx=(DATA+"/Replicates_DESeq.txt")
with open (DESeqReplx, 'r') as DESeqReplx_handle:
   with open (DESeqReplxout, 'w') as DESeqReplxout_handle:
      for rec in DESeqReplx_handle:
         rec=str(rec).strip().rstrip().split(",")
         DESeqReplxId=str(rec[0]).replace("\"","")
         Map=GeneIdMap.get(DESeqReplxId)
         DESeqReplxout_handle.write(str(Map).strip().rstrip().replace("\"","").replace("None","Gene")+'\t'+str(rec[2]).strip().rstrip().replace("\"","")+"\n")
         
#iterate through pairwise DESeq files
#map gene to # and build matrix of rLogFC (last column) (use file id tag as col header)
   
for PairwiseDESeqIN in glob.glob(os.path.join(DATA, 'Pairwise*DESeq.txt')):
   (PATH, PDESeqFILENAME)=os.path.split(PairwiseDESeqIN)
   (Shortname, Extension)=os.path.splitext(PDESeqFILENAME)
   Short_tag=Shortname.strip().split("_")
   tag=str(Short_tag[1])
   
   out_header=[]
   PWDESeqout=(DATA+"/Pairwise_"+tag+"_DESeqForHeatMap.txt")
   with open(PairwiseDESeqIN, 'r') as PWDESeq_handle:
      with open(PWDESeqout, 'w') as PWDESeqout_handle:
         outheader=("Gene\t"+tag+"_rLogFC")
         PWDESeqout_handle.write(outheader+"\n")
         next(PWDESeq_handle)
         for PWDESeq_line in PWDESeq_handle:
            PWDESeq_line=str(PWDESeq_line).strip().rstrip().split(",")
            PWDESeqId=str(PWDESeq_line[0]).replace("\"","")      
            PWMap=GeneIdMap.get(PWDESeqId)
            PWDESeqout_handle.write(str(PWMap).strip().rstrip().replace("\"","")+"\t"+str(PWDESeq_line[4])+"\n")
            Chkout=(DATA+"/mainiv.txt")
            with open(Chkout, 'w') as chkout_handle:
               chkout_handle.write("all done")
            chkout_handle.close()
   
   
   
   