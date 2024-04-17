FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt
RUN pip install flake8 black isort mypy
COPY . /backend/
