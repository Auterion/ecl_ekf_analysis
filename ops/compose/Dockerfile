FROM python:3.5

WORKDIR /app

COPY requirements.txt dev-requirements.txt /app/
# Get python dependencies  
RUN \
  pip install --upgrade pip && \
  pip install -r /app/requirements.txt && \
  pip install -r /app/dev-requirements.txt

