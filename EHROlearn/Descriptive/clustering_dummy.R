setwd('/Users/Desktop/ITR/test/processed')
library("gplots")
library("geneplotter")
library(RColorBrewer)

df <- read.csv('DF_ind_cluster.csv',header=TRUE)
names <- names(df)
ind_list <- names[c(1,3:20,2)]
df_sort <- df[order(df$group1,decreasing=TRUE),]

levels(df_sort$group1) <- c(levels(df_sort$group1), "Metformin + Sulfonylureas")
levels(df_sort$group1) <- c(levels(df_sort$group1), "Metformin + Insulin")
df_sort$group1[df_sort$group1 == 'onlysulf'] <- 'Metformin + Sulfonylureas'
df_sort$group1[df_sort$group1 == 'onlyinsulin'] <- 'Metformin + Insulin'
df1 <- df_sort[ind_list]

row_names <- df1[,1]
row.names(df1) <- row_names
col_names <- colnames(df1)
df1 <- df1[2:19]
df1 <- scale(df1)

## Split the data and get the row cluster separately first
df_A <- df1[1:237,]
df_B <- df1[238:368,]


AA = heatmap.2(as.matrix(t(df_A)),
               distfun = dist,
               hclustfun = hclust,
               dendrogram="none",
               reorderfun=function(d, w) reorder(d, w, agglo.FUN = mean),
               na.rm = TRUE,
               trace="none",
               density.info="none",
               col =c("white", "black"),
               na.color="blue",
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
               col=c("white","black"),
               na.color="blue",
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


df_ord <- df_ordered[ind_list]
row_names <- df_ord[,1]
row.names(df_ord) <- row_names
col_names <- colnames(df_ord)
df_ord1 <- df_ord[2:19]

df_ord2 <- scale(df_ord1)

df3 <- t(df_ord2)

key.xtickfun=function() {
  breaks <- parent.frame()$breaks
  return(list(
    at=parent.frame()$scale01(c(breaks[1],
                                breaks[length(breaks)])),
    labels=c(as.character(breaks[1]),
             as.character(breaks[length(breaks)]))
  ))
}

pdf("heatmap_2_updated.pdf", width=12, height=9)


heatmap.2(as.matrix(df3),
          distfun = dist,
          hclustfun = hclust,
          Colv=FALSE,
          dendrogram="none",
          reorderfun=function(d, w) reorder(d, w, agglo.FUN = mean),
          na.rm = TRUE,
          symkey = FALSE,
          keysize = 0.7,
          key.xtickfun=function() {
            breaks <- parent.frame()$breaks
            return(list(
              at=parent.frame()$scale01(c(breaks[1],
                                          breaks[length(breaks)])),
              labels=c(as.character(breaks[1]),
                       as.character(breaks[length(breaks)]))
            ))
          },
          breaks=c(0,0.5,1.0),
          trace="none",
          density.info="none",
          col=c("grey","black"),
          na.color="blue",
          # ylab =  "Dummy Features",
          labCol="",
          offsetCol=0.2,
          srtRow = 0,
          margins=c(5,9.2),
          cexRow=0.8,
          cexCol=0.5,
          ColSideColors=as.character(c(rep(5,237),rep(6,131))),
          colsep=1:ncol(df3),
          rowsep=1:nrow(df3)
)

par(cex=0.7)
legend("topright",inset=c(0.01,-0.014),
       legend = unique(df_ordered$group1),
       col = c(5,6),
       lty= 1,
       lwd = 5,
       bty="n",
       text.font=1
)
dev.off()
