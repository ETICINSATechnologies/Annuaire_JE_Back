FROM python:3.6

RUN mkdir -p api
WORKDIR api

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY . ./
ENV PYTHONPATH /api
EXPOSE 5000

CMD gunicorn -b 0.0.0.0:5000 api.web_api:app