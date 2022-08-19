def risk_level_3(in_data, scale_data,w_2_dir, d_info):

    c_in_data = c.deepcopy(in_data)
    ci_99 = c_in_data.shape[1] - 1  # 99% CI column
    ci_99_val = c_in_data.iloc[:,ci_99]
    diff_idx=np.diff(ci_99_val)
    r_values=[]
	r_status=[] ## identification of the ci_99_val whether 0,1,2,3
	copy_scale_score = c.deepcopy(scale_data)
	risk_score_idx= copy_scale_score.shape[1]-1 #-----> added July 21/22 for DWT_PE
	## check the difference is all the same  or not
	if (len(ci_99_val.unique()) ==1):
		  
        if ci_99_val[0] == 0: ## no changes
            r_values = ((copy_scale_score.iloc[:,risk_score_idx]).mean())
            copy_scale_score["Level"] = np.where(copy_scale_score["risk"] < r_values, 'L', 'M')
            r_status=1
                #r_values = ((copy_scale_score.iloc[:,risk_score_idx]).mean()).tolist()
                #r_values = [(copy_scale_score.iloc[:,risk_score_idx]).mean()]
        elif  ci_99_val[0] == 1: ## decreasing
            r_values = ((copy_scale_score.iloc[:,risk_score_idx]).mean())
            copy_scale_score["Level"] = np.where(copy_scale_score["risk"] < r_values[0], 'M', 'H')
            r_status=2
                # r_values = ((copy_scale_score.iloc[:,risk_score_idx]).mean()).tolist()
            #r_values = [(copy_scale_score.iloc[:,risk_score_idx]).mean()]
        else: ## increasing
            copy_scale_score["Level"] = 'H'
                # r_values = ((copy_scale_score.iloc[:,risk_score_idx]).mean()).tolist()
            r_values = [(copy_scale_score.iloc[:,risk_score_idx]).mean()]
            r_status=3
    else:  ## different values

        r_status=0
        cut_off_value =  np.where(diff_idx != 0)
        for v in range(0, len(cut_off_value[0])):
          r_idx = int(c_in_data.iloc[cut_off_value[0][v]+1,0]) ## due to the diff calcualtion, the original index should be added by 1
          #print(r_idx)
          # get risk score values
          #temp_values = copy_scale_score.iloc[r_idx,copy_scale_score.shape[1]-1]
          temp_values = copy_scale_score.iloc[r_idx,risk_score_idx] #-----> modified July 21/22 for DWT_PE
          r_values.append(temp_values)

          # assign risk level to data
          if len(cut_off_value[0]) == 1: # two level
            copy_scale_score["Level"] = np.where(copy_scale_score["risk"] < r_values[0], 'L', 'H')
          else: # three level
            min_val = min(r_values)
            max_val = max(r_values)
            copy_scale_score.loc[copy_scale_score["risk"] < min_val, "Level"] = 'L'
            copy_scale_score.loc[(copy_scale_score['risk'] >= min_val) & (copy_scale_score['risk'] < max_val), "Level"] = 'M'
            copy_scale_score.loc[copy_scale_score['risk'] >= max_val, "Level"] = 'H'

  l_file_name = file_name_create(d_info, '_risklevel')
  # l_name = str(day_info) + '_risklevel'
  # l_file_name = "%s.csv" % l_name
  copy_scale_score.to_csv(w_2_dir + '/' + l_file_name, index=False)

    return copy_scale_score,r_values,r_status