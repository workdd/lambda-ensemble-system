

docker build -t jg-lambda-image-efficientnet . --no-cache

export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)

docker tag jg-lambda-image-efficientnet $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/jg-lambda-image-efficientnet

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

docker push $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/jg-lambda-image-efficientnet

docker rmi -f $(docker images -q)
