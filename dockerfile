FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]