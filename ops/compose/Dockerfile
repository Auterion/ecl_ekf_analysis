FROM python:3.5

COPY requirements.txt dev-requirements.txt /app/
COPY . /app/libs/ecl-ekf-analysis
WORKDIR /app

# Get python dependencies
RUN \
  pip install --upgrade pip && \
  pip install -r /app/requirements.txt && \
  pip install -r /app/dev-requirements.txt && \
  pip install --upgrade /app/libs/ecl-ekf-analysis

