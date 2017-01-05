source("http://bioconductor.org/biocLite.R")
biocLite("DESeq2")
biocLite("Biobase")

library(DESeq2)
library(Biobase)

setwd("/home/hadoop/mdc002")
#dataTable<-read.table("GeneCounts.txt", sep="\t", header=TRUE, row.names=1)
$dTbl$
$python$


## Simon Anders : running comparisons without replicates ########

dds <- DESeqDataSetFromMatrix(countData = dataTable, colData=samples, design=~condition)
#rld <- rlogTransformation( dds) #,blind = TRUE)
rld <- rlogTransformation( dds)
res <- data.frame(
  assay(rld), 
  avgLogExpr = ( assay(rld)[,2] + assay(rld)[,1] ) / 2,
  rLogFC = assay(rld)[,2] - assay(rld)[,1] )

pairwise_result<-( res[ order(res$rLogFC), ] )

$outpyth$
