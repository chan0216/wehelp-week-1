FROM python:3.9
WORKDIR /docker-flask
ADD . /docker-flask
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]