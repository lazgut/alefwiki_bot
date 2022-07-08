FROM python:3.9

WORKDIR usr/src/app/

COPY . /usr/src/app/

RUN python -m venv venv

RUN . ./venv/bin/activate

RUN pip install --user pyTelegramBotAPI beautifulsoup4 requests lxml pandas sqlalchemy psycopg2

CMD ["python", "run.py"]