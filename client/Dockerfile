# escape=`

# Build a new image from scratch for learning purposes
FROM python:3

WORKDIR /usr/src/app

COPY rcmdTCP.py ./

COPY . .

ENTRYPOINT [ "python", "-u" ]
CMD ["./rcmdTCP.py"]