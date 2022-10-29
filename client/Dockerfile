# escape=`

FROM python:3 as server

WORKDIR /usr/src/app

COPY client.py ./

COPY Encrypt.py ./

COPY . .

ENTRYPOINT [ "python", "-u" ]
CMD ["./client.py"]