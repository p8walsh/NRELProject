# escape=`

# Build a new image from scratch for learning purposes
FROM python:3 as client

WORKDIR /usr/src/app

COPY ./client/rcmdTCP.py ./

COPY Encrypt.py ./

COPY . .

ENTRYPOINT [ "python", "-u" ]
CMD ["./rcmdTCP.py"]

# Build a new image from scratch for learning purposes
FROM python:3 as server

WORKDIR /usr/src/app

COPY ./server/rcmddTCP.py ./

COPY Encrypt.py ./

COPY . .

ENTRYPOINT [ "python", "-u" ]
CMD ["./rcmddTCP.py"]