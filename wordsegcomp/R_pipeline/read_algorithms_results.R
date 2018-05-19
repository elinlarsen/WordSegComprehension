#note : the architecture of the results directory should be
# path_res, '/',algo,'/', unit,'/freq-words.txt'
# thus, the results file containing the list of number of occurrences by each words correctly segmented should be name
# as '/freq-words.txt'
# unit is either syllable or phoneme

read_gold=function(path_res, corpus)
{

  file_freq=paste(path_res ,'gold', 'syllable','freq-words.txt', sep="/")
  freq=read_delim(file=file_freq, "\t", escape_double = FALSE, trim_ws = TRUE)
  colnames(freq)=c("count", "Type") ### different order in columns
  print(freq)
  freq$count_gold=freq$count
  freq$unit <- ""  
  freq$algos<-"gold"
  #freq$freq_scaled<-freq$count/(nrow(freq)+1)
  freq$freq_smoothed<-(freq$count)/(nrow(freq)+ sum(freq$count))
  freq$corpus<-corpus
  freq$au<-freq$algos
  freq$au=factor(freq$au)
  return(freq)
}

  
read_algorithms_results=function(ortholines, algos, path_res, corpus, unit=c('syllable', 'phoneme'))
{
  ortho=paste(ortholines ,"gold", 'syllable','freq-words.txt', sep="/")
  df_ortho=read_delim(file=ortho, "\t", escape_double = FALSE, trim_ws = TRUE)
  print(nrow(df_ortho))
  
  datalist = list()
  L=length(algos)
  M=length(unit)
  
  for (i in 1:M)
  {
    u=unit[i]
    for (j in 1:L)
    { 
      algo=algos[j] #get data about algo results
      
      file_freq=paste(path_res ,algo, u,'freq-words.txt', sep="/")
      df=read_delim(file=file_freq, "\t", escape_double = FALSE, trim_ws = TRUE)
      
      freq=merge(df, df_ortho, by="Type", all=TRUE)
      colnames(freq)=c("Type", "count", "count_gold")
      
      freq$count[is.na( freq$count)] <- 0
      
      freq$unit <- u  
      freq$algos<-algo
      #freq$freq_scaled<-freq$count/(nrow(freq)+1)
      freq$freq_smoothed<-(freq$count+1)/(nrow(freq)+ sum(freq$count))
      freq$corpus<-corpus
      freq$au<-paste(freq$algos,freq$unit, sep="/")
      freq$au=factor(freq$au)
      
      if (i==1)
      {datalist[[j]] <- freq}
      else(datalist[[j+L]] <- freq)
      
    }
  }
  
  freq_algos <- dplyr::bind_rows(datalist)
  return(freq_algos)
}