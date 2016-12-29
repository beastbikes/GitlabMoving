FROM daocloud.io/bohanzhang/python-geo
MAINTAINER BohanZhnag <bohan.zhang@speedx.com>

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
COPY . /code/