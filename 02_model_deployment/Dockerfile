FROM python:3.8.12-slim

ENV PTHONUNBUFFERED True

# RUN pip install pipenv

WORKDIR /opt/app
# COPY ["Pipfile", "Pipfile.lock", "./"]

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /opt/app

# Add this for local docker deployment
# EXPOSE 9698
# ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9698", "predict:app" ]

# Add this for cloud deployment
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 predict:app