master="hadoop@ec2-3-85-133-45.compute-1.amazonaws.com" 

slave1="hadoop@ec2-18-234-118-124.compute-1.amazonaws.com"
slave2="hadoop@ec2-18-234-118-124.compute-1.amazonaws.com"
slave3="hadoop@ec2-18-234-118-124.compute-1.amazonaws.com"
slave4="hadoop@ec2-18-234-118-124.compute-1.amazonaws.com"

ssh -i "vockey_3.pem" ${master}
ssh -i "vockey_3.pem" ${slave1}
ssh -i "vockey_3.pem" ${slave2}
ssh -i "vockey_3.pem" ${slave3}
ssh -i "vockey_3.pem" ${slave4}



