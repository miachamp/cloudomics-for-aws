source("http://bioconductor.org/biocLite.R")
biocLite("DESeq2")
biocLite("Biobase")
biocLite("gplots")
biocLite("RColorBrewer")

library(DESeq2)
library(Biobase)
library(gplots)
library(RColorBrewer)

#########################################################

###################### heatmap ##########################

setwd("/home/hadoop/mdc002/")
data <- read.csv("Pairwise_DESeq_Matrix.csv", comment.char="#")

rnames <- data[,1]                            # assign labels in column 1 to "rnames"
mat_data <- data.matrix(data[,2:ncol(data)])  # transform column 2-5 into a matrix
rownames(mat_data) <- rnames                  # assign row names 

my_palette <- colorRampPalette(c("red", "black", "green"))(n = 299)

# creates an output image
png("Pairwise_Unsupervised_Cluster.png",      
  width = 5*300,        # 5 x 300 pixels
  #height = 5*300,
  height = 12*300,
  res = 300,            # 300 pixels per inch
  pointsize = 6)        # smaller font size

#####################################################
######### Unsupervised parameter settings ###########

row_distance = dist(mat_data, method = "manhattan")
row_cluster = hclust(row_distance, method = "ward.D2")
col_distance = dist(t(mat_data), method = "manhattan")
col_cluster = hclust(col_distance, method = "ward.D2")

#######################################################

NewMatrix<-mat_data[rev(row_cluster$labels[row_cluster$order]), col_cluster$labels[col_cluster$order]]
write.csv(NewMatrix, file="/home/hadoop/mdc002/Pairwise_DESeq_MatrixCLUSTERED.csv")

###############################################################################################

############ COMPLETE UNSUPERVISED ###########################################################
heatmap.2(as.matrix(mat_data), Rowv = as.dendrogram(row_cluster), Colv = as.dendrogram(col_cluster), col=my_palette, scale="row", key=T, keysize=0.3, margins =c(12,9), density.info="none", trace="none",labRow=rownames(mat_data), cexRow=0.5, cexCol=1.2, labCol=colnames(mat_data)) 


##############################################################################################

dev.off()
#####################################

