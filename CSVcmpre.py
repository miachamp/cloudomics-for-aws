#!/usr/bin/env python
#Mia D. Champion
#OMICSLander v1.0 August, 2015

""" 
OMICS-LANDER: Cloud-application for Identification of Genomic Regions of Epigenomic and Co/Post-Transcriptional Deregulation

"""

import sys, os, re, glob
import pandas as pd
pd.set_option('display.max_rows', None)
from operator import itemgetter
import itertools as IT
from itertools import groupby

################################################################################
dir_path = ("/home/hadoop/")
sys.path.append(dir_path+"/Code/")

DATA=glob.glob(os.path.join(dir_path, 'cloud*'))
DATA=str(DATA).replace('\'','').replace('[','').replace(']','')

#################################  Variation Cmpre #############################

class PeakParser(object):
   def __init__(self, PeakParser_line):
      self.PeakParser_list = PeakParser_line
      self.chr, self.start, self.stop, self.gene, self.region = PeakParser_line
      
   def __str__(self):
      return '\t'.join(self.PeakParser_list) + '\n'
      
class CmpreVar(object):
   """
   Separates out csv parsing from iterating over records for variation records
   """
   def __init__(self, varcsv_line):
      self.varcsv_list = varcsv_line
      self.chr, self.pos, self.ref, self.alt, self.compressed, self.score = varcsv_line  
      
   def __str__(self):
      return '\t'.join(self.varcsv_list[0:4]) + '\n'
      
def CmpreVar_reader(Normal_file_name, Tumor_file_name, outfile):    #Output Tumor only variations as a score of '0', matches are scored as '1'
   score_list = []
   Norm_IN=pd.read_csv(Normal_file_name, sep="\t",usecols=["chr","pos","ref","alt"])
   Tum_IN=pd.read_csv(Tumor_file_name, sep="\t",usecols=["chr","pos","ref","alt"])
   
   Tum_IN['compressed']=Tum_IN.apply(lambda x:'%s%s' % (x['chr'],x['pos']),axis=1)
   Norm_IN['compressed']=Norm_IN.apply(lambda x:'%s%s' % (x['chr'],x['pos']),axis=1)
   Tum_IN['Success'] = Tum_IN['compressed'].isin(Norm_IN['compressed']).astype(int)
   
   Tum_IN.to_csv(outfile, index=False, sep='\t')
   #return Tum_IN

def CmpreVar_reporter(outfile, MatchesReport, UniqueReport):      #This is to report shared and unique variations between 2 files
   with open(outfile) as handle:
      TumNormMatches=[]
      TumorUnique=[]
      
      for res_line in handle:
         res_line=str(res_line).strip().rstrip().split("\t")
         result=CmpreVar(res_line)
         if result.score == '1' :
            TumNormMatches.append(result)
         elif result.score == '0' :
            TumorUnique.append(result)
         
      with open(MatchesReport, 'wb') as Matchwrite_handle:
         Matchwrite_handle.write("chr\tpos\tref\talt\n")
         for match_obj in TumNormMatches:
            Matchwrite_handle.write(str(match_obj).strip()+"\n")
            
      with open(UniqueReport, 'wb') as Tuniqouthandle:
         Tuniqouthandle.write("chr\tpos\tref\talt\n")
         for uniq_obj in TumorUnique:
            Tuniqouthandle.write(str(uniq_obj).strip()+"\n")
            
      Matchwrite_handle.close()
      Tuniqouthandle.close()

def summary(data, key=itemgetter(0), value=itemgetter(1)):

    for k, group in groupby(data, key):
        yield (k, sum(value(row) for row in group))

################################################################################

if __name__ == '__main__':
   print 'flag for gtf parse.'

   