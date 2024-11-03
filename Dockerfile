FROM python:3

WORKDIR /app

COPY main.py main.py

COPY requirements.txt requirements.txt

COPY database.sqlite database.sqlite

RUN pip install -r requirements.txt

CMD [ "/app/main.py" ]
