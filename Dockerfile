FROM python:latest
RUN  pip install -i https://mirrors.aliyun.com/pypi/simple pip -U \
     && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
     && pip install scrapy==2.5 redis pyMongo
WORKDIR /app
ENTRYPOINT ["scrapy","crawl","poems","-a"]
CMD ["author=''"]
