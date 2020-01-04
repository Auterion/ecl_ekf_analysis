FROM python:3.5

COPY . /app
WORKDIR /app

# Get python dependencies
RUN \
  pip install --upgrade pip && \
  pip install -r /app/requirements.txt && \
  pip install -r /app/dev-requirements.txt && \
  pip install --upgrade /app/

