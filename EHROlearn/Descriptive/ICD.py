import pandas as pd
import os
from dateutil import parser
import datetime
import math
import numpy as np



df = pd.read_csv('ICD_demo.csv')
df2 = pd.read_csv('ICD_demo_post.csv')



name_list = list(df)
name_new = [x for x in name_list if (x[-8:] != 'earliest') & (x[-7:] != 'earlies') & ((x[-6:] != 'latest')
            & (x[-5:] != 'parse') & (x != 'age'))]

icd = df[name_new]
icd_post = df2[name_new]



icd_sulf = icd[icd.group1 == 'onlysulf']
icd_insulin = icd[icd.group1 == 'onlyinsulin']

icd_sulf_post = icd_post[icd_post.group1 == 'onlysulf']
icd_insulin_post = icd_post[icd_post.group1 == 'onlyinsulin']


###### Group A
dat1 = icd_sulf
dat2 = icd_sulf_post

comorbidity = ['ret', 'neuro', 'nephro','hyperten', 'isch', 'stroke', 'ami', 'angina', 'coron', 'cv', 'perif',      'dysth','sd', 'rd']


dat1.rename(columns={'hyperten_earlies_Post_Diag':'hyperten_earliest_Post_Diag'}, inplace=True)
count1 = []

for comorb in comorbidity:
    a = dat1[dat1[comorb + '_earliest_Post_Diag'] == 1].shape[0]
    count1.append(a)



dat2.rename(columns={'hyperten_earlies_Post_Diag':'hyperten_earliest_Post_Diag'}, inplace=True)
count2 = []

for comorb in comorbidity:
    a = dat2[dat2[comorb + '_earliest_Post_Diag'] == 1].shape[0]
    count2.append(a)


###### Group B
dat3 = icd_insulin
dat4 = icd_insulin_post

comorbidity = ['ret', 'neuro', 'nephro','hyperten', 'isch', 'stroke', 'ami', 'angina', 'coron', 'cv', 'perif', 'dysth','sd', 'rd']


dat3.rename(columns={'hyperten_earlies_Post_Diag':'hyperten_earliest_Post_Diag'}, inplace=True)
count3 = []

for comorb in comorbidity:
    a = dat3[dat3[comorb + '_earliest_Post_Diag'] == 1].shape[0]
    count3.append(a)



dat4.rename(columns={'hyperten_earlies_Post_Diag':'hyperten_earliest_Post_Diag'}, inplace=True)
count4 = []

for comorb in comorbidity:
    a = dat4[dat4[comorb + '_earliest_Post_Diag'] == 1].shape[0]
    count4.append(a)



code = ['362.01','357','v81.5','997.91','v17.3','v17.1','410','413','746.85', '430-438','443.9','300.4','296.2','296.3']





############# cluster map ##############
########################################

from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()


########### group A


df1 = {'code': code, 'Before Treatment': count1, 'Post Treatment': count2}

countdf1 = pd.DataFrame(data = df1, index = code)
countdf1.sort_index(inplace=True)



df2 = {'code': code, 'Before Treatment': count3, 'Post Treatment': count4}

countdf2 = pd.DataFrame(data = df2, index = code)
countdf2.sort_index(inplace=True)





names = ['Metformin + Sulfonylureas','Metformin + Insulin']
countdf = [countdf1,countdf2]
yticks = ['Single Depression','Recurrent Depression','Dysthymic Disorder', 'Neuropathy',
          'Retinopathy','Acute Myocardial Infarction','Angina','Cerebrovascular','Periferial Vascular',
          'Coronary Artery','Hypertension','Stroke','Ischemia','Nephropathy']



### all plots in a figure
fig, axn = plt.subplots(1, 2, sharex=True, sharey=True)
cbar_ax = fig.add_axes([.91, .3, .03, .4])

for i, ax in enumerate(axn.flat):
    ax = sns.heatmap(countdf[i][['Before Treatment','Post Treatment']], ax=ax,
                cbar=i == 0,
                annot=True,
                linewidths=.5,yticklabels=yticks,cmap='hot_r',
                cbar_ax=None if i else cbar_ax)
    ax.set_title(names[i])
    ax.tick_params(labelsize=10)
    ax.set_yticklabels(yticks, rotation=0)
fig.tight_layout(rect=[0, 0, .9, 1])
# plt.savefig('ICD.png', format='png', dpi=900)
plt.savefig('ICD.pdf', format='pdf', dpi=900)


################## updated figure ################
################# Group A vs B    ################

## before TRT
yticks = ['Single Depression','Recurrent Depression','Dysthymic Disorder', 'Neuropathy',
          'Retinopathy','Acute Myocardial Infarction','Angina','Cerebrovascular','Periferial Vascular',
          'Coronary Artery','Hypertension','Stroke','Ischemia','Nephropathy']
names = ['Metformin + Sulfonylureas','Metformin + Insulin']
df_before =  {'code': code, names[0]: count1, names[1]: count3}

countdf_before = pd.DataFrame(data = df_before, index = code)
countdf_before.sort_index(inplace=True)

ax1 = sns.heatmap(countdf_before[[names[0],names[1]]],annot=True,
                     linewidths=.5,yticklabels=yticks,cmap='hot_r',vmin=0,vmax=36)
plt.yticks(rotation=0)
# plt.suptitle('Before Treatment',fontsize=15)
plt.tight_layout(rect=[0, 0, 0.8, 0.7])
plt.subplots_adjust(top=0.9)

plt.savefig('ICD_before.pdf', format='pdf', dpi=900)
plt.show()

## post TRT
yticks = ['Single Depression','Recurrent Depression','Dysthymic Disorder', 'Neuropathy',
          'Retinopathy','Acute Myocardial Infarction','Angina','Cerebrovascular','Periferial Vascular',
          'Coronary Artery','Hypertension','Stroke','Ischemia','Nephropathy']
names = ['Metformin + Sulfonylureas','Metformin + Insulin']
df_post =  {'code': code, names[0]: count2, names[1]: count4}

countdf_post = pd.DataFrame(data = df_post, index = code)
countdf_post.sort_index(inplace=True)

ax1 = sns.heatmap(countdf_post[[names[0],names[1]]],annot=True,
                     linewidths=.5,yticklabels=yticks,cmap='hot_r',vmin=0,vmax=36)
plt.yticks(rotation=0)
plt.suptitle('Post Treatment',fontsize=15)
plt.tight_layout(rect=[0, 0, .8, .7])
plt.subplots_adjust(top=0.9)


plt.savefig('ICD_post.png', format='png', dpi=900)
plt.show()