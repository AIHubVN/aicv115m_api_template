# Build a docker that run the service
# author: Xuan-Son Vu
# 26 Aug 2021

# base image
FROM python:3.7.11

EXPOSE 8000

# set the working directory
WORKDIR .
COPY ./ .

RUN apt update
RUN apt install ffmpeg libsndfile1 --yes
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# start serving
CMD python3 serve.py
