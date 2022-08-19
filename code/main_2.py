fs = 60  # training
hours_ = 16  # hours info
bootstrap_rep =2000


data_folder="/content/drive/MyDrive/Kyoto/data"
# data_folder = "F:\\KyotoTemporal\\out\\MLE\\test\\"
# data_folder="F:\\KyotoTemporal\\out\\MLE_TS_1\\01\\"
# out_folder = "F:\\KyotoTemporal\\out\\RNN_out\\RiskEstimate\\"
out_folder = "/content/drive/MyDrive/Kyoto"
## Monthly data store
# base_folder = "F:\\KyotoTemporal\\out\\RNN_out\\Fcast_Actual\\"


day_list = []


#create a logger
logger = logging.getLogger()

for folder in os.listdir(data_folder):
    d = os.path.join('/content/drive/MyDrive/Kyoto/data', folder)
	df3=pd.DataFrame()
    #     df =pd.read_csv(d)
    result = pyreadr.read_r(d)
    
    print(result.keys())
    
    # input_data = result["user_ts"]  # extract the pandas data frame for object c6 --> MLE data
    input_data = result["input"]  # extract the pandas data frame for object c6

    d1 = input_data.drop(["i"], axis=1)

    # day = pd.to_numeric((d.split('1_')[1]).split('.')[0]) ---> for MLE data
    day = pd.to_numeric(d.split('2015')[1][2:4])
    day_list.append(day)
    out_perm = np.array([])
  # log file
    log_filename = str.format('mylog%d.log' % day)
    logging.basicConfig(filename=log_filename, level=logging.INFO)

    np_filter_d1 = d1.fillna(method='bfill')  # ffill - forward-fill propagate inplace=False

    ##### ---------------  for TESTING ONLY
    # filtered_d1 = c.deepcopy(np_filter_d1.iloc[0:5000,:])

  ##### ---------------  for TESTING ONLY


    ###### ------------ Testing for Entire data
    ###### ------------
    filtered_d1 = c.deepcopy(np_filter_d1)
    ###### ------------
    ###### ------------ Testing for Entire data
    

# 16 hours of data for training
    # train_size=int(fs*hours_*60) --> for MLE 1sec
    train_size=int(fs*hours_)
    col_len = filtered_d1.shape[1]
    
    # seperate training and testing data
    tr_df = c.deepcopy(filtered_d1[0:train_size])
    tst_df = c.deepcopy(filtered_d1[train_size:])
    
# feature varianve ----------------------------------------------------
  # all actual variable
    combine_actual_df =pd.concat([tr_df, tst_df], axis=0)
  # original actal feature variance
    # actual_df_var = combine_actual_df.iloc[:,0:37].var(axis=1)  #-------> Original for MLE
    actual_df_var = combine_actual_df.iloc[:,0:85].var(axis=1)  #-------> modified July for DWT_PE
  # integration of actual feature variance and class such as session, normal, KA, UA
    actual_df = pd.concat([actual_df_var, combine_actual_df.iloc[:,37:col_len]], axis=1)
    
    # scaling to (0,1)
    train_df = c.deepcopy(tr_df)
    scalers={}
    for i in tr_df.columns:
        scaler = MinMaxScaler(feature_range=(0,1))
        s_s = scaler.fit_transform(train_df[i].values.reshape(-1,1))
        s_s=np.reshape(s_s,len(s_s))
        scalers['scaler_'+ i] = scaler
        train_df[i]=s_s
    test_df = c.deepcopy(tst_df)  
    for i in tr_df.columns:
        scaler = scalers['scaler_'+i]
        s_s = scaler.transform(test_df[i].values.reshape(-1,1))
        s_s=np.reshape(s_s,len(s_s))
        scalers['scaler_'+i] = scaler
        test_df[i]=s_s


  # train and test data combine
    data_scaled = pd.concat([train_df, test_df], axis=0)

    
# prepare for writing output -------------------------------
    os.chdir(out_folder) #change the month directory
    # print('Completed current folder --',out_folder)
    month_folder = (d.split('2015')[1][0:2])


    # create a folder for month
    if not os.path.exists(month_folder):
      
      os.makedirs(month_folder)
    # join the month folder to existed directory       
    write_dir = os.path.join(out_folder, month_folder)   
    os.chdir(write_dir) #change the month directory
    print('Completed write --',write_dir)
    
    # print(ss)
    # risk level and threshold
    level, t, t_status = risk_score_generation_colab(filtered_d1,data_scaled, d, day, write_dir,bootstrap_rep)
    # print(ss)
    ## ------------------------------------------------------------------------------------------------
    logging.info("Done risk_score_generation_colab for entire data ")  
     ## ------------------------------------------------------------------------------------------------
    # print('------- done 0')
    #     # dividing traing and testing with defined train size
#     train_df,test_df = data_scaled[0:train_size], data_scaled[train_size:] 
# class info to be forecasted 
    out_idx = [d1.columns.get_loc("c_ses"), d1.columns.get_loc("Normal"), d1.columns.get_loc("KA"),d1.columns.get_loc("UA")]
    
    # Set the input_sequence_length length - this is the timeframe used to make a single prediction
    input_sequence_length = fs # number of features

    # output_sequence_length = len(out_idx) # number of outputs
    output_sequence_length = 1 # number of outputs

# spliting data to features and class
    x_train, y_train = partition_dataset(input_sequence_length, output_sequence_length, train_df.values,out_idx)
    x_test, y_test = partition_dataset(input_sequence_length, output_sequence_length, test_df.values,out_idx)

# LSTM model generation and training
    model = Sequential()
    # n_output_neurons = output_sequence_length
    n_output_neurons = 4

    n_input_neurons = x_train.shape[1] * x_train.shape[2]
#     n_input_neurons = x_train.shape[2]
    print(n_input_neurons, x_train.shape[1], x_train.shape[2])
    model.add(LSTM(n_input_neurons, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2]))) 
    model.add(Dropout(0.25))

    model.add(LSTM(int(n_input_neurons/2), return_sequences=False))
    model.add(Dropout(0.25))

    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.25))

    # model.add(Dense(output_sequence_length))
    model.add(Dense(n_output_neurons))

    model.compile(optimizer='adam', loss='mse',metrics=['accuracy']) 
    model.summary()
    # Training the model

##### ---------------  for TESTING ONLY
    # epochs = 10
    # batch_size = 2


##### ---------------  for TESTING ONLY


    epochs = 50
    batch_size = 10
    early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)
    history = model.fit(x_train, y_train,batch_size=batch_size, 
                        epochs=epochs, validation_data=(x_test, y_test))
    ## ------------------------------------------------------------------------------------------------
    ##   write the accuracy for train and validation
    ## ------------------------------------------------------------------------------------------------
    acc_name = file_name_create(day, '_ACCURACY_train_val')
    train_acc=history.history['accuracy']
    train_acc = pd.DataFrame(train_acc)
    val_acc = history.history['val_accuracy']
    val_acc = pd.DataFrame(val_acc)
    all_acc = pd.concat([train_acc,val_acc], axis=1)
    # all_acc = train_acc +  val_acc
    all_acc.columns = ['Train','Validation']                                            

    all_acc.to_csv(write_dir + '/' + acc_name,  index=False, header=True)
  ## ------------------------------------------------------------------------------------------------
    logging.info("Done Model generation")  
    ## ------------------------------------------------------------------------------------------------  
    # predict
    pred_e1d1=model.predict(x_test)


    y_pred = scaler.inverse_transform(pred_e1d1)
    y_pred= y_pred.reshape((len(y_test), n_output_neurons))
    #reshape_test= y_test.reshape((len(y_test), n_output_neurons))
    #inv_y_test = scaler.inverse_transform(reshape_test) #---- not needed
    # inverse transform for testing label
    # inv_test= scaler.inverse_transform(y_test.reshape(-1,1)).reshape(y_test.shape) 
    inv_y_test= y_test.reshape((len(y_test), n_output_neurons))

    # # actual risk level from data scale     
    # act_d_r_l = dy_level_risk[train_size:] # for actual risk level
    

  
       # tst_risk_score = risk_score_calculation(test_df,tst_act_scaled_df,d,out_folder)
    # check any numpy array contains Nan value ----------> added 8/4/22 due to 20150616 file
    if  np.isnan(np.sum(y_pred)) : 
        # y_pred =np.nan_to_num(y_pred) # if true, replace to zero
        col_mean = np.nanmean(y_pred, axis=0)
        
        #Find indices that you need to replace
        inds = np.where(np.isnan(y_pred))

        #Place column means in the indices. Align the arrays using take
        y_pred[inds] = np.take(col_mean, inds[1])

    ##  RMSE accuracy measures
    
    for i in range(0,n_output_neurons):
        #when target attributes are also scaled
        p= mean_squared_error(inv_y_test[:,i], y_pred[:,i], squared=False)
        mse= mean_squared_error(inv_y_test[:,i], y_pred[:,i])
        mae = mean_squared_error(inv_y_test[:,i], y_pred[:,i])
        # when target attributes are not scaled

        out_perm = np.hstack((out_perm, p,mae, mse)) 
#         
        del p,mae,mse
    
    out_perm = np.hstack((day,out_perm))
    
    
    out=pd.DataFrame(out_perm)
    out =out.T
    out_perm=pd.DataFrame(out_perm)
    y_pred=pd.DataFrame(y_pred)
    inv_y_test=pd.DataFrame(inv_y_test)

    df3 = pd.concat([df3,out], axis=0)

  ## ------------------------------------------------------------------------------------------------
    logging.info("Done RMSE ")  
    ## ------------------------------------------------------------------------------------------------  
    tst_row_dim = (test_df.shape)[0]
    # tst_scale_var=test_df.iloc[fs+1:tst_row_dim,0:37].var(axis=1) --> MLE
    tst_scale_var=test_df.iloc[fs+1:tst_row_dim,0:37].var(axis=1)
    
    pd.DataFrame(tst_scale_var)
    tst_scale_var.reset_index(drop=True,inplace=True)
    
    pred_row_var = pd.concat([tst_scale_var,y_pred], axis=1)
    inv_row_var = pd.concat([tst_scale_var,inv_y_test], axis=1)
    
  
    
# write to output
    day_folder = (d.split('2015')[1][2:4])
    hdr=['fea_var','session','N','A','NA']
    fcast_name = file_name_create(day_folder, '_Fcast_values')
    pred_row_var.to_csv(write_dir + '/' + fcast_name, index=False,header=hdr) 

    acual_name = file_name_create(day_folder, '_Actual_values')
    inv_row_var.to_csv(write_dir + '/' + acual_name, index=False, header=hdr)  

    # target = scale_score['risk']
    # target_ecdf_values, y = ecdf_values(target)
    # change_values, change_idx = peak_change_V2(target_ecdf_values, str(day), save=False)
    # bootstrap_out_idx = bootstrap_out(change_values, change_idx, str(day), btrap_rep)
    
    # tst_level, t = risk_score_generation_colab(filtered_d1,data_scaled, write_dir, d, day, 'Risk',bootstrap_rep)
    tst_act_depnedvarOnly= test_df.iloc[0:(y_pred.shape)[0],37:(test_df.shape)[1]]

    # index rearrange from 0
    tst_act_depnedvarOnly.reset_index(drop=True,inplace=True)
    # test dataset feature variance calculation
    tst_scl_var = test_df.iloc[:,0:37].var(axis=1)
    pd.DataFrame(tst_scl_var)
    tst_scl_var.reset_index(drop=True,inplace=True)
    # # combine between the feature var and fcast values
    tst_scl_var_df=tst_scl_var.iloc[0:(y_pred.shape)[0]]
    tst_scl_var_df=pd.concat([tst_scl_var_df,y_pred],axis=1)
    tst_scl_var_df.columns = ['var', 'c_ses', 'Normal', 'KA', 'UA']
  

  # risk level with fcast values
    test_score = fcast_risk_level_colab_2(tst_act_depnedvarOnly,tst_scl_var_df,t,t_status, day, write_dir)

    ## ------------------------------------------------------------------------------------------------
    logging.info("Done Risk Level with fcast values ")  
    ## ------------------------------------------------------------------------------------------------  
      

    # confusion matrix of risk levels between test depenent variabls and the forecasted variables
    Risklevel_performance (level, train_size, test_score, y_pred, d, write_dir,month_folder)

     ## ------------------------------------------------------------------------------------------------
    logging.info("Done MRiskLevel Performance")  
    ## ------------------------------------------------------------------------------------------------  
    
    fcast_name = file_name_create(month_folder, '_RMSE_MAPE_LSTM')
    if (d.split('2015')[1][2:4]) == '01':
        df3.columns = ['Day','S_RMSE','S_MAE','S_MSE','N_RMSE','N_MAE','N_MSE','A_RMSE','A_MAE','A_MSE','UA_RMSE','UA_MAE','UA_MSE']
        # fcast_perm_name = file_name_create(month_folder, '_RMSE_MAPE_LSTM')
        # fcast_name = file_name_create(month_folder, '_RMSE_MAPE_LSTM')
        df3.to_csv(write_dir + '/' + fcast_name,  index=False) 
          
    else:
        # fcast_name = file_name_create(month_folder, '_RMSE_MAPE_LSTM')
        # df3.to_csv(write_dir + '/' + fcast_perm_name,  index=False, mode='a',header=False)
        df3.to_csv(write_dir + '/' + fcast_name,  index=False, mode='a',header=False)

## ------------------------------------------------------------------------------------------------
    logging.info("Done for day %s ",day)  
    ## ------------------------------------------------------------------------------------------------  
    