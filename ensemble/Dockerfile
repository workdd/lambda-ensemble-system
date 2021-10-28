FROM amazon/aws-lambda-python:3.8

# optional : ensure that pip is up to data
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

# install git
RUN yum install git -y

# git clone
RUN git clone https://github.com/manchann/lambda-ensemble-sequence.git

# install packages
RUN pip install -r lambda-ensemble-sequence/requirements.txt

# move lambdafunc.py
RUN cp lambda-ensemble-sequence/ensemble/lambda_function.py /var/task/
RUN cp lambda-ensemble-sequence/ensemble/imagenet_class_index.json /var/task/

CMD ["lambda_function.lambda_handler"]