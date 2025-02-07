FROM python:3.11.1
RUN apt-get update
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r app/requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 8050