FROM python:3.6

RUN mkdir -p annu_api
WORKDIR annu_api

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY . ./
ENV PYTHONPATH /annu_api


CMD python api/web_api.py