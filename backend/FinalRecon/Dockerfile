FROM alpine:3.15.4

RUN apk update && \
    apk add python3 py3-pip gcc python3-dev postgresql-dev libffi-dev musl-dev libxml2-dev libxslt-dev && \
    rm -rf /var/cache/apk/*

WORKDIR /root/finalrecon/
COPY . .

RUN pip3 install wheel && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ENTRYPOINT ["python3", "finalrecon.py"]
