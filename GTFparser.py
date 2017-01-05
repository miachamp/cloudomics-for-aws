#!/usr/bin/env python
#Mia D. Champion
#OMICSLander v1.0 August, 2015

import os,sys,re

class Gtf(object):
    
    def __init__(self, gtf_line):
        self.gtf_list = gtf_line
        self.seqname, self.source, self.feature, self.start, self.end, self.score, self.strand, self.frame, self.attribute = gtf_line  
        self.attribute = dict(
            map(lambda x: re.split('\s+', x.replace('"', '')),
                re.split('\s*;\s*', self.attribute.strip().strip(';'))))  # convert attrs to dict

        self.start, self.end = int(self.start), int(self.end)
        
    def __str__(self):
        return '\t'.join(self.gtf_list) + '\n'


def gtf_reader(file_name, output):    
    gtf_list = []
    with open(file_name) as handle:
        for gtf_line in handle:
            gtf_line=str(gtf_line).strip().rstrip().split("\t")
            gtf = Gtf(gtf_line)
            if gtf.feature.lower() == 'transcript':
                gtf_list.append(gtf)
    gtf_list.sort(key=lambda x: (x.seqname, x.attribute['gene_id'], x.attribute['transcript_id'], x.start, x.end))

    # write the contents back to a file
    
    with open(output, 'wb') as write_handle:
        write_handle.write("gene\ttranscripts\n")
        for gtf_obj in gtf_list:
            outparse=str(gtf_obj).strip().rstrip().split("\t")
            annot=str(outparse[8]).split(";")
            #gtfcoord=str(outparse[0]).strip().rstrip()+"\t"+str(outparse[3]).strip().rstrip()+"\t"+str(outparse[4]).strip().rstrip()+"\t"+str(annot[0]).replace("gene_id","").replace("\"","")+"\t"+str(annot[1]).replace("transcript_id","").replace("\"","")+"\n"
            gtfcoord=str(annot[0]).strip().rstrip().replace(" ","").replace("gene_id","").replace("\"","")+"\t"+str(annot[1]).strip().rstrip().replace("transcript_id","").replace(" ","").replace("\"","")+"\n"
            write_handle.write(str(gtfcoord))


if __name__ == '__main__':
        print 'flag for gtf parse.'