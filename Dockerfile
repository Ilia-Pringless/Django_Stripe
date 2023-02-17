FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./stripe_project/ ./

CMD ["gunicorn", "stripe_project.wsgi:application", "--bind", "0:8000" ]