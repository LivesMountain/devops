FROM python:3.5
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple

CMD ["/usr/local/bin/python","devops/manage.py","runserver","0.0.0.0:8080"]
