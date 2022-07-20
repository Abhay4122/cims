FROM python:3.8

WORKDIR /app

# Create user cims
RUN addgroup --system cims && adduser --system --ingroup cims cims

# copy host to container
COPY ./requirements.txt /app/requirements.txt

# Run the requirements.txt into container
RUN pip3 install -r /app/requirements.txt

# Copy the code from host to container
COPY ./src /app

# Give the ownership from root to cims user
RUN chown -R cims:cims /app

USER cims

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]