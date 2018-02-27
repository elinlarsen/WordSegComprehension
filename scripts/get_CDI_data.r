library(wordbankr)
spanish_wg <- get_administration_data("English (American)", "WS")
print(nrow(spanish_wg))
#c <- get_instruments()
agemax <- 0
valmax <- 0
for (a in seq(1,50)){
  #print(a)
  temp = nrow(spanish_wg[spanish_wg$age==a,])
  print(temp)
  if (temp > valmax){
    valmax = temp
    agemax = a
  }
  
}
print(agemax)
print(valmax)
