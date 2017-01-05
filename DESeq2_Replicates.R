source("http://bioconductor.org/biocLite.R")
biocLite("DESeq2")
biocLite("Biobase")

library(DESeq2)
library(Biobase)

setwd("/home/hadoop/mdc002")
dataTable<-read.table("GeneCounts.txt", sep="\t", header=TRUE, row.names=1)
$python$

##############  Running Group Replicates ########################
dds <- DESeqDataSetFromMatrix(countData = dataTable, colData=samples, design=~condition)
DSeq_dds<-DESeq(dds)
res<-results(DSeq_dds)

replx_result<-(res[order(res$padj),])
write.csv(replx_result, file="Replicates_DESeq.txt")
