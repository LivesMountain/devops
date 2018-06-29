FROM python:3.5
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple \
    &&mkdir -p /data/program/dcuploader/logs \
    &&cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

CMD ["/usr/local/bin/python","devops/manage.py","runserver"]
