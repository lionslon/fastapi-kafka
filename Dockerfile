FROM python:3.11-bookworm

ARG UID=1000
ARG GID=1000
ENV PYTHONUNBUFFERED=1
WORKDIR /src
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt
COPY . .
