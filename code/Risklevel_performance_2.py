def Risklevel_performance_2 (all_level, tr_size, scale_tscore, yhat, day_info, wr_dir,month_info):
	
  daily_info = str(day_info).split('2015')[1][2:4]	
  all_risk_level = c.deepcopy(all_level)
  yhat_df = c.deepcopy(yhat)
  # cm_risk=pd.DataFrame()
  cm=pd.DataFrame()

  df_level = all_risk_level[tr_size:]
  df_level.reset_index(drop=True,inplace=True)
  tst_level=df_level.iloc[0:(yhat_df.shape)[0],:]

  len_tst_risk = len(pd.unique(tst_level['Level']))
  actual_risk = len(pd.unique(all_level['Level']))
  daily_info = str(day_info).split('2015')[1][2:4]

  if actual_risk != len_tst_risk: ## ----- modified July 31 2022
    acc=0
    prec=0
    recall=0
    f1=0
    cm = np.hstack((daily_info,acc,prec,recall,f1))

    cm1=pd.DataFrame(cm)
    cm1=cm1.T
    cm1_name = file_name_create(month_info, '_cm_2_risk_level')

    if str(day_info).split('2015')[1][2:4] =='01':
      cm1.columns=['day','acc','precision','recall','f1']
      cm1.to_csv(write_dir + '/' + cm1_name,  index=False,header=True)
    else:
      cm1.to_csv(write_dir + '/' + cm1_name,  index=False,header=False,mode='a')

  else:   
    if len_tst_risk==2:

      tn, fp, fn, tp = confusion_matrix(tst_level['Level'], scale_tscore['Level']).ravel()
      acc= accuracy_score(tst_level['Level'], scale_tscore['Level']) 
      prec=metrics.precision_score(tst_level['Level'], scale_tscore['Level'], average='weighted')
      recall = metrics.recall_score(tst_level['Level'], scale_tscore['Level'], average='weighted')
      #prec=tp/(tp+fp)
      #recall=tp/(tp+fn) 
      f1 = 2 * (prec * recall) / (prec + recall) 
      #total=(tn+fp+fn+tp)
      #acc = (tp+tn)/total
      #sen =  tp/(tp+fn)
      #spec = tn/(fp+tn)
      daily_info = str(day_info).split('2015')[1][2:4] 
      cm = np.hstack((daily_info,acc,prec,recall,f1))

      cm1=pd.DataFrame(cm)
      cm1=cm1.T
      cm1_name = file_name_create(month_info, '_cm_2_risk_level')

      if str(day_info).split('2015')[1][2:4] =='01':
        cm1.columns=['day','acc','precision','recall','f1']
        cm1.to_csv(write_dir + '/' + cm1_name,  index=False,header=True)
      else:
        cm1.to_csv(write_dir + '/' + cm1_name,  index=False,header=False,mode='a')

    elif  len_tst_risk==1: # one level 
      # tn, fp, fn, tp = confusion_matrix(tst_level['Level'], scale_tscore['Level']).ravel()
      a_val =  len(tst_level['Level'] == test_score['Level'])
      tp=a_val/len(tst_level['Level'])
      acc= accuracy_score(tst_level['Level'], scale_tscore['Level']) 
      prec=metrics.precision_score(tst_level['Level'], scale_tscore['Level'], average='weighted')
      recall = metrics.recall_score(tst_level['Level'], scale_tscore['Level'], average='weighted')
      #prec=tp/(tp+fp)
      #recall=tp/(tp+fn) 
      f1 = 2 * (prec * recall) / (prec + recall) 
      #total=(tn+fp+fn+tp)
      #acc = (tp+tn)/total
      #sen =  tp/(tp+fn)
      #spec = tn/(fp+tn)
      # daily_info = str(day_info).split('2015')[1][2:4]
      cm = np.hstack((daily_info,acc,prec,recall,f1))

      cm1=pd.DataFrame(cm)
      cm1=cm1.T
      cm1_name = file_name_create(month_info, '_cm_2_risk_level')

      if str(day_info).split('2015')[1][2:4] =='01':
        cm1.columns=['day','acc','precision','recall','f1']
        cm1.to_csv(write_dir + '/' + cm1_name,  index=False,header=True)
      else:
        cm1.to_csv(write_dir + '/' + cm1_name,  index=False,header=False,mode='a')
    else:

      MCM= multilabel_confusion_matrix(tst_level['Level'], scale_tscore['Level'])
      # skm.classification_report(tst_level['Level'], scale_tscore['Level'])
      acc = accuracy_score(tst_level['Level'], scale_tscore['Level'])
      prec=metrics.precision_score(tst_level['Level'], scale_tscore['Level'], average='weighted')
      recall = metrics.recall_score(tst_level['Level'], scale_tscore['Level'], average='weighted')
      # recall=prec=tp/(tp+fp)
      # recall=tp/(tp+fn)
      f1 = 2 * (prec * recall) / (prec + recall)
      # sen =  tp/(tp+fn)
      # spec = tn/(fp+tn)
      # daily_info = str(day_info).split('2015')[1][2:4]
      cm = np.hstack((daily_info,acc,prec,recall,f1))

      cm1=pd.DataFrame(cm)
      
      cm1=cm1.T
      cm_name = file_name_create(month_info, '_cm_2_risk_level')

      if str(day_info).split('2015')[1][2:4] =='01':
        cm1.columns=['day','acc','precision','recall','f1']
        cm1.to_csv(wr_dir + '/' + cm_name,  index=False,header=True)
      else:
        cm1.to_csv(wr_dir + '/' + cm_name,  index=False,header=False,mode='a')