def fcast_risk_level_colab_2(tst_act_depvals,tst_scaled_var,cut_threshold, cut_status, day, write_dir,):


  copy_tdf = c.deepcopy(tst_act_depvals)
  scale_tscore = c.deepcopy(tst_scaled_var)

  col_list = ['KA', 'UA']
  scale_tscore['AttackSum'] = copy_tdf[col_list].sum(axis=1)

  scale_tscore['ratio_N'] = scale_tscore['Normal'] + scale_tscore['var']
  scale_tscore['ratio_A'] = (scale_tscore['UA'] + scale_tscore['KA']) + scale_tscore['var']

  idx_n = scale_tscore.columns.get_loc("ratio_N")
  idx_a = scale_tscore.columns.get_loc("ratio_A")
  idx_s = copy_tdf.columns.get_loc("c_ses")
  #     def risk_score(data):
  scale_tscore['risk'] = (scale_tscore['ratio_A'] / (scale_tscore['ratio_N'] + scale_tscore['ratio_A'])) * copy_tdf[
      'c_ses']
  if cut_status != 0: ## there are zero changes
    
    if cut_status == 1: ## there are zero changes
      scale_tscore["Level"] = np.where(scale_tscore["risk"] < cut_threshold, 'L', 'M')
    elif cut_status == 2: 
      scale_tscore["Level"] = np.where(scale_tscore["risk"] < cut_threshold, 'M', 'H')
    else:
      scale_tscore["Level"] = np.where(scale_tscore["risk"] < cut_threshold, 'H')
  else: #cut_status == 0 that is the risk level is L/H or L/M/H

    if len(cut_threshold) == 1: # two level
          scale_tscore["Level"] = np.where(scale_tscore["risk"] < cut_threshold[0], 'L', 'H')
    # elif len(cut_off_value[0]) == 0: 
    #   ...
    else: # three level
          min_val = min(cut_threshold)
          max_val = max(cut_threshold)
          scale_tscore.loc[scale_tscore["risk"] < min_val, "Level"] = 'L'
          scale_tscore.loc[(scale_tscore['risk'] >= min_val) & (scale_tscore['risk'] < max_val), "Level"] = 'M'
          scale_tscore.loc[scale_tscore['risk'] >= max_val, "Level"] = 'H'

  _name = file_name_create(day, '_fcast_risk_level')
  scale_tscore.to_csv(write_dir + '/' + _name,  index=False)

  return scale_tscore