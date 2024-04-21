# cs643_apache_spark
cs643_apache_spark project with aws 

Git Repo

https://github.com/vkchadha/cs643_apache_spark



There are 3 sections to this read me
Section 1: Model & Training 
Seciont 2: Setting up EMR cluster ( Pyspark ENV ) 
Seciont 3: Setting up Docker & Running Inference
Seciton 4: Chat CPT 



Section 1 : 

Model was developed using PYSPARK ML Lib regression model . 
Logistic Regsion Model was used, standard with 10,000 epochs & learning rate of 0.001
Training Data Set was split into 80 : 20 for training and testing
Model trained on training data set & tested against the test dataset.  
Model Predicts :- F1 Score , accurracy is captured, Area Under the Curve. 


Section 2: Setting up EMR cluster ( Pyspark ENV ) 
* Update local Credentials ~/.aws/credentials
* Create a Key value pair for EMR Cluster. this will be used to connect ec2 hosts- "vockey_3.pem" ( Pemfile Name )
* Create EMR Cluster & S3
Step 1: Upload all code & Data set to S3 bucket. In this case we have left access to the s3 bucket as public
S3 Bucket :- https://us-east-1.console.aws.amazon.com/s3/buckets/vc35sparktraining?region=us-east-1&bucketType=general&tab=objects


Step 2: Create cluster usinf the following command 
Command :- aws emr create-cluster --release-label emr-7.1.0 --applications Name=Spark --ec2-attributes KeyName=vockey_3 --instance-groups InstanceGroupType='MASTER,InstanceCount=1,InstanceType=m4.large' InstanceGroupType='CORE,InstanceCount=4,InstanceType=m4.large' --use-default-roles  


#--bootstrap-actions Path=s3://vc35sparktraining/bootstrap.sh 
Important :- Due to issues with the EMR environment, setting running bootstrap to install required python binaries corrupts the awscli due to which one cannot cp any code   executables from s3 to the master node. 

Step 3: Install required binaries all of the hosts 


sudo yum update
#sudo yum install python-dev-is-python3
sudo pip install pandas 
sudo pip install fsspec
sudo pip3 install s3fs


Step 4 : Copy code for training on the EMR Master Ec2 Instance 

Command :- 
aws s3 cp s3://vc35sparktraining/training.py .
aws s3 cp s3://vc35sparktraining/TrainingDataset.csv .

Command :- 
spark-submit training.py

Model: 
Model will be saved to following Path :- s3://vc35sparktraining/model/pyspark_log_reg.ml

https://us-east-1.console.aws.amazon.com/s3/buckets/vc35sparktraining?region=us-east-1&bucketType=general&prefix=model/&showversions=false


Results: 
Results will be saved to following Path :
s3://vc35sparktraining/model/results/model_results.text
https://us-east-1.console.aws.amazon.com/s3/buckets/vc35sparktraining?region=us-east-1&bucketType=general&prefix=model/results/&showversions=false
format :
accuracy 0.6088560885608856
f1 0.5957466333480821
weightedPrecision 0.6008473409654067
weightedRecall 0.6088560885608856
auc 0.5957466333480821




Section 3 : Docker Hub 
Docker Hub 
https://hub.docker.com/repository/docker/vc35/cs643_pyspark_project/general
Build docker image 


Log on the ec2 instance
command : 
git clone https://github.com/vkchadha/cs643_apache_spark

sudo apt-get update -y

sudo apt-get install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
docker --version
docker build -t apache_docker .
sudo docker build -t apache_docker .
docker run -it --entrypoint /bin/bash apache_docker
/usr/bin/python3 /app/inference.py

Seciton 4: Chat CPT 



