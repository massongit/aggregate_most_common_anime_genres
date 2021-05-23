FROM python:3.8.7

RUN mkdir /app
WORKDIR /app
ADD . .
RUN apt update \
    && apt install -y mariadb-client
RUN pip install pipenv \
    && pipenv install
CMD ["bash", "run.sh"]
