FROM python:3.6

RUN mkdir -p api
WORKDIR api

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY . ./
ENV PYTHONPATH /api
RUN python controller/


CMD python api/web_api.py