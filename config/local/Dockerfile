FROM python:3.8-slim-buster

WORKDIR /app

# copy host to container
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# mirror the src volume with docker
# COPY ./src /app


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]