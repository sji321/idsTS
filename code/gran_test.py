

import pyreadr # package to read R data
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import grangercausalitytests
import math
import warnings


#--------------------------------------------------------------------------------

warnings.simplefilter('ignore')
#--------------------------------------------------------------------------------
base = 'path'
out_folder = 'path'
data_folder = os.path.join(out_folder,'folder/')

paper_out_folder = os.path.join(out_folder,'folder1/') 

os.chdir(data_folder)  
f = os.listdir(data_folder) # your directory path

for i in range (0, len(f)):  

    df_sheet_name = pd.read_excel(f[i], sheet_name='file_name')
    pattern =f[i].split('_')[5]
    scale =f[i].split('_')[3]
    file_date =f[i].split('_')[4]


    out_name =  'Gran_' + scale+ file_date + pattern + '.csv'

    matr = granger_test_2(df_sheet_name)
    
    fig, ax = plt.subplots()

    num_ticks = 10

    
    ax.set_xticks(np.arange(0,len(df_sheet_name),num_ticks))
    ax.set_yticks(np.arange(0,len(df_sheet_name),num_ticks))


    shw1 = ax.imshow(matr, cmap=plt.cm.Reds)

    # make bars
    bar1 = plt.colorbar(shw1)
    
    os.chdir(paper_out_folder) 
    figure_name = out_name + '.pdf'
    fig.savefig(figure_name)
    matr.to_csv(out_name)
    
    
    print('completed,' [i])
    os.chdir(data_folder)
    



def granger_test_2(df_sheet_name):
    na_filter_ = df_sheet_name.fillna(method='bfill')
    
    maxlag=20
    variables=na_filter_.columns  
    matrix = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
    for col in matrix.columns:
        for row in matrix.index:
            test_result = grangercausalitytests(na_filter_[[row, col]], maxlag=20, verbose=False)            
            p_values = [round(test_result[i+1][0]['ssr_chi2test'][1],4) for i in range(maxlag)]            
            min_p_value = np.min(p_values)
            matrix.loc[row, col] = min_p_value
    matrix.columns = [var + '_x' for var in variables]
    matrix.index = [var + '_y' for var in variables]


    return matrix







