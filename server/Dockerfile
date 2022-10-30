# escape=`

FROM python:3 as server

WORKDIR /usr/src/app

COPY server.py ./

COPY Encrypt.py ./

COPY . .

ADD requirements.txt .
RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "-u" ]
CMD ["./server.py"]