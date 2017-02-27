setwd('/Users/Desktop/ITR/test/processed')

library("randomForest")
library("Hmisc")
library("reshape2")


rm(list=ls())
df <- read.csv('df_RF_updated.csv',header=TRUE)

row.names(df) <- df$patient_id
df <- subset(df, select = - c(patient_id) )


## impute using RF and run RF on imputed dataset
set.seed(123)
df_new <- rfImpute(group1 ~ ., ntree=300,data = df)

## run RF ntree = 1000
set.seed(123)
fit.rf <- randomForest(group1 ~ ., data = df_new,ntree = 1000, importance=TRUE)

## predicted probabilities
pred_prob <- predict(fit.rf,type='prob')

## importance
imp <- data.frame(importance(fit.rf,type=1))
colnames(imp) <- "score"
imp$variable <- rownames(imp)
imp_f <- imp[order(- imp$score),][1:50,]

df_new$pred_prob <- pred_prob[,2]

df_new$pred_prob_s <- pred_prob[,2]
df_new$pred_prob_i <- pred_prob[,1]

write.csv(df_new,file='df_new_RF.csv')


df_new <- read.csv('df_new_RF.csv')

## divide propensity score into 4 quartiles
df_new$strata <- 1
df_new$strata[(df_new$pred_prob < quantile(df_new$pred_prob,0.5)) & 
                (df_new$pred_prob >= quantile(df_new$pred_prob,0.25))] <- 2
df_new$strata[(df_new$pred_prob < quantile(df_new$pred_prob,0.75)) & 
                (df_new$pred_prob >= quantile(df_new$pred_prob,0.5))] <- 3
df_new$strata[(df_new$pred_prob < 1) & 
                (df_new$pred_prob >= quantile(df_new$pred_prob,0.75))] <- 4
table(df_new$strata)





###############################################################
########## mean based on strata by group ##############
###############################################################

df1 <- subset(df_new, strata == 1)
df2 <- subset(df_new, strata == 2)
df3 <- subset(df_new, strata == 3)
df4 <- subset(df_new, strata == 4)


#### continous feature
## overall_hb_mean
t.test(overall_hb_mean ~ group1, data = df1)
t.test(overall_hb_mean ~ group1, data = df2)
t.test(overall_hb_mean ~ group1, data = df3)
t.test(overall_hb_mean ~ group1, data = df4)


#### count features

##  bp.S._medium_medium_new
df1_1 = subset(df1, bp.S._medium_medium_ind == 1)
df1_2 = subset(df2, bp.S._medium_medium_ind == 1)
df1_3 = subset(df3, bp.S._medium_medium_ind == 1)
df1_4 = subset(df4, bp.S._medium_medium_ind == 1)

t.test( bp.S._medium_medium_new ~ group1, data = df1_1)
t.test( bp.S._medium_medium_new ~ group1, data = df1_2)
t.test( bp.S._medium_medium_new ~ group1, data = df1_3)
t.test( bp.S._medium_medium_new ~ group1, data = df1_4)



#### dummy features

## bp.S._low_long_ind
df1_1 = subset(df1, group1 =='onlysulf')
df1_2 = subset(df1, group1 == 'onlyinsulin')
x1 <- c(sum(df1_1$bp.S._low_long_ind), (length(df1_1$bp.S._low_long_ind)- sum(df1_1$bp.S._low_long_ind)))
x2 <- c(sum(df1_2$bp.S._low_long_ind), (length(df1_2$bp.S._low_long_ind)- sum(df1_2$bp.S._low_long_ind)))
p1 = sum(df1_1$bp.S._low_long_ind) / length(df1_1$bp.S._low_long_ind)
p2 = sum(df1_2$bp.S._low_long_ind) / length(df1_2$bp.S._low_long_ind)
x <- matrix(c(x1,x2),nrow=2)
fisher.test(x)

df1_1 = subset(df2, group1 =='onlysulf')
df1_2 = subset(df2, group1 == 'onlyinsulin')
x1 <- c(sum(df1_1$bp.S._low_long_ind), (length(df1_1$bp.S._low_long_ind)- sum(df1_1$bp.S._low_long_ind)))
x2 <- c(sum(df1_2$bp.S._low_long_ind), (length(df1_2$bp.S._low_long_ind)- sum(df1_2$bp.S._low_long_ind)))
p1 = sum(df1_1$bp.S._low_long_ind) / length(df1_1$bp.S._low_long_ind)
p2 = sum(df1_2$bp.S._low_long_ind) / length(df1_2$bp.S._low_long_ind)
x <- matrix(c(x1,x2),nrow=2)
fisher.test(x)


df1_1 = subset(df3, group1 =='onlysulf')
df1_2 = subset(df3, group1 == 'onlyinsulin')
x1 <- c(sum(df1_1$bp.S._low_long_ind), (length(df1_1$bp.S._low_long_ind)- sum(df1_1$bp.S._low_long_ind)))
x2 <- c(sum(df1_2$bp.S._low_long_ind), (length(df1_2$bp.S._low_long_ind)- sum(df1_2$bp.S._low_long_ind)))
p1 = sum(df1_1$bp.S._low_long_ind) / length(df1_1$bp.S._low_long_ind)
p2 = sum(df1_2$bp.S._low_long_ind) / length(df1_2$bp.S._low_long_ind)
x <- matrix(c(x1,x2),nrow=2)
fisher.test(x)

df1_1 = subset(df4, group1 =='onlysulf')
df1_2 = subset(df4, group1 == 'onlyinsulin')
x1 <- c(sum(df1_1$bp.S._low_long_ind), (length(df1_1$bp.S._low_long_ind)- sum(df1_1$bp.S._low_long_ind)))
x2 <- c(sum(df1_2$bp.S._low_long_ind), (length(df1_2$bp.S._low_long_ind)- sum(df1_2$bp.S._low_long_ind)))
p1 = sum(df1_1$bp.S._low_long_ind) / length(df1_1$bp.S._low_long_ind)
p2 = sum(df1_2$bp.S._low_long_ind) / length(df1_2$bp.S._low_long_ind)
x <- matrix(c(x1,x2),nrow=2)
fisher.test(x)

