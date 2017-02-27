import os
import pydot
from sklearn.externals.six import StringIO
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree
import random
from random import *
import numpy as np

df = pd.read_csv('df_weight_RF_neg.csv')

df.index = df['patient_id']
del df['Unnamed: 0']

df.window_value = -1 * df.window_value
df['newweight'] = df['ipweight'] / df['pred_prob']
sample_weights = df.newweight

del df['newweight']
del df['ipweight']
del df['abs_res']
del df['pred_prob']
del df['pred_prob_s']
del df['pred_prob_i']
del df['group_new']
del df['res']
del df['weight']


## create dummies for sklearn
dummy_sex = pd.get_dummies(df['sex'])

df_final = pd.concat([df,dummy_sex],axis=1,ignore_index=False)
del df_final['sex']
del df_final['F']

dummy_race = pd.get_dummies(df['race'])
del dummy_race['W']
dummy_race.columns = [['Race:B','Race:D','Race:O','Race:U']]

df_final = pd.concat([df_final,dummy_race],axis=1,ignore_index=False)
del df_final['race']

dummy_group = pd.get_dummies(df['group1'])
del dummy_group['onlyinsulin']
dummy_group.columns = [['Medication']]

df_final = pd.concat([df_final,dummy_group],axis=1,ignore_index=False)
del df_final['group1']



name_list = list(df_final)
name_left = [ x for x in name_list if (x[0:6] != 'length') & (x[0:6] != 'number') & (x[-3:] != 'ind')
              & (x[-3:] != 'new') & (x[0:7] != 'patient')]


name1 = [x for x in name_left if (x != 'window_value')]
df_temp = df_final[name1]

name2 = [x for x in name1 if (x != 'Medication')]

for item in name2:
    int =  'int_'+ item
    df_temp[int] = df_temp['Medication'] * df_temp[item]




############################ max depth = 5 ################################
###########################################################################
## reg tree built
clf = tree.DecisionTreeRegressor(random_state=123,min_samples_leaf=2,max_depth=2)

## features and response

name_left1 = [x for x in list(df_temp) if x != 'window_value']
X = df_temp[name_left1]
## rename some labels
X.rename(columns={'bp.D._low_long_new': 'DBP (low_long)', 'bp.S._low_medium_ind': 'SBP (low_medium) Extreme Dummy',
                         'hb_medium_medium_new': 'HbA1C (medium_medium)', 'length_obs_hdl': 'Length of HDL Observation',
                         'bp.D._high_long_new': 'DBP (high_long)', 'recent_hdl_mean': 'Recent HDL Mean',
                         'overall_bp.S._mean': 'Overall SBP Mean', 'overall_bmi_mean': 'Overall BMI Mean',
                         'hdl_medium_medium_new': 'HDL (medium_medium)', 'length_obs_bmi': 'Lenght of BMI Observation',
                         'overall_bmi_mean': 'Overall BMI Mean', 'hdl_medium_medium_new': 'HDL (medium_medium)',
                         'bp.S._high_short_new': 'SBP (high_short)', 'hb_low_short_ind': 'HbA1C (low_short) Extreme Dummy',
                         'bp.S._low_medium_new': 'SBP (low_medium)', 'overall_ldl_mean': 'Overall LDL Mean',
                         'recent_ldl_mean': 'Recent LDL Mean', 'bp.S._medium_medium_new':'SBP (medium_medium)',
                         'number_ldl_measure_new': 'Number of LDL Measures','length_obs_bp.D.': 'Length of DBP Observation',
                         'bmi_low_short_ind': 'BMI (low_short) Extreme Dummy', 'length_obs_bp.S.': 'Length of SBP Observation',
                         'bp.S._high_medium_new': 'SBP (high_medium)', 'bmi_low_short_ind': 'BMI (low_short)',
                         'recent_1stmonth_bp.S._mean': 'Recent One Month SBP Mean','length_obs_hb':'Length of HbA1C Observation',
                         'number_hb_measure_new': 'Number of HbA1C Measures','recent_1stmonth_bp.D._mean':'Recent One Month DBP Mean',
                         'bp.S._low_long_ind': 'SBP (low_long) Extreme Dummy', 'length_obs_bp.D.': 'Length of DBP Observation',
                         'dysth_latest_Post_Diag': 'Latest Dysthymic Disorder Diagnosis Post Treatment',
                         'recent_hb_mean': 'Recent HbA1C Mean', 'number_bp.S._measure_new': 'Number of SBP Measures',
                         'hdl_high_long_new': 'HDL (high_long)', 'overall_hb_mean': 'Overall HbA1C Mean',
                         'overall_bp.D._mean': 'Overall DBP Mean', 'hb_high_long': 'HbA1C (high_long) Extreme Dummy',
                         'bmi_high_short_new': 'BMI (high_short)', 'bp.S._medium_long_new':'SBP (medium_long)',
                         'bmi_low_long_ind': 'BMI (low_long) Extreme Dummy', 'hb_high_long_ind': 'HbA1C (high_long) Extreme Dummy',
                  'recent_bmi_mean': 'Recent BMI Mean','overall_hdl_mean': 'Overall HDL Mean', 'age': 'Age', 'M': 'Gender',
                  'rd_latest_Post_Diag': 'Recurrent Depression Diagnosis Post Treatment',
                  'int_overall_ldl_mean': 'Interaction with Overall LDL Mean',
                  'Race:O': 'Race (Other)', 'int_overall_bp.S._mean': 'Interaction with Overall SBP Mean',
                  'int_recent_ldl_mean': 'Interaction with Recent LDL Mean','int_recent_bmi_mean':'Interaction with Recent BMI Mean',
                  'int_overall_hb_mean': 'Interaction with Overall HbA1C Mean',
                  'int_overall_hdl_mean': 'Interaction with Overall HDL Mean',
                  'int_recent_hb_mean': 'Interaction with Recent HbA1C Mean',
                  'int_overall_bmi_mean': 'Interaction with Overall BMI Mean',
                  'int_age': 'Interaction with Age', 'int_recent_1stmonth_bp.D._mean' : 'Interaction with Recent One Month DBP Mean',
                  'int_overall_bp.D._mean': 'Interaction with Overall DBP Mean'}, inplace=True)


y = df_final['window_value']


fit1 = clf.fit(X, y, check_input=True,sample_weight=np.array(sample_weights),X_idx_sorted=None)


imp =fit1.feature_importances_

dot_data = StringIO()
tree.export_graphviz(fit1, feature_names=list(X),
                         filled=False, rounded=True,
                         special_characters=True, rotate=False,impurity=False,label="all",out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("Q_tree_depth_5_1.pdf")



####  A =1  predicted
X1 = df.copy()

## create dummies for sklearn
dummy_sex = pd.get_dummies(X1['sex'])

df_X1 = pd.concat([X1,dummy_sex],axis=1,ignore_index=False)
del df_X1['sex']
del df_X1['F']

dummy_race = pd.get_dummies(X1['race'])
del dummy_race['W']
dummy_race.columns = [['Race:B','Race:D','Race:O','Race:U']]

df_X1 = pd.concat([df_X1,dummy_race],axis=1,ignore_index=False)
del df_X1['race']

dummy_group = pd.get_dummies(X1['group1'])
del dummy_group['onlyinsulin']
dummy_group.columns = [['Medication']]

df_X1 = pd.concat([df_X1,dummy_group],axis=1,ignore_index=False)
del df_X1['group1']



df_X1.Medication =1

name_list = list(df_X1)
name_left = [ x for x in name_list if (x[0:6] != 'length') & (x[0:6] != 'number') & (x[-3:] != 'ind')
              & (x[-3:] != 'new') & (x[0:7] != 'patient')]


name1 = [x for x in name_left if (x != 'window_value')]
df_temp1 = df_X1[name1]

name2 = [x for x in name1 if (x != 'Medication')]

for item in name2:
    int =  'int_'+ item
    df_temp1[int] = df_temp1.Medication * df_temp1[item]

name_left1 = [x for x in list(df_temp1) if x != 'window_value']
X_pred1 = df_temp1[name_left1]

pred1 = fit1.predict(X_pred1)



#####  A = 0  predicted
X2 = df.copy()

## create dummies for sklearn
dummy_sex = pd.get_dummies(X2['sex'])

df_X2 = pd.concat([X2,dummy_sex],axis=1,ignore_index=False)
del df_X2['sex']
del df_X2['F']

dummy_race = pd.get_dummies(X2['race'])
del dummy_race['W']
dummy_race.columns = [['Race:B','Race:D','Race:O','Race:U']]

df_X2 = pd.concat([df_X2,dummy_race],axis=1,ignore_index=False)
del df_X2['race']

dummy_group = pd.get_dummies(X2['group1'])
del dummy_group['onlyinsulin']
dummy_group.columns = [['Medication']]

df_X2 = pd.concat([df_X2,dummy_group],axis=1,ignore_index=False)
del df_X2['group1']


df_X2.Medication = 0

name_list = list(df_X2)
name_left = [ x for x in name_list if (x[0:6] != 'length') & (x[0:6] != 'number') & (x[-3:] != 'ind')
              & (x[-3:] != 'new') & (x[0:7] != 'patient')]


name1 = [x for x in name_left if (x != 'window_value')]
df_temp2 = df_X2[name1]

name2 = [x for x in name1 if (x != 'Medication')]

for item in name2:
    int =  'int_'+ item
    df_temp2[int] = df_temp2.Medication * df_temp2[item]

name_left = [x for x in list(df_temp1) if x != 'window_value']
X_pred2 = df_temp2[name_left]

pred2 = fit1.predict(X_pred2)


pred1_1 = pd.DataFrame(pred1)
pred2_1 = pd.DataFrame(pred2)

pred_df = pd.concat([pred1_1, pred2_1], axis=1)
pred_df.index = df.index
pred_df.columns =[['Pred1','Pred2']]
pred_df['Medication'] = df_final.Medication


pred_df['Prediction'] = ((pred_df['Pred1'] < pred_df['Pred2'])).astype('int')


np.random.seed(0)
pred_df['Pred_equal'] = np.random.choice([0, 1], size=(len(pred1),), p=[0.5,0.5])


pred_df['Predicted'] = pred_df['Pred2']
pred_df.loc[pred_df['Prediction'] == 1, 'Predicted'] = pred_df['Pred1']

pred_df.loc[ pred_df['Pred1'] == pred_df['Pred2'], 'Prediction' ] = pred_df['Pred_equal']


### compute value function

df_new = pd.read_csv('df_weight_RF_neg.csv')
df_new.index = df_new['patient_id']
del df_new['Unnamed: 0']
df_new['window_value'] = -1 * df_new['window_value']
df_new['newweight'] = df_new['ipweight'] / df_new['pred_prob']

# df_new.group1 = df_new.group1.map(lambda x: 1 if (x == 'onlysulf') else 0)

df_merge = pd.concat([df_new,pred_df],axis=1,ignore_index=False)
df_merge['Misclass'] = ((df_merge['Medication'] == df_merge['Prediction']) ^ (df_merge['Prediction'] == -1))

df_merge_True = df_merge.loc[df_merge.Misclass == True]

pd.options.mode.chained_assignment = None
df_merge_True['Reward_Propensity'] = df_merge_True['window_value'] * df_merge_True['newweight']

Reward_sum = df_merge_True['Reward_Propensity'].sum()
df_merge_True['Reward_weight'] = Reward_weight = df_merge_True['newweight']
Reward_weight = df_merge_True['Reward_weight'].sum()
Value = Reward_sum / Reward_weight

df_merge_A = df_merge[df_merge.Medication == 1]
df_merge_B = df_merge[df_merge.Medication == 0]

df_merge_A['Reward_Propensity'] = df_merge_A['window_value'] * df_merge_A['newweight']
df_merge_A['Reward_weight'] = df_merge_A['newweight']

df_merge_B['Reward_Propensity'] = df_merge_B['window_value'] * df_merge_B['newweight']
df_merge_B['Reward_weight'] =  df_merge_B['newweight']


Reward_sum_A = df_merge_A['Reward_Propensity'].sum()
Reward_weight_A = df_merge_A['Reward_weight'].sum()
Value_A = Reward_sum_A / Reward_weight_A

Reward_sum_B= df_merge_B['Reward_Propensity'].sum()
Reward_weight_B = df_merge_B['Reward_weight'].sum()
Value_B = Reward_sum_B / Reward_weight_B


print ('Value AB is :', Value)
print ('Value A is: ', Value_A)
print ('Value B is: ', Value_B)


## importance
imp = pd.DataFrame(imp)
vars = pd.DataFrame(name_left1)

importance = pd.concat([vars,imp],axis=1)
importance.columns = [['Features','imp']]

importance = importance[importance.imp != 0]
importance.sort_values('imp',axis=0,ascending=False)