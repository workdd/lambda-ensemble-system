```
aws configure

export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)

echo "export ACCOUNT_ID=${ACCOUNT_ID}" | tee -a ~/.bash_profile

docker tag lambda-ensemble $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/lambda-ensemble

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

docker push $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/lambda-ensemble
```