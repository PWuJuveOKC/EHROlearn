import os
import pydot
from sklearn.externals.six import StringIO
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree


df = pd.read_csv('df_weight_RF_neg.csv')

df.index = df['patient_id']
del df['Unnamed: 0']
del df['ipweight']
del df['abs_res']
del df['window_value']
del df['pred_prob']
del df['pred_prob_s']
del df['pred_prob_i']
del df['group1']
del df['res']


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


## sample weights
sample_weights = df_final.weight
del df_final['weight']

df_final.index = df_final.patient_id

name_list = list(df_final)

name_left = [ x for x in name_list if (x[0:6] != 'length') & (x[0:6] != 'number') & (x[-3:] != 'ind')
              & (x[-3:] != 'new') & (x[0:7] != 'patient')] ## remove some features (lab measure patterns etc.


########################### max_depth = 5 #########################
###################################################################

## decision tree built
clf = tree.DecisionTreeClassifier(random_state=123,min_samples_leaf=2,max_depth=5)

## features and response

X = df_final[name_left]
## rename some labels
X.rename(columns={'bp.D._low_long_new': 'DBP (low_long)', 'bp.S._low_medium_ind': 'SBP (low_medium) Extreme Dummy',
                         'hb_medium_medium_new': 'HbA1C (medium_medium)', 'length_obs_hdl': 'Length of HDL Observation',
                         'bp.D._high_long_new': 'DBP (high_long)', 'recent_hdl_mean': 'Recent HDL',
                         'overall_bp.S._mean': 'Overall SBP', 'overall_bmi_mean': 'Overall BMI',
                         'hdl_medium_medium_new': 'HDL (medium_medium)', 'length_obs_bmi': 'Lenght of BMI Observation',
                          'hdl_medium_medium_new': 'HDL (medium_medium)',
                         'bp.S._high_short_new': 'SBP (high_short)', 'hb_low_short_ind': 'HbA1C (low_short) Extreme Dummy',
                         'bp.S._low_medium_new': 'SBP (low_medium)', 'overall_ldl_mean': 'Overall LDL',
                         'recent_ldl_mean': 'Recent LDL', 'bp.S._medium_medium_new':'SBP (medium_medium)',
                         'number_ldl_measure_new': 'Number of LDL Measures','length_obs_bp.D.': 'Length of DBP Observation',
                         'bmi_low_short_ind': 'BMI (low_short) Extreme Dummy', 'length_obs_bp.S.': 'Length of SBP Observation',
                         'bp.S._high_medium_new': 'SBP (high_medium)', 'bmi_low_short_ind': 'BMI (low_short)',
                         'recent_1stmonth_bp.S._mean': 'Recent One Month SBP','length_obs_hb':'Length of HbA1C Observation',
                         'number_hb_measure_new': 'Number of HbA1C Measures','recent_1stmonth_bp.D._mean':'Recent 1-Month DBP',
                         'bp.S._low_long_ind': 'SBP (low_long) Extreme Dummy', 'length_obs_bp.D.': 'Length of DBP Observation',
                         'dysth_latest_Post_Diag': 'Latest Dysthymic Disorder Diagnosis Post Treatment',
                         'recent_hb_mean': 'Recent HbA1C', 'number_bp.S._measure_new': 'Number of SBP Measures',
                         'hdl_high_long_new': 'HDL (high_long)', 'overall_hb_mean': 'Overall HbA1C',
                         'overall_bp.D._mean': 'Overall DBP', 'hb_high_long': 'HbA1C (high_long) Extreme Dummy',
                         'bmi_high_short_new': 'BMI (high_short)', 'bp.S._medium_long_new':'SBP (medium_long)',
                         'bmi_low_long_ind': 'BMI (low_long) Extreme Dummy', 'hb_high_long_ind': 'HbA1C (high_long) Extreme Dummy',
                  'recent_bmi_mean': 'Recent BMI','overall_hdl_mean': 'Overall HDL', 'age': 'Age', 'M': 'Gender',
                  'rd_latest_Post_Diag': 'Recurrent Depression Diagnosis Post Treatment',
                  'neuro_earliest_Post_Diag':'Neuropathy Diagnosis' }, inplace=True)


y = df_final['group_new']
y = y.map(lambda x: 'Medication' if (x == 'onlysulf') else 'Insulin')

## tree results
fit1 = clf.fit(X, y, check_input=True,sample_weight=np.array(sample_weights),X_idx_sorted=None)

pred = fit1.predict(X)
pred_proba = fit1.predict_proba(X)
imp =fit1.feature_importances_
pred = pd.DataFrame(pred)

## tree plot
dot_data = StringIO()
tree.export_graphviz(fit1, feature_names=list(X),
                         filled=True, rounded=True,
                        class_names=list(y),
                         special_characters=True, rotate=False,impurity=False,label="all",out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("tree_depth_5_1.pdf")


## value function computing
df_new = pd.read_csv('df_weight_RF_neg.csv')
df_new.index = df_new['patient_id']
del df_new['Unnamed: 0']
df_new['window_value'] = -1 * df_new['window_value']

df_new.group1 = df_new.group1.map(lambda x: 'Medication' if (x == 'onlysulf') else 'Insulin')

pred.index = df_new.index
pred.columns=['pred']
df_merge = pd.concat([df_new,pred],axis=1,ignore_index=False)
df_merge['Misclass'] = (df_merge['group1'] == df_merge['pred'])

df_merge_True = df_merge.loc[df_merge.Misclass == True]

pd.options.mode.chained_assignment = None
df_merge_True['Reward_Propensity'] = df_merge_True['window_value'] * df_merge_True['ipweight'] / df_merge_True['pred_prob']

Reward_sum = df_merge_True['Reward_Propensity'].sum()
df_merge_True['Reward_weight'] = Reward_weight = df_merge_True['ipweight'] / df_merge_True['pred_prob']
Reward_weight = df_merge_True['Reward_weight'].sum()
Value = Reward_sum / Reward_weight

df_merge_A = df_merge[df_merge.group1 == 'Medication']
df_merge_B = df_merge[df_merge.group1 == 'Insulin']

df_merge_A['Reward_Propensity'] = df_merge_A['window_value'] * df_merge_A['ipweight'] / df_merge_A['pred_prob']
df_merge_A['Reward_weight'] = df_merge_A['ipweight'] / df_merge_A['pred_prob']

df_merge_B['Reward_Propensity'] = df_merge_B['window_value'] * df_merge_B['ipweight'] / df_merge_B['pred_prob']
df_merge_B['Reward_weight'] =  df_merge_B['ipweight'] / df_merge_B['pred_prob']


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
vars = pd.DataFrame(name_left)

importance = pd.concat([vars,imp],axis=1)
importance.columns = [['Features','imp']]

importance = importance[importance.imp != 0]
importance.sort_values('imp',axis=0,ascending=False)



