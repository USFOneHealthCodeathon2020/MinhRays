

 df <- read.table("./input.txt",header=FALSE)
df



n<-length(df$V1)


sink("./queryout.txt")

df$V1 = as.vector(df$V1)

for (i in 1:n){
paste(cat(">input_query",sep="_", i,'\n'))
cat(paste(df[i,1], '\n'))
}
sink()

