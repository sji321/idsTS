unit_root_test=function(input_df,f,f.name)
{
  pp.res=NULL
  kpss.res=NULL
  box.res=NULL
  adf.res=NULL
  
  for(i in 1:dim(input_df)[2])
  {
    temp=pp.test(input_df[,i])$p.value
    temp2=kpss.test(input_df[,i])$p.value
    box_temp=Box.test(input_df[,i], lag = 20, type="Ljung")$p.value
    temp.adf <- adf.test(input_df[,i])$p.value
    
    pp.res=cbind(pp.res,temp)
    kpss.res=cbind(kpss.res,temp2)
    box.res=cbind(box.res,box_temp)
    adf.res=cbind(adf.res,temp.adf)
  }
  
  kpss_stationary=which(kpss.res>0.05)
  pp_unit_root=which(pp.res>0.05) # reject the null hypo
  box=which(box.res>0.05) # reject 
  adf=which(adf.res>0.05) # reject 
  
  sink(paste(f.name,f,"_pp_KPSS_Box.txt"))
  print(pp.res)
  print(kpss.res)
  print(box.res)
  print(adf.res)
  print(kpss_stationary)
  print(pp_unit_root)
 
  print(box)
  print(adf)
  sink()
  
  final_res=rbind(pp.res,kpss.res,box.res)
  rownames(final_res)=c("PP", "KpSS","BOX")
  return(final_res)
  
}


