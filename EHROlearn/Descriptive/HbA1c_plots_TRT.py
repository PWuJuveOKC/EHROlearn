from __future__ import division, print_function
import math
import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from pylab import *


## use gap days file
test = pd.read_csv('ABCDhab_gap.csv')

## Only group A + B
test = test[(test.group1 == 'onlyinsulin') ^ (test.group1 == 'onlysulf')]
test['test_time_day'] = test.test_time.apply(lambda x: x[0:10])

## parse test time and change time
test['test_time_day_parse'] = test.test_time_day.apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))
test['changetime_parse'] = test.changetime.apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))


test['Post_Trt'] = (test.test_time_day_parse >= test.changetime_parse)
test['Post_Trt'] = test.Post_Trt.apply(lambda x: int(x))

## remove last record
test = test[test.Gap_days != -1]

#test.to_csv('ABCDhab_gap.csv')

## group A
test_A = test[test.group1 == 'onlysulf']
test_A_1 = test_A[test_A.Post_Trt == 0]
test_A_2 = test_A[test_A.Post_Trt == 1]


x_A_1 = test_A_1['Gap_days']
y_A_1 = test_A_1['testvalue']

log_x_A_1 =list(x_A_1.apply(lambda x: math.log(x)))
y_A_1 = list(y_A_1)


x_A_2 = test_A_2['Gap_days']
y_A_2 = test_A_2['testvalue']

log_x_A_2 =list(x_A_2.apply(lambda x: math.log(x)))
y_A_2 = list(y_A_2)



## group B
test_B = test[test.group1 == 'onlyinsulin']
test_B_1 = test_B[test_B.Post_Trt == 0]
test_B_2 = test_B[test_B.Post_Trt == 1]

x_B_1 = test_B_1['Gap_days']
y_B_1 = test_B_1['testvalue']

log_x_B_1 =list(x_B_1.apply(lambda x: math.log(x)))
y_B_1 = list(y_B_1)


x_B_2 = test_B_2['Gap_days']
y_B_2 = test_B_2['testvalue']

log_x_B_2 =list(x_B_2.apply(lambda x: math.log(x)))
y_B_2 = list(y_B_2)



################## heatmap ###################
##############################################

from mpl_toolkits.axes_grid1 import AxesGrid

# before trt
A1, xedges1, yedges1 = np.histogram2d(log_x_A_1,y_A_1, normed=True,bins=20)
extent1 = [xedges1[0],xedges1[-1],yedges1[0],yedges1[-1]]

B1, xedges2, yedges2 = np.histogram2d(log_x_B_1,y_B_1, normed=True,bins=20)
extent2 = [xedges2[0],xedges2[-1],yedges2[0],yedges2[-1]]



vals = [A1.T,B1.T]

extent = [extent1,extent2]

names = ['Metformin + Sulfonylureas','Metformin + Insulin']
cmap = 'hot_r'
fig = plt.figure()

grid = AxesGrid(fig, 111,
                nrows_ncols=(1, 2),
                axes_pad=0.5,
                share_all=False,
                label_mode="L",
                cbar_location='right',
                cbar_mode="single",
                cbar_pad = 0.03,
                )

for i in range(2):
    im = grid[i].imshow(vals[i],extent=extent[i],origin='lower',cmap=cmap,aspect=1.25,vmin=0,vmax=0.20)
    grid[i].set_ylabel('HbA1c level')
    grid[i].set_title(names[i])
    grid.cbar_axes[i].colorbar(im)
    grid[i].set_xlim(-12,8)
    grid[i].set_ylim(2,18)
fig.text(0.5, 0.15, 'Time to next measurement in days (log-scale)', ha='center')

plt.subplots_adjust(top=0.9)
plt.savefig('HbA1c_intensity_before.png', format='png', dpi=900)
plt.show()





# post trt
A2, xedges1, yedges1 = np.histogram2d(log_x_A_2,y_A_2, bins=20,normed=True)
extent1 = [xedges1[0],xedges1[-1],yedges1[0],yedges1[-1]]

B2, xedges2, yedges2 = np.histogram2d(log_x_B_2,y_B_2, bins=20,normed=True)
extent2 = [xedges2[0],xedges2[-1],yedges2[0],yedges2[-1]]


vals = [A2.T,B2.T]
extent = [extent1,extent2]
cmap = 'hot_r'

names = ['Metformin + Sulfonylureas','Metformin + Insulin']
fig = plt.figure()
fig.suptitle('Post Treatment', fontsize=15)
grid = AxesGrid(fig, 111,
                nrows_ncols=(1, 2),
                axes_pad=0.5,
                share_all=False,
                label_mode="L",
                cbar_location='right',
                cbar_mode="single",
                cbar_pad = 0.03,
                )

for i in range(2):
    im = grid[i].imshow(vals[i],extent=extent[i],origin='lower',cmap=cmap,aspect='auto',vmin=0,vmax=0.2)
    grid[i].set_ylabel('HbA1c level')
    grid[i].set_title(names[i])
    grid.cbar_axes[i].colorbar(im)
    grid[i].set_xlim(-12,8)
    grid[i].set_ylim(2,18)
fig.text(0.5, 0.2, 'Time to next measurement in days (log-scale)', ha='center')

plt.subplots_adjust(top=0.9)
plt.savefig('intensity_post.png', format='png', dpi=900)
plt.show()



## histogram

## before trt, HbA1C
plt.suptitle('Before Treatment',size=20)
common_params = dict(bins=40,range=(4, 20),)

plt.subplots_adjust(hspace=.4)
plt.subplot(211)
plt.title('Metformin + Sulfonylureas')
plt.yticks(range(0,120,20))
plt.hist(np.array(test_A_1['testvalue']), **common_params)


plt.subplot(212)
plt.title('Metformin + Insulin')
plt.hist(np.array(test_B_1['testvalue']), **common_params)
plt.yticks(range(0,50,10))
plt.xlabel('HbA1c level',size=15)

plt.savefig('Histogram_Hb_before.png', format='png', dpi=900)
plt.show()


## before trt, Gap days
plt.suptitle('Before Treatment',size=20)
common_params = dict(bins=40,range=(0, 1000),)

plt.subplots_adjust(hspace=.4)
plt.subplot(211)
plt.title('Metformin + Sulfonylureas')
plt.yticks(range(0,160,20))
plt.hist(np.array(test_A_1['Gap_days']), **common_params)


plt.subplot(212)
plt.title('Metformin + Insulin')
plt.hist(np.array(test_B_1['Gap_days']), **common_params)
plt.yticks(range(0,80,20))
plt.xlabel('Days to next measurement',size=15)

plt.savefig('Histogram_days_before.png', format='png', dpi=900)
plt.show()





## post trt, HbA1C
plt.suptitle('Post Treatment',size=20)
common_params = dict(bins=40,range=(4, 20),)

plt.subplots_adjust(hspace=.4)
plt.subplot(211)
plt.title('Metformin + Sulfonylureas')
plt.yticks(range(0,160,20))
plt.hist(np.array(test_A_2['testvalue']), **common_params)


plt.subplot(212)
plt.title('Metformin + Insulin')
plt.hist(np.array(test_B_2['testvalue']), **common_params)
plt.yticks(range(0,50,10))
plt.xlabel('HbA1c level',size=15)

plt.savefig('Histogram_Hb_post.png', format='png', dpi=900)
plt.show()


## post trt, Gap days
plt.suptitle('Post Treatment',size=20)
common_params = dict(bins=40,range=(0, 1000),)

plt.subplots_adjust(hspace=.4)
plt.subplot(211)
plt.title('Metformin + Sulfonylureas')
plt.yticks(range(0,120,20))
plt.hist(np.array(test_A_2['Gap_days']), **common_params)


plt.subplot(212)
plt.title('Metformin + Insulin')
plt.hist(np.array(test_A_2['Gap_days']), **common_params)
plt.yticks(range(0,120,20))
plt.xlabel('Days to next measurement',size=15)

plt.savefig('Histogram_days_post.png', format='png', dpi=900)
plt.show()

