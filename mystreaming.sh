#!/bin/bash

#Mia D. Champion
#OMICSLander v1.0 August, 2015
#use default python2.6


###################  PART II : STREAMING ######################################
cd /home/hadoop/Code
shopt -s nullglob
set -- cloud*
#if [ "$#" -gt 0 ]; then
#  ./script "$@" # call script with that list of files.
#fi
# Or with bash arrays so you can keep the arguments:
Bucket='omicslander'
clientID=( cloud*)

#lazy fix for R scripts
mkdir temp
chmod -R 755 temp
list='echo *R';for file in $list;do sed "s|mdc002|${clientID}|g" $file > ./temp/$file;done
mv ./temp/* .
rm -r temp
cd /home/hadoop/

################################################################################
cat /home/hadoop/$clientID/myGeneCounts.txt|awk -F $'\t' 'BEGIN {OFS = FS} {$1=""; print $0}'|sed 's/^\t//g' > /home/hadoop/$clientID/GeneCounts.txt

sudo python /home/hadoop/Code/MAIN_I_.py 
sudo python /home/hadoop/Code/MAIN_II_.py
sudo python /home/hadoop/Code/MAIN_III_.py

##############################################

sudo chmod 777 /home/hadoop/$clientID/tmp.txt

FILEchk=('/home/hadoop/'$clientID'/tmp.txt')
if [ -f $FILEchk ];
then
    list='echo /home/hadoop/Code/DESeq2_*_NoRep*R'; for file in $list; do sudo R CMD BATCH $file; done
    rm $FILEchk
    Replicates=('/home/hadoop/Code/DESeq2_Replicates.R')
    sudo R CMD BATCH $Replicates
else
    echo ""
fi

sudo python /home/hadoop/Code/MAIN_IV_.py
sudo chmod 755 /home/hadoop/$clientID/*
FILEchk2=('/home/hadoop/'$clientID'/mainiv.txt')
if [ -f $FILEchk2 ];
then
    cut -f1 /home/hadoop/$clientID/Pairwise_*_DESeqForHeatMap.txt > /home/hadoop/$clientID/genelist.out
    sudo rm $FILEchk2
    cat /home/hadoop/$clientID/genelist.out|sed -e '/^Gene$/d'|sort -n|sort -u > /home/hadoop/$clientID/MGeneList.txt
    sed '1 i\Gene' /home/hadoop/$clientID/MGeneList.txt > /home/hadoop/$clientID/MatrixGeneList.txt
    sudo rm /home/hadoop/$clientID/MGeneList.txt
    sudo rm /home/hadoop/$clientID/genelist.out
    
    ##############################################
    sudo python /home/hadoop/Code/MAIN_V_.py
    paste /home/hadoop/$clientID/NormTrxCount.txt.output /home/hadoop/$clientID/TumTrxCount.txt.output > /home/hadoop/$clientID/TkCounts.txt.output
    cat /home/hadoop/$clientID/TkCounts.txt.output|sed 's/\t/:/g'|sed '1d'|sed '1 i\trxNum' > /home/hadoop/$clientID/TxCounts.txt.output
    cat /home/hadoop/$clientID/AllNormVTumPeakDelta.txt.output|sed 's/^/ :(/g'|sed 's/$/)/g' > /home/hadoop/$clientID/PeakDelta.txt.output
    paste /home/hadoop/$clientID/MatrixGeneList.txt /home/hadoop/$clientID/PeakDelta.txt.output /home/hadoop/$clientID/TxCounts.txt.output > /home/hadoop/$clientID/FinMatrixGeneList.txt
    cat /home/hadoop/$clientID/FinMatrixGeneList.txt|sed 's/\t//g'|sed 's/ /\t/g'|sed '1d'|sed '1 i\Gene' > /home/hadoop/$clientID/AnnotMatrixGeneList.txt
else
    echo ""
fi

FILEchk3=('/home/hadoop/'$clientID'/AnnotMatrixGeneList.txt')
if [ -f $FILEchk3 ];
then
    sudo python /home/hadoop/Code/MAIN_VI_.py
    sudo chmod 755 /home/hadoop/$clientID/*
    paste /home/hadoop/$clientID/AnnotMatrixGeneList.txt /home/hadoop/$clientID/Pairwise*_*_*output > /home/hadoop/$clientID/PW_DESeq_Matrix.txt
    cat /home/hadoop/$clientID/PW_DESeq_Matrix.txt|sed 's/\t://g'|sed 's/\t/,/g' > /home/hadoop/$clientID/Pairwise_DESeq_Matrix.csv
    
    sudo rm /home/hadoop/$clientID/ReplicatesForHeatmap.txt
    sudo rm /home/hadoop/$clientID/PW_DESeq_Matrix.txt
    sudo rm /home/hadoop/$clientID/*.output
    sudo rm /home/hadoop/$clientID/MatrixGeneList.txt
    sudo rm /home/hadoop/$clientID/*TrxCount.txt
    sudo rm /home/hadoop/$clientID/*DESeqForHeatMap.txt
    sudo rm /home/hadoop/$clientID/*MatrixGeneList.txt
    sudo rm /home/hadoop/$clientID/AllNormVTumPeakDelta.txt
    sudo rm /home/hadoop/$clientID/GeneCounts.txt
    
    PairwiseIN=('/home/hadoop/Code/DESeq2_HeatMap_PW.R')
    sudo R CMD BATCH $PairwiseIN
else
    echo ""
fi

FILEchk4=('/home/hadoop/'$clientID'/Pairwise_Unsupervised_Cluster.png')
if [ -f $FILEchk4 ];
then
    sudo mv /home/hadoop/$clientID/*tranxONLY.gtf /home/hadoop/$clientID/outputs/
    sudo mv /home/hadoop/$clientID/*png /home/hadoop/$clientID/outputs/
    sudo mv /home/hadoop/$clientID/*DESeq* /home/hadoop/$clientID/outputs/
    hadoop fs -moveFromLocal /home/hadoop/$clientID/outputs s3://omicslander/$clientID/
else
    echo ""
fi
