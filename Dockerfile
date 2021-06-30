FROM python:3.8-slim-buster

RUN mkdir /flask-blogger
COPY requirements.txt /flask-blogger
WORKDIR /flask-blogger
RUN pip3 install -r requirements.txt

COPY . /flask-blogger

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
