FROM python:3.7

WORKDIR /app

COPY . /app

COPY ./moviesByPhone/docker-settings.py /app/moviesByPhone/settings.py

ENV TWILIO_ACCOUNT_SID=1 TWILIO_AUTH_TOKEN=2

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
