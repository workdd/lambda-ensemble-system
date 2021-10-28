sudo service docker restart

docker build -t jg-lambda-ensemble-image . --no-cache

export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)

docker tag jg-lambda-ensemble-image $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/jg-lambda-ensemble-image

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

docker push $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/jg-lambda-ensemble-image

docker rmi -f $(docker images -q)
