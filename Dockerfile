FROM alpine:latest

LABEL authors="Krzysztof Semenowicz <git@semenowicz.net>"

RUN apk --no-cache add ca-certificates python3 py3-pip

ADD requirements.txt /

RUN pip3 install -r requirements.txt

RUN mkdir /app

ADD src/mysql_updatetables_v3.py /app

WORKDIR /app

ENTRYPOINT [ "/usr/bin/python3", "/app/mysql_updatetables_v3.py"]
