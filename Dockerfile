FROM python:3.8-slim-buster

RUN mkdir /flask-blogger
COPY requirements.txt /flask-blogger
WORKDIR /flask-blogger
RUN pip3 install -r requirements.txt

COPY . /flask-blogger

CMD ["gunicorn", "wsgi:app", "-w 4", "-b 0.0.0.0:80"]
