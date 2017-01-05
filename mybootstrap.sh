#!/bin/bash

#Mia D. Champion
#OMICSLander v1.0 August, 2015
#use default python2.6

################## PART I : BOOTSTRAP FUNCTIONS ###############################
sudo pip install pandas
sudo pip install boto3

mkdir /home/hadoop/Code
sudo chmod 755 /home/hadoop/Code

hadoop fs -copyToLocal s3://omicslanderconfigs/Code/* /home/hadoop/Code/
hadoop fs -copyToLocal s3://omicslanderconfigs/cloud* /home/hadoop/Code/
hadoop fs -rm s3://omicslanderconfigs/cloud*

cd /home/hadoop/Code
config=('/home/hadoop/Code/*.txt')
if [ -f $config ];
then
    for file in *txt; do sudo mv "$file" "${file%.*}"; done
else
    echo ""
fi

cd /home/hadoop/
sudo chmod 755 /home/hadoop/Code/

cd /home/hadoop/Code
shopt -s nullglob
set -- cloud*
#if [ "$#" -gt 0 ]; then
#  ./script "$@" # call script with that list of files.
#fi
# Or with bash arrays so you can keep the arguments:
Bucket='omicslander'
clientID=( cloud*)
cd /home/hadoop/
mkdir /home/hadoop/$clientID
mkdir /home/hadoop/$clientID/outputs

sudo chmod -R 755 /home/hadoop/$clientID
sudo chmod -R 755 /home/hadoop/$clientID/outputs
sudo chmod -R 755 /usr/lib64/R/library

hadoop fs -copyToLocal s3://$Bucket/$clientID/$clientID.zip /home/hadoop/

cd /home/hadoop/
unzip /home/hadoop/$clientID.zip

origZip=('/home/hadoop/'$clientID'.zip')
if [ -f $origZip ];
then
    sudo rm $origZip
else
    echo ""
fi

#rm -r *zip
#rm -r __MACOSX


