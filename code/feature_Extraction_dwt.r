
feature_extration_dwt=function(ts_data, decom_level, wav_filter, n)
{
  # n - number of class needed to be exclude in finding features
  
  result=NULL
 
  
  message("\nStarting -- Feature extraction")
  for(row in 1:dim(ts_data)[1])
  {
    process_sig=ts_data[row, 1:(length(ts_data)-n)]
    
    
    wav_feature=wavDWT_feature_v2(process_sig, decom_level, wav_filter)
    
    result=rbind(result,wav_feature)
    
    
    rm(wav_feature)
    
   
    if (row %% 10000 == 0) cat(".",row) 
    
  }
  
  return (result)
  
}