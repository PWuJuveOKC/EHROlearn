library("randomForest")

rm(list=ls())
setwd('/Users/Desktop/ITR/test/processed')
df = read.csv('window_df.csv',header=TRUE)

## negative the window_value
df$window_value <- -1 * df$window_value
row.names(df) <- df$patient_id

## reassign propensity score (observed TRT correspondingly)
df$pred_prob <- ifelse(df$group1 == 'onlysulf', df$pred_prob_s, df$pred_prob_i)
df1 <- subset(df, select = - c(patient_id,pred_prob,pred_prob_i,pred_prob_s) )


## Inverse Probability Weight
df1$complete<- ifelse(is.na(df1$window_value) , 'incomplete', 'complete'  )
df_ipw <- subset(df1, select = -c(group1,window_value))

## run RF ntree = 1000
set.seed(123)
ipw.rf <- randomForest(factor(complete) ~ ., data = df_ipw,ntree = 1000, importance=TRUE)
## predicted probabilities
prob <- predict(ipw.rf,type='prob')[,1]
ipweight <- 1/prob

## complete case and remove TRT 
df_window <- subset(df1, !is.na(window_value))  ## 106 obs
df_window <- subset(df_window, select = -c(group1,complete))


## RF regression to compute residuals
set.seed(123)
window.fit <- randomForest(window_value ~ ., data = df_window, ntree = 1000,importance=TRUE)
window_imp <- data.frame(importance(window.fit,type=1))

## residual calculation
pred <- predict(window.fit)
res <- df_window$window_value - pred
abs_res <- abs(res)
df_window$abs_res <- abs_res
df_window$res <- res



df$ipweight <- ipweight
df_temp <- df
df_temp <- subset(df_temp, !is.na(window_value))
df_temp$res <- res
df_temp$abs_res <- abs_res

## switch class label
df_temp$group1 <- ifelse(df_temp$group1=='onlysulf',1,-1)
df_temp$group_new <- sign(df_temp$group1 *df_temp$res)

## weight calculation
df_temp$weight <- df_temp$ipweight * df_temp$abs_res / df_temp$pred_prob 


df_temp$group_new <- ifelse(df_temp$group_new == 1, 'onlysulf','onlyinsulin')
df_temp$group1 <- ifelse(df_temp$group1 == 1, 'onlysulf','onlyinsulin')
df_weight <- subset(df_temp, weight <= quantile(weight,0.95))

write.csv(df_weight,file='df_weight_RF_neg.csv')
