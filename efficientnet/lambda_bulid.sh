docker build -t jg-seq-efficientnet . --no-cache

export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)

docker tag jg-seq-efficientnet $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/jg-seq-efficientnet

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

docker push $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/jg-seq-efficientnet

docker rmi -f $(docker images -q)
