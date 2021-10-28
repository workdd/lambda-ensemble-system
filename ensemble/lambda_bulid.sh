docker build -t jg-seq-ensemble . --no-cache

export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)

docker tag jg-seq-ensemble $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/jg-seq-ensemble

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

docker push $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/jg-seq-ensemble

docker rmi -f $(docker images -q)
