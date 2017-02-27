setwd('/Users/Desktop/ITR/test/processed')
library("gplots")
library("geneplotter")
library(RColorBrewer)


df <- read.csv('DF_cts_cluster.csv',header=TRUE)

## remove ids with too many missings
final <- df[!(is.na(df$bmi_low_long)),]
final <- final[!(is.na(final$bp.S._high_medium)),]
final <- final[!(is.na(final$bp.S._high_short)),]
final <- final[!(is.na(final$bp.D._medium_short)),]
final <- final[!(is.na(final$bp.S._medium_medium)),]
final <- final[!(is.na(final$ldl_low_medium)),] 
#final <- na.omit(df)

sul <- table(final$group1)[2]
ins <- table(final$group1)[1]

df <- final
names <- names(df)
scale_list <- names[1:79]
df_sort <- df[order(df$group1,decreasing=TRUE),]

levels(df_sort$group1) <- c(levels(df_sort$group1), "Metformin + Sulfonylureas")
levels(df_sort$group1) <- c(levels(df_sort$group1), "Metformin + Insulin")
df_sort$group1[df_sort$group1 == 'onlysulf'] <- 'Metformin + Sulfonylureas'
df_sort$group1[df_sort$group1 == 'onlyinsulin'] <- 'Metformin + Insulin'
df1 <- df_sort[scale_list]

row_names <- df1[,1]
row.names(df1) <- row_names
col_names <- colnames(df1)
df1 <- df1[2:79]
df1 <- scale(df1)

## Split the data and get the row cluster separately first
df_A <- df1[1:sul,]
df_B <- df1[(sul+1):dim(df1)[1],]


AA = heatmap.2(as.matrix(t(df_A)),
               distfun = dist,
               hclustfun = hclust,
               dendrogram="none",
               reorderfun=function(d, w) reorder(d, w, agglo.FUN = mean),
               na.rm = TRUE,
               trace="none",
               density.info="none",
               key=TRUE,
               keysize=1,
               
               na.color="white",
               ylab =  "Features",
               labCol="",
               offsetCol=0.5,
               srtRow = 45,
               margins=c(12,8),
               cexRow=0.5,
               cexCol=0.5,
)


BB = heatmap.2(as.matrix(t(df_B)),
               distfun = dist,
               hclustfun = hclust,
               dendrogram="col",
               reorderfun=function(d, w) reorder(d, w, agglo.FUN = mean),
               na.rm = TRUE,
               trace="none",
               density.info="none",
               key=TRUE,
               keysize=1,
               
               na.color="white",
               ylab =  "Features",
               labCol="",
               offsetCol=0.5,
               srtRow = 45,
               margins=c(12,8),
               cexRow=0.5,
               cexCol=0.5,
)


## combine the data
order_A <- rownames(df_A)[AA$colInd]
order_B <- rownames(df_B)[BB$colInd]
patient_id <- c(order_A,order_B)

df_new <- data.frame(patient_id)
df_ordered <- df_sort[match(patient_id, df_sort$patient_id),]


df_ord <- df_ordered[scale_list]
row_names <- df_ord[,1]
row.names(df_ord) <- row_names
col_names <- colnames(df_ord)
df_ord1 <- df_ord[2:79]

df_ord2 <- scale(df_ord1)
df3 <- t(df_ord2)

pdf("heatmap_1_updated.pdf", width=12, height=9)

my_palette <- colorRampPalette(c("dodgerblue4","forestgreen","yellow", "orange","darkorange2","red"))(1000)
# llmat = rbind(c(0,3),c(2,1),c(0,4))
# llwid = c(0,4)
# llhei = c(0,4,0.5)

heatmap.2(as.matrix(df3),
          distfun = dist,
          hclustfun = hclust,
          Colv=FALSE,
          dendrogram="none",
          reorderfun=function(d, w) reorder(d, w, agglo.FUN = mean),
          na.rm = TRUE,
          trace="none",
          density.info="none",
          key=TRUE,
          keysize=0.7,
          col=my_palette,
          breaks=c(seq(-1.5,1.5,0.003)),
          na.color="white",
          # ylab =  "Continuous and Count Features",
          labCol="",
          offsetCol=0.2,
          srtRow = 0,
          margins=c(5,9.2),
          cexRow=0.68,
          cexCol=0.5,
          ColSideColors=as.character(c(rep(5,sul),rep(6,ins))),
)

par(cex=0.7)
legend("topright",inset=c(0.01,-0.013),
       legend = unique(df_ordered$group1),
       col = c(5,6),
       lty= 1,
       lwd = 5,
       bty="n",
       text.font=1
)
dev.off()
