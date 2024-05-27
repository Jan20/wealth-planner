# syntax=docker/dockerfile:1.4

FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y locales

RUN pip install --no-cache-dir -r requirements.txt

RUN sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG de_DE.UTF-8
ENV LANGUAGE de_DE:de
ENV LC_ALL de_DE.UTF-8

COPY . .

EXPOSE 5000

CMD ["python3", "main.py"]
