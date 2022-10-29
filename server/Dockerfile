# escape=`

FROM python:3 as server

WORKDIR /usr/src/app

COPY server.py ./

COPY Encrypt.py ./

COPY . .

ENTRYPOINT [ "python", "-u" ]
CMD ["./server.py"]