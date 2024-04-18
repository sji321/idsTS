#########################convert hms time to Minute#####################################
c2s_user_input_v1=function(c.temp.dt,time_unit)
{
    res=NULL
    out=NULL
    start=0

    temp_flag=c("OTH", "REJ","RSTO","RSTOS0", "RSTR",   "RSTRH",  "S0",     "S1" ,    "S2" ,    "SF"  ,   "SH" ,    "SHR" )
    temp_connection= c("dns" ,"http","other","rdp", "sip", "smtp","smtp,ssl", "snmp","ssh", "ssl" )
    temp_protocol = c("icmp","tcp","udp")

    flag_freq=NULL
    total_time_info=c.temp.dt[dim(c.temp.dt)[1],dim(c.temp.dt)[2]]# check time infor in the last row in time column (i.e. col23)
    num_of_rwo_time_unit=(total_time_info/time_unit)+1
    
    #for(i in 1:(c.temp.dt[dim(c.temp.dt)[1],dim(c.temp.dt)[2]])) ## original --Remove
    for(i in 0:num_of_rwo_time_unit)
    {
     
      n.df=NULL
      
     ## select each second
      end = time_unit*i +2
     
      s.df=subset(c.temp.dt, c.temp.dt[,dim(c.temp.dt)[2]] >= start  &  c.temp.dt[,dim(c.temp.dt)[2]] < end)
      if(dim(s.df)[1] !=0)
      {
        c_ses=dim(s.df)[1]
        ## compute MLE of norm distribution for continuous variables corresponding each time
	      idx=c(1, 3:13)
        temp <-s.df[,idx]
     
        mle_out=calc_Jan2022_mle_kmeans(temp,'pareto')  
        # count frequency of flag variables
        flag=nominal_to_frequency(s.df[,14],'flag')
    	  # count frequency of connection
    	  connec=nominal_to_frequency(s.df[,2],'connection')
    
      	# Count the frequency of protocol
      	protocol=nominal_to_frequency(s.df[,15],'protocol')

	    #count number of different s.ip,port,d.ip,port
        s.ip <-length(unique(s.df[,16])) 
        s.pr <-length(unique(s.df[,17]))
        d.ip <-length(unique(s.df[,18]))
	      d.pr <-length(unique(s.df[,19]))
        
       
    
        Normal <-length(which(s.df[,21]=='Normal')) #attack
        KA <-length(which(s.df[,21]=='KnownA'))
	      UA <- length(which(s.df[,21]=='UnknownA')) #attack
        
        
        n.df=cbind(n.df,mle_out,s.ip,s.pr,d.ip,d.pr,connec,flag, protocol, c_ses,Normal,KA,UA,i)
        
        res=rbind(res,n.df)
        rm(mle_out,Normal,KA,UA, flag,protocol,c_ses,connec)
       
        #cat("done for",time_unit*i, "seconds!/n")
        rm(n.df)
        
        start=end
        
      #  cat(" done for time ----- ", i)
       
      }else{ ##-- if there is no time data exist
        #cat("No rows are found for",i*time_unit, "seconds!/n")
        if(i!=0)
        {
          out=replicate(dim(res)[2], 0) # -- enter zero for the corresponding time 
          res=rbind(res,out)
      
        }else{ 
          out=replicate(43, 0) # -- enter zero for the corresponding time 
          res=rbind(res,out)
          
        }
        
          start=end ## -----------> modified on Feb. 1 2022
      }
  
  	if (i %% 1000 == 0) cat("i.")# cat(".")
    
      # cat("start",start,"index",i,"\n")
    }# end for i 
   
    
    return(res) 
    
   
 
}