fs=60 # training

data_folder="/..path/ "
out_folder="/..path/"


day_list=[]

df3=pd.DataFrame()

for folder in os.listdir('/..path'):
    d = os.path.join('/..path', folder)
    
    result = pyreadr.read_r(d)
    input = result["user_ts"] # extract the pandas data frame for object c6

    d1=input.drop(["i"],axis=1)
    day = pd.to_numeric((d.split('1_')[1]).split('.')[0])
    
    day_list.append(day)
    out_perm=np.array([])

    np_filter_d1=d1.fillna(method = 'bfill') #ffill - forward-fill propagate inplace=False

     ## -- use entire data
   
    ## 
    filtered_d1 = c.deepcopy(np_filter_d1.iloc[:,:])
    hours_ = 1
    train_size=int(fs*hours_*60)
    train_size=int(filtered_d1.shape[0]*0.8)
    col_len = filtered_d1.shape[1]
    
    tr_df = c.deepcopy(filtered_d1[0:train_size])
    tst_df = c.deepcopy(filtered_d1[train_size:])

    # ------------feature varianve ----------------------------------------------------
    combine_actual_df =pd.concat([tr_df, tst_df], axis=0)
    actual_df_var = combine_actual_df.iloc[:,0:37].var(axis=1)
    actual_df = pd.concat([actual_df_var, combine_actual_df.iloc[:,37:col_len]], axis=1)


#--------------------------------------------------------------------------------------
    data_scaled = c.deepcopy(filtered_d1)
    scalers={}
    for i in data_scaled.columns:
        scaler = MinMaxScaler(feature_range=(0,1))
        s_s = scaler.fit_transform(data_scaled[i].values.reshape(-1,1))
        s_s=np.reshape(s_s,len(s_s))
        scalers['scaler_'+ i] = scaler
        data_scaled[i]=s_s
    
    _scale_var = data_scaled.iloc[:,0:37].var(axis=1)
    actual_scaled_df = pd.concat([_scale_var, data_scaled.iloc[:,37:col_len]], axis=1)
    
    
    
    train_df,test_df = data_scaled[0:train_size], data_scaled[train_size:] 

    out_idx = [d1.columns.get_loc("c_ses"), d1.columns.get_loc("Normal"), d1.columns.get_loc("KA"),d1.columns.get_loc("UA")]

    # Set the input_sequence_length length - this is the timeframe used to make a single prediction
    input_sequence_length = fs # number of features

     # output_sequence_length = len(out_idx) # number of outputs
    output_sequence_length = 1 # number of outputs


    x_train, y_train = partition_dataset(input_sequence_length, output_sequence_length, train_df.values,out_idx)
    x_test, y_test = partition_dataset(input_sequence_length, output_sequence_length, test_df.values,out_idx)

## Model generation
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

    epochs = 2
    batch_size = 2
    early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)
    history = model.fit(x_train, y_train,batch_size=batch_size, 
                        epochs=epochs, validation_data=(x_test, y_test))
    
    # predict
    pred_e1d1=model.predict(x_test)

    y_pred = scaler.inverse_transform(pred_e1d1)
    y_pred= y_pred.reshape((len(y_test), n_output_neurons))
    inv_test= scaler.inverse_transform(y_test.reshape(-1,1)).reshape(y_test.shape) 
    inv_y_test= inv_test.reshape(len(y_test), n_output_neurons)
   

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

    tst_row_dim = (test_df.shape)[0]
    tst_scale_var=test_df.iloc[fs+1:tst_row_dim,0:37].var(axis=1)

    pd.DataFrame(tst_scale_var)
    tst_scale_var.reset_index(drop=True,inplace=True)
    
    pred_row_var = pd.concat([tst_scale_var,y_pred], axis=1)
    inv_row_var = pd.concat([tst_scale_var,inv_y_test], axis=1)
    

 _name = (d.split('2015')[1][0:2]) + '_RMSE_MAPE_LSTM' 
f_name = str(day) + '_Fcast_values' 
a_name = str(day) + '_Actual_values'
noscale_name = str(day) + '_NoscaleActual'
ac_scale_var_name = str(day) + '_scaleActualFeaVar'
ac_var_name= str(day) + '_ActualFeaVar'
file_name = "%s.csv" % name
fcast_name = "%s.csv" % f_name
acual_name = "%s.csv" % a_name
noscale_acual_name ="%s.csv" % noscale_name
acual_scale_var_name ="%s.csv" % ac_scale_var_name
acual_var_name ="%s.csv" % ac_var_name

if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# create a folder for month
month_folder = (d.split('2015')[1][0:2])
write_dir = os.path.join(out_folder,month_folder)

os.makedirs(write_dir, exist_ok=True)

pred_row_var.columns=['fea_var','session','N','A','NA']
pred_row_var.to_csv(write_dir + '/' + fcast_name, index=False) 
# when scale is done for all features
pred_row_var.columns=['fea_var','session','N','A','NA']
inv_row_var.to_csv(write_dir + '/' + acual_name, index=False) 

actual_scaled_df.columns=['fea_var','session','N','A','NA']
actual_scaled_df.to_csv(write_dir + '/' + acual_scale_var_name, index=False) 

actual_df.columns=['fea_var','session','N','A','NA']
actual_df.to_csv(write_dir + '/' + acual_var_name, index=False) 
print('Completed --', d)


df3.columns = ['Day','S_RMSE','S_MAE','S_MSE','N_RMSE','N_MAE','N_MSE','A_RMSE','A_MAE','A_MSE','UA_RMSE','UA_MAE','UA_MSE']
df3.to_csv(out_folder + '/' + file_name,  index=False) 
