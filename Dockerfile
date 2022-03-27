FROM python:3.9


RUN pip3 install --upgrade pip

RUN pip3 install --user flask
RUN pip3 install --user xmltodict

RUN mkdir /app
WORKDIR /app

COPY . /app
ENTRYPOINT ["python"]
CMD ["app.py"]