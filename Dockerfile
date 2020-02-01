FROM python:3 AS build-env

RUN mkdir /app
WORKDIR /app
COPY . .
COPY ./pip.conf /root/.config/pip/
RUN python3 setup.py install

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD python -u /app/server.py
