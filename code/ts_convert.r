
args = commandArgs(trailingOnly=TRUE)


SourceLocation = ""

DataLocation = ""

OutputLocation = ""

time_step = 0

# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  
  #11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
   SourceLocation = "..path"
   DataLocation =  "..path"
   OutputLocation =  "..path"
   time_step=1
  # 5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555
   SourceLocation = "..path"
   DataLocation =  "..path"
   OutputLocation =  "..path"
  
  time_step=15
  # 151515151515151515151515151515151515151515151515151515151515151515151515151515151515151515151515151515151515151515151
} else {
 
  # (in Windows): RScript filename.R data_path
  
  # (in Linux): nohup Rscript Kyoto_Process_By_TimeStamp.R /home/djeong/soji/ 1h_201502_classification Data/02 > running.log 2>&1 &
  
  ##############################################################################################################################
  ## Retrive Directory Information
  ##############################################################################################################################
  SourceLocation = args[1]
  DataLocation = args[2]
  OutputLocation = args[3]
  time_step = strtoi(args[4]) ## Timestamp
}

message("SourceLocation: ", SourceLocation)
message("DataLocation: ", DataLocation)  
message("OutputLocation: ", OutputLocation)
message("TimeStamp: ", time_step)


##############################################################################################################################
## Loading Required Functions
##############################################################################################################################
message("Loading Required Functions")
setwd(SourceLocation) 


##############################################################################################################################
## Loading Libraries
##############################################################################################################################
message("Loading Libraries")
library(wavelets)
library(fitdistrplus) # for MLE
library(tseries)  # statistical test
library(vars)
library(MTS)
library(forecast)	# for using accuracy()
library(BigVAR)
##############################################################################################################################
## Loading Data List
message("Loading Data File Names")
setwd(DataLocation) # change to the data directory
data_file_names=list.files() # Get the list of all data files

## DATA PROCESSING
message("Start processing each data file")


ex.names=c("ratio_1","ratio_2","ratio_3","ratio_4"," ratio_5"," sss_w1"," sss_w2","sss_w3","sss_w4","high_low_ration_1",
            "high_low_ration_2","high_low_ration_3","c_ses","Normal","Attack", " UA",   "time")


first.filter='c6'
three.filter='la8'
four.filter ='d6'


for(data_file_idx in 1:1)
{
  
  tryCatch({
    
    a.name=noquote(tail(strsplit(data_file_names[data_file_idx],"/")[[1]])[1]) 
    file_extension=strsplit(a.name, "\\.")[[1]][2] ## finding fine extension
    
   
    
   
    if(file_extension == "txt")
    {
      d.name = basename(data_file_names[data_file_idx]) # Extract file name
      k.name = substr(d.name,1,8)     
      
      
      message("Reading file: ", d.name)
      dd=read.table(data_file_names[data_file_idx], header=FALSE, sep="\t")  # Loading *.txt data
      
      ## create an individual folder at the target directory
      dir.create(OutputLocation, showWarnings = FALSE) # create the target directory if not exists
      setwd(OutputLocation)                            # change the working directory
      
      # Create sub-folders
      TargetSubDir <- paste(k.name, sep = "_")
      dir.create(file.path(getwd(), TargetSubDir), showWarnings = FALSE) # create the target directory if not exists
      setwd(file.path(getwd(), TargetSubDir))                            # change the working directory
      
      ###----------------------------------------------------------------------------
      ### Raw Data process & create time infomation  ( the most time consuming process)
      ###---------------------------------------------------------------------------
      var_idx=c(1:14, 24, 19:23) #including ip. port
      #conti.idx=c(1, 3:13,19:22,15:18,23) #including ip. port
      
      temp.c=dd[,var_idx] #extract conti var only
      ## Add class label to the end of data,df
      label=dd[,18]
      temp.c=cbind(temp.c,label)
      rm(label)
      #colnames(temp.c)[length(conti.idx)+1] = "label" # column name change
      
      temp.c$label[temp.c$label == -1] <- 'KnownA'
      temp.c$label[temp.c$label == 1] <- 'Normal'
      temp.c$label[temp.c$label == -2] <- 'UnknownA'
      message("Finished Changing Class Lables")
      
      
      
      #dim_col=dim(temp.c)[2]
      
      time2=strptime(dd[,23], format='%H:%M:%S')
      sec=time2$hour * 3600 + time2$min * 60 + time2$sec
      temp_2_sec <- cbind(temp.c,sec)
      
      
      user_ts=c2s_user_input_v1(temp_2_sec,time_step)   # ------> ts convert by wavelet
      
      #remove Inf values from data
      user_ts[user_ts ==Inf] = 0
      
      user_ts=as.data.frame(user_ts)# ------> modified
      ts_user_name=paste("mle",k.name,"by_ts",sep = "_")  #------> new
      save(user_ts, file=paste(ts_user_name,".RData",sep = ""))   #------> modified
      rm(sec,temp.c,temp_2_sec,dd)
      
    }    ## end for ---- if(file_extension == "txt")
      ###----------------------------------------------------------------------------
      ### Feature extraction
      ### use s.ip, d.ip, sport,d.port, num_of_cession dor DWT
      ###---------------------------------------------------------------------------
      
      
    
      message("\nStarting -- Feature extraction")
      
    # DWT feature extraction
      
      w1_feature= wavDWT_feature_v2(user_ts, wt.level, first.filter)
      w2_feature= wavDWT_feature_v2(user_ts, wt.level, three.filter)
      w3_feature= wavDWT_feature_v2(user_ts, wt.level, four.filter)
      
      w1_feature=as.data.frame(w1_feature)
      w2_feature=as.data.frame(w2_feature)
      w3_feature=as.data.frame(w3_feature)
      
      message("\nFinished -- Feature extraction")
      
      
      start_col=dim(user_ts)[2]-4 # find starting column for classes
      
      
      f_res=cbind(w1_feature, user_ts[,start_col:length(user_ts)])### one day processing
      f_res_3=cbind(w2_feature, user_ts[,start_col:length(user_ts)])### one day processing
      f_res_4=cbind(w3_feature, user_ts[,start_col:length(user_ts)])### one day processing
      
      colnames(f_res)=ex.names
      colnames(f_res_3)=ex.names
      colnames(f_res_4)=ex.names
      
      
      c_ses=user_ts[,39] # find a column (i.e. c_ses) to insert to wf featuress
      
      
     
      
      wf_name=paste(k.name,first.filter,three.filter,four.filter,sep="_")
      save(f_res,f_res_3,f_res_4,file=paste(wf_name,time_step,"_sec_wf.RData",sep=""))
      
      rm(user_ts) ## remove sec_ts
      wav_feature_len = dim(w1_feature)[2]
      
      rm(w1_feature,w2_feature,w3_feature)
      
    
    
    setwd(OutputLocation)
    
    ###----------------------------------------------------------------------------
    ### main process
    ### create list for the wavelets' features 
    ###--------------------------------------------------------------------------- 
    
    varx_by_wav=list() #------> new
    
    list_of_wf=list()
    list_of_wf[[1]]=f_res
    list_of_wf[[2]]=f_res_3
    list_of_wf[[3]]=f_res_4
    
    list_of_wf_name=list()
    list_of_wf_name[[1]]=first.filter
    list_of_wf_name[[2]]=three.filter
    list_of_wf_name[[3]]=four.filter
    
    ###------------------------------------------------------------------------
    for(w_idx in 1:length(list_of_wf) )
    {
      w.name= list_of_wf_name[[w_idx]]
      final_result=list_of_wf[[w_idx]]
      message("\nStarting -- Wavlet : ", k.name, w.name)
      
     
      
      # Create sub-folders
      # TargetSubDir <- paste(w.name, k.name, Sys.Date(),sep = "_") ##----> Removed
      TargetSubDir <- paste(w.name, k.name,sep = "_")
      dir.create(file.path(getwd(), TargetSubDir), showWarnings = FALSE) # create the target directory if not exists
      setwd(file.path(getwd(), TargetSubDir))                            # change the working directory
      
      ###----------------------------------------------------------------------------
      ### Checking NA values
      ### looking for columns were the variance is 0
      ###----------------------------------------------------------------------------
      
      # replace NA values from each cols to ero
      #final_result[is.na(final_result)] = 0
      
      ### remove any row having zero variance and NaN values
      na_row = which(is.na(final_result))
      zero_row =apply(final_result,1,function(x) var(x,na.rm=T)==0)
      row.idx=setdiff(all_row ,union(na_row,zero_row)) # remove al NA cols
      final_result=final_result[row.idx,]
      
      
      # na_count <-sapply(final_result, function(y) sum(length(which(is.na(y))))) ##count NA value from columns
      # na.col=which(na_count!=0)
      # 
      # zero.count=apply(final_result,2,function(x) var(x,na.rm=T)==0)
      # zero.col=which(zero.count!=0)
      
      ###----------------------------------------------------------------------------
      ### removing NA columns & all )'s columns
      ###----------------------------------------------------------------------------
      all.idx=1:31 # wavelet columns except two classess & time (normal and attack, time)
      en.idx=c(32:35) #five labels (c-sces,normal,attack,UA, time)
      
      #w.idx=setdiff(all.idx,union(na.col,zero.col)) # remove al NA cols
      
      
      rm(na_count,na.col,zero.count,zero.col)
      
      threshold=0.5
      file.name=paste0(w.name,k.name,sep="_")
      
      ###----------------------------------------------------------------------------
      ### Converting to stationary using diffM()
      ###  Ljung-Box test tests the null hypothesis of absence of serial correlation which is much stronger than stationarity.
      ###----------------------------------------------------------------------------
      
      info.idx=c((wav_feature_len+1):35)
      class_info=final_result[,info.idx]##four columns of data
      class_info=as.data.frame(class_info)
      ## class_label_cess_all --> output will be n times (4 matrix + class type)
      wt_label=class_label_cess_all_v2(class_info,k.name,w.name,0,'wt') ## adding two more column
      wt_df=cbind(final_result,wt_label)
      
      write.csv(wt_df, file=paste(w.name,"_wt_",k.name,"_labels_.csv"),row.names=FALSE)
      # rm(final_df,wt_label,wt_label_median)
      
      diff_o=1
      min_diff=apply(final_result, 2,function(x) (diff(x)) )
      diff_en=apply(final_result[,en.idx], 2,function(x) (diff(x)) )
      diff_ces=apply(class_info, 2,function(x) (diff(x)) ) # difference for c_ses
      min_diff=as.data.frame(min_diff)
      diff_en=as.data.frame(diff_en)
      diff_ces=as.data.frame(diff_ces)
      
      save(wt_df,min_diff,diff_en,diff_ces,file=paste(w.name,k.name,"_wf_diff.RData",sep=""))
      rm(class_info,wt_df,wt_label)
      # all labels for diff data
      diff_label=class_label_cess_all_v2(diff_ces,k.name,w.name,0,'all') # 0 indicate all data
      
      ################### write files #####################################
      diff_df=cbind(min_diff,diff_label)
      names(diff_df)[dim(diff_df)[2]-1]<- "M_three"
      names(diff_df)[dim(diff_df)[2]]<- "two"
      #write.csv(diff_df, file=paste(w.name,"_all_diff_",k.name,"_labels.csv"),row.names=FALSE)
      
      rm(class_info,wt_df,wt_label)  #------->new
      
      # feature selection using correlation
      target.idx = feature_selection(final_result, 0.5, wav_feature_len,file.name) 
      
      ###----------------------------------------------------------------------------
      ### Converting to data to Time series for training
      ###----------------------------------------------------------------------------
      
      fs=3600/time_step    # frequency. Currently 1h  240   #----> modified
      
      n=dim(min_diff)[1]    #----------------->modified
      en.idx=c(32:35) ##endous variables
      
      sample=fs ## 1h sample for traiing   #----> modified (previous value =3600)
      ahead=fs ## 1h forecasting       #----> modified  (previous value =3600)
      
      target_names=ex.names[target.idx]
      class.names=c("session", "Normal","Attack","UA")
      
      ###----------------------------------------------------------------------------
      ### Training data generation
      ###----------------------------------------------------------------------------    
      tr_ex=NULL
      for(j in 1:length(target.idx))
      {
        
        t_idx=which(all.idx==target.idx[j])
        t=ts(min_diff[1:sample,t_idx], start = 0, frequency=fs)   #----------------->modified
        tr_ex=cbind(tr_ex,t)
        rm(t)
        
      }
      
      tr_en=NULL
      
      for(j in 1:length(en.idx))
      {
        
        t=ts(diff_en[1:sample,j], start = 0, frequency=fs)
        tr_en=cbind(tr_en,t)
        rm(t)
        
      }
      
      colnames(tr_ex)=target_names
      colnames(tr_en)=class.names
      
      ###----------------------------------------------------------------------------
      ### Testing data generation
      ###----------------------------------------------------------------------------    
      
      
      
      
    }## ------------------
    
  }, error=function(e){
    cat("ERROR :", conditionMessage(e), "\n")
  }) ## end for the tryCatch


  
} ## end for the main function
