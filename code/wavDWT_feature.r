


wavDWT_feature=function(input, d.levels,w ){
  
  # library(wmtsa)
  # library(entropy)
 
  #dwtobj1 <- wavDWT(as.numeric(process_sig),  n.levels=d.levels, wavelet= w,keep.series=TRUE)
 
  ############################################################################# 
  # ploting the level of 1
  # plot(dwtobj1, levels = 1)
  # plot(wavShift(dwtobj1))
  # summary(dwtobj1)

  #Plotting wavelet coefficients of level 1 through 4 and not plotting any scaling coefficients.
  #plot(dwtobj1, levels = 4, plot.V=F)
 
  
  # a character string denoting the filter type. Supported types include:
  #   
  #   EXTREMAL PHASE (daublet):
  #   "haar", "d2", "d4", "d6", "d8", "d10", "d12", "d14", "d16", "d18", "d20"
  # 
  # LEAST ASYMMETRIC (symmlet):
  #   "s2","s4", "s6", "s8", "s10", "s12", "s14", "s16", "s18", "s20"
  # 
  # BEST LOCALIZED:
  #   "bl2","bl4", "bl6", "l14", "l18", "l20"
  # 
  # COIFLET:
  #   "c6", "c12", "c18", "c24", "c30"
  # 
  # Default: "s8".
  # 
  # plot(wavShift(dwtobj1))
  # eda.plot(dwtobj1)
  ############################################################################# 
  
  #b@W[[2]]
 
  temp=NULL
  f_wavelet = NULL
  for (row in 1: dim(input)[1])
  {
    process_sig = input[row,1:(length(input)-5)]
    dwtobj1 <- dwt(as.numeric(process_sig),  n.levels=d.levels, filter = w, boundary="reflection") #library(wavelets)
    
    ratio_1 = sum(dwtobj1@W$W2)/sum(dwtobj1@V$V4)
    ratio_2 = sum(dwtobj1@W$W2)/sum(dwtobj1@V$V2)
    ratio_3 = sum(dwtobj1@W$W3)/sum(dwtobj1@V$V3)
    ratio_4 = sum(dwtobj1@W$W4)/sum(dwtobj1@V$V4)
    ratio_5 = sum(dwtobj1@W$W3)/sum(dwtobj1@V$V4)
    
  
    sss_w1 = sum_of_square(dwtobj1@V$V1)/sum_of_square(dwtobj1@W$W1)
    sss_w2 = sum_of_square(dwtobj1@V$V2)/sum_of_square(dwtobj1@W$W2)
    sss_w3 = sum_of_square(dwtobj1@V$V3)/sum_of_square(dwtobj1@W$W3)
    sss_w4 = sum_of_square(dwtobj1@V$V4)/sum_of_square(dwtobj1@W$W4)
 
    high_low_ration_1 = sum_of_square(dwtobj1@W$W2)/sum_of_square(dwtobj1@V$V1) # HS/high frequency of low frequency
    high_low_ration_2 = sum_of_square(dwtobj1@W$W3)/sum_of_square(dwtobj1@V$V1)
    high_low_ration_3 = sum_of_square(dwtobj1@W$W4)/sum_of_square(dwtobj1@V$V1)
    
    
   
    temp=c(ratio_1,ratio_2,ratio_3,ratio_4, ratio_5, sss_w1, sss_w2,sss_w3,sss_w4,high_low_ration_1,high_low_ration_2,high_low_ration_3)
    f_wavelet=rbind(f_wavelet,temp)
    
     message("Wavelet Data Processing in row: ", row)
     if (row %% 10000 == 0) cat(".",row) # print "in progress" message as a dot in every 1000 data processed

    rm(temp)
  }
   
  
   
   return(f_wavelet)
   
  }

#--------------------------------------------
sum_of_square = function (sig)
{
  tota_sss= 0
  len_row = dim(sig)[1]
  local_mean = mean(sig)
  for (i in 1:len_row){
    temp_sum = (sig[i] - local_mean) * (sig[i] - local_mean)
    tota_sss= tota_sss + temp_sum
  }
  
  return (tota_sss)
}


