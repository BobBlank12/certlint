# syntax-docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app
RUN mkdir -p /app/website/uploads
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD [ "python3", "main.py", "run" ]
