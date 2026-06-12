FROM python:3.12-alpine
COPY . /code
WORKDIR /code
RUN pip install redis flask
CMD ["python", "app.py"]
