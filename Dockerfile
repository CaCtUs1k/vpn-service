FROM python:3.11-slim
LABEL maintainer="denischernish19012004@gmail.com"

ENV PYTHONUNBUFFERED 1
ENV DEBUG_MODE True
ENV SECRET_KEY "mysecretvfbhtfhgthvgfkey"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]