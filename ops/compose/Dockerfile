FROM --platform=linux/amd64 python:3.6


COPY requirements.txt dev-requirements.txt /app/
COPY . /app/libs/ecl-ekf-analysis
WORKDIR /app

# Get python dependencies
RUN \
  pip install --upgrade pip && \
  pip install -r /app/requirements.txt && \
  pip install -r /app/dev-requirements.txt && \
  pip install --upgrade /app/libs/ecl-ekf-analysis

