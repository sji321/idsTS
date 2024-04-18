#!/usr/bin/env python
# coding: utf-8

# In[1]:


##------------------------------------------------------
## Collect each month converted time series 
##---------------------------------------------------------

import pyreadr # package to read R data
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import grangercausalitytests
import math
import warnings

warnings.simplefilter('ignore')

base = 'path'
out_folder =  'path'
paper_out_folder = os.path.join(out_folder,'target_folder/')


file_name ='*.RData' 
data_folder = os.path.join(base,'folder/')



        
os.chdir(data_folder)    
dir_list = os.listdir(data_folder)
all_df =pd.DataFrame() # final output data collection file
month_df =pd.DataFrame()
for i in range(0,len(dir_list)):
    d= os.path.join(data_folder,dir_list[i])
    os.chdir(d)
    files_list = os.listdir(d)
    
    #----- each month file reading -------------#
    for month in range(0,len(files_list)):
        
        day_df = pyreadr.read_r(files_list[month])    
       
        input_data = day_df['input'] # extract the pandas data frame for object c6
        #--- add day and month info to the data
        day_info = pd.to_numeric((files_list[month].split('2015')[1]).split('.')[0])
        month_info = pd.to_numeric(d.split('or3/')[1])
        input_data['day'] = day_info   # add day info
        input_data['month'] = month_info # add month info
        all_df=all_df.append(input_data)
    print('Completed --',month_info )  
    month_df=month_df.append(all_df)   
                                   
    
print('Completed All--' )
os.chdir(paper_out_folder)
# month_df.to_csv('combine_all_ts_or3_60.csv',index=False)
month_df.to_csv('file_name0.csv',index=False)



paper_out_folder = os.path.join(out_folder,'folder/')
os.chdir(paper_out_folder)
month_df.to_csv('file_name.csv',index=False)






