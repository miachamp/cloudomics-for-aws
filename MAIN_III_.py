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

####  generate R scripts for DESeq2 ############################################


DESeq_file=DATA+"/GeneCounts.txt"
DESeqRepScript=CODE+"/DESeq2_Replicates.R"
DESeqNoRepScript=CODE+"/DESeq2_NoReplicates.R"

headers=1
DESeqIn=open(DESeq_file,'r')
NormSamples=[]
TumSamples=[]
for i in range(headers):
   samples_header=DESeqIn.next().strip()
   cols=samples_header.split("\t")
   for i in range(1,len(cols)):
      if 'N' in cols[i]:
         NormSamples.append(cols[i])
      elif 'T' in cols[i]:
         TumSamples.append(cols[i])
         
New_Dict={}
keys=NormSamples
values=TumSamples
New_Dict=dict(zip(keys, values))

myKeys=list(sorted(New_Dict.keys()))
myKeys=str(myKeys).strip().rstrip().replace("[","").replace("]","").replace("\'","\"").replace(" ","")
myValues=list(sorted(New_Dict.values()))
myValues=str(myValues).strip().rstrip().replace("[","").replace("]","").replace("\'","\"").replace(" ","")

lenKeys=str(len(keys))
lenVals=str(len(values))

Rcodeline="samples<-data.frame(row.names=c("+myKeys+","+myValues+"), condition=as.factor(c(rep(\"Norm\","+lenKeys+"),rep(\"Tum\","+lenVals+"))))"

from tempfile import mkstemp
from shutil import move
from os import remove, close


def replace(file_path, pattern, subst):
   #Create temp file
   fh, abs_path = mkstemp()
   with open(abs_path,'w') as new_file:
      with open(file_path) as old_file:
         for line in old_file:
            new_file.write(line.replace(pattern, subst))                     
   remove(file_path)
   move(abs_path, file_path)     

colpattern="$dTbl$"
pattern="$python$"
out_pattern="$outpyth$"
x=replace(DESeqRepScript, pattern, Rcodeline)     

last_key_col=len(keys)+1

for key,value in (sorted(New_Dict.iteritems())):
   
   Key_pos=((sorted(New_Dict.keys()).index(key)))+2
   Val_pos=((sorted(New_Dict.values()).index(value)))+last_key_col+1
   #print New_Dict.keys()
   col_NR_line="dataTable<-read.table((pipe(\"cut -f1,"+str(Key_pos)+","+str(Val_pos)+" GeneCounts.txt\")), sep=\"\\t\", header=TRUE, row.names=1)"
   #print col_NR_line
   new_NR_line="samples<-data.frame(row.names=c(\""+key+"\",\""+value+"\"), condition=as.factor(c(rep(\"Norm\",1),rep(\"Tum\",1))))"
   out_NR_line="write.csv(pairwise_result, file=\"Pairwise_"+key+"vs"+value+"_DESeq.txt\")"
   new_script=CODE+"/DESeq2_"+key[1:]+"_NoReplicates.R"
   filechk=DATA+"/tmp.txt"
   with open(new_script, 'w') as outscript_handle:
      with open(DESeqNoRepScript) as old_file:
         for line in old_file:
            outscript_handle.write(line.replace(colpattern, col_NR_line).replace(pattern, new_NR_line).replace(out_pattern, out_NR_line)) 
            with open (filechk, 'w') as filechk_handle:
               filechk_handle.write("all done")
               filechk_handle.close()
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      