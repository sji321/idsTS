

cor2count=function(data,t,f_name)
{
 
 
    col_len=dim(data)[2]
    res=NULL
    #res=matrix(0,nrow=2*col_len, ncol=col_len)
    for(row in 1:(col_len-1))
    {
      temp=(which( abs(data[row,])<t))
      #write(temp, file = fileConn, append = TRUE, sep = " ")
      res=cbind(res,t(temp),length(temp),"D")
      #res=rbind(t(temp),length(temp))
      #List[[row]] <- res
      
    }
    #Matrix = do.call(cbind, List)
    return(res)
    #close(fileConn)
}
   

