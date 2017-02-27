from __future__ import division, print_function
import pandas as pd
import os
from dateutil import parser
import datetime
import matplotlib.pyplot as plt
import numpy as np


## readin data (Processed by Ying)
HB = pd.read_csv("ABCDhab.csv")

id = HB.compatient_id.unique()
len(id)  ## 718

pd.options.mode.chained_assignment = None
## Only group A + B
test = HB[(HB.group1 == 'onlyinsulin') ^ (HB.group1 == 'onlysulf')]
test['test_time_day'] = test.test_time.apply(lambda x: x[0:10])

## parse test time and change time
test['test_time_day_parse'] = test.test_time_day.apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))
test['changetime_parse'] = test.changetime.apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))


test['days_from_change'] = test['test_time_day_parse'] - test['changetime_parse']
test['days_from_change'] = test.days_from_change.apply(lambda x: x / np.timedelta64(1,'D'))


HB_A = test[test.group1 == 'onlysulf']
HB_B = test[test.group1 == 'onlyinsulin']


## count unique patient id
id_AB = test.compatient_id.unique()
len(id_AB)  #560
id_A = HB_A.compatient_id.unique()
len(id_A) #357
id_B = HB_B.compatient_id.unique()
len(id_B) #203



#########################################################################################################
########################################### Spaghetti plots #############################################
#########################################################################################################



import seaborn as sns; sns.set(color_codes=True)
sns.set_style("white")
import statsmodels


################ group A ##################
###########################################




for patient in id_A:
    a = test[test.compatient_id == patient]
    plt.plot(a.days_from_change,a.testvalue,linewidth=1)

plt.title('Metformin + Sulfonylureas',fontsize=20)
sns.regplot(x='days_from_change',y='testvalue', data=HB_A,line_kws={'color': 'black'},lowess=True,scatter=False)
sns.axlabel('Days from Treatment Initiation','HbA1c level')
sns.plt.xlim(-1500,2500)
plt.savefig('spaghetti_groupA.pdf', format='pdf', dpi=900)


## after TRT 365 days
HB_A1 = HB_A[(HB_A.days_from_change <= 365)]
id_A1 = HB_A1.compatient_id.unique()
len(id_A1) #318

for patient in id_A1:
    a = HB_A1[HB_A1.compatient_id == patient]
    plt.plot(a.days_from_change,a.testvalue,linewidth=1)

plt.title('Metformin + Sulfonylureas',fontsize=20)
sns.regplot(x='days_from_change',y='testvalue', data=HB_A1,line_kws={'color': 'black'},lowess=True,scatter=False)
sns.axlabel('Days from Treatment Initiation','HbA1c level')
sns.plt.xlim(-1200,500)
plt.savefig('spaghetti_groupA1.pdf', format='pdf', dpi=900)



## subplots
dat = HB_A[['days_from_change','testvalue','compatient_id']]
dat.columns = ['Days from Treatment Initiation','HbA1c level','ID']


dat1 = dat[dat.ID.isin(list(id_A[0:50]))]
dat2 = dat[dat.ID.isin(list(id_A[50:100]))]
dat3 = dat[dat.ID.isin(list(id_A[100:150]))]
dat4 = dat[dat.ID.isin(list(id_A[150:200]))]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
plt.suptitle('Metformin + Sulfonylureas',size=20)
ax1.set_ylim(4,18)
ax2.set_ylim(4,18)
ax3.set_ylim(4,18)
ax4.set_ylim(4,18)

ax1.set_xlim(-1500,2500)
ax2.set_xlim(-1500,2500)
ax3.set_xlim(-1500,2500)
ax4.set_xlim(-1500,2500)


for patient in id_A[0:50]:
    a = test[test.compatient_id == patient]
    # ax1.yticks(range(2,20,2))
    ax1.plot(a.days_from_change,a.testvalue,linewidth=1)

sns.regplot(x='Days from Treatment Initiation',y='HbA1c level', data=dat1,line_kws={'color': 'black'},lowess=True,ax=ax1,scatter=False)

for patient in id_A[50:100]:
    a = test[test.compatient_id == patient]
    # ax2.yticks(range(2,20,2))
    ax2.plot(a.days_from_change,a.testvalue,linewidth=1)

sns.regplot(x='Days from Treatment Initiation',y='HbA1c level', data=dat2,line_kws={'color': 'black'},lowess=True,ax=ax2,scatter=False)


for patient in id_A[100:150]:
    a = test[test.compatient_id == patient]
    # ax3.yticks(range(2,20,2))
    ax3.plot(a.days_from_change,a.testvalue,linewidth=1)

sns.regplot(x='Days from Treatment Initiation',y='HbA1c level', data=dat3,line_kws={'color': 'black'},lowess=True,ax=ax3,scatter=False)


for patient in id_A[150:200]:
    a = test[test.compatient_id == patient]
    # ax4.yticks(range(2,20,2))
    ax4.plot(a.days_from_change,a.testvalue,linewidth=1)

sns.regplot(x='Days from Treatment Initiation',y='HbA1c level', data=dat4,line_kws={'color': 'black'},lowess=True,ax=ax4,scatter=False)

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.subplots_adjust(top=0.85)
plt.savefig('spaghetti_groupA_sub.png', format='png', dpi=900)



################ group B ##################
###########################################


for patient in id_B:
    a = test[test.compatient_id == patient]
    plt.plot(a.days_from_change,a.testvalue,linewidth=1)

plt.title('Metformin + Insulin',fontsize=20)
sns.regplot(x='days_from_change',y='testvalue', data=HB_B,line_kws={'color': 'black'},lowess=True,scatter=False)
sns.axlabel('Days from Treatment Initiation','HbA1c level')
sns.plt.xlim(-1500,2500)

plt.savefig('spaghetti_groupB.pdf', format='pdf', dpi=900)

## after TRT 365 days
HB_B1 = HB_B[(HB_B.days_from_change <= 365)]
id_B1 = HB_B1.compatient_id.unique()
len(id_B1) #184

for patient in id_B1:
    a = HB_B1[HB_B1.compatient_id == patient]
    plt.plot(a.days_from_change,a.testvalue,linewidth=1)
plt.title('Metformin + Insulin',fontsize=20)
sns.regplot(x='days_from_change',y='testvalue', data=HB_B1,line_kws={'color': 'black'},lowess=True,scatter=False)
sns.axlabel('Days from Treatment Initiation','HbA1c level')
sns.plt.xlim(-1200,500)
plt.savefig('spaghetti_groupB1.pdf', format='pdf', dpi=900)


dat = HB_B[['days_from_change','testvalue','compatient_id']]
dat.columns = ['Days from Treatment Initiation','HbA1c level','ID']

dat1 = dat[dat.ID.isin(list(id_B[0:50]))]
dat2 = dat[dat.ID.isin(list(id_B[50:100]))]
dat3 = dat[dat.ID.isin(list(id_B[100:150]))]
dat4 = dat[dat.ID.isin(list(id_B[150:200]))]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
plt.suptitle('Metformin + Insulin',size=20)
ax1.set_ylim(4,18)
ax2.set_ylim(4,18)
ax3.set_ylim(4,18)
ax4.set_ylim(4,18)

ax1.set_xlim(-1500,2500)
ax2.set_xlim(-1500,2500)
ax3.set_xlim(-1500,2500)
ax4.set_xlim(-1500,2500)



for patient in id_B[0:50]:
    a = test[test.compatient_id == patient]
    # ax1.yticks(range(2,20,2))
    ax1.plot(a.days_from_change,a.testvalue,linewidth=1)

sns.regplot(x='Days from Treatment Initiation',y='HbA1c level', data=dat1,line_kws={'color': 'black'},lowess=True,ax=ax1,scatter=False)

for patient in id_B[50:100]:
    a = test[test.compatient_id == patient]
    # ax2.yticks(range(2,20,2))
    ax2.plot(a.days_from_change,a.testvalue,linewidth=1)

sns.regplot(x='Days from Treatment Initiation',y='HbA1c level', data=dat2,line_kws={'color': 'black'},lowess=True,ax=ax2,scatter=False)


for patient in id_B[100:150]:
    a = test[test.compatient_id == patient]
    # ax3.yticks(range(2,20,2))
    ax3.plot(a.days_from_change,a.testvalue,linewidth=1)

sns.regplot(x='Days from Treatment Initiation',y='HbA1c level', data=dat3,line_kws={'color': 'black'},lowess=True,ax=ax3,scatter=False)


for patient in id_B[150:200]:
    a = test[test.compatient_id == patient]
    # ax4.yticks(range(2,20,2))
    ax4.plot(a.days_from_change,a.testvalue,linewidth=1)

sns.regplot(x='Days from Treatment Initiation',y='HbA1c level', data=dat4,line_kws={'color': 'black'},lowess=True,ax=ax4,scatter=False)

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.subplots_adjust(top=0.85)
plt.savefig('spaghetti_groupB_sub.png', format='png', dpi=900)
