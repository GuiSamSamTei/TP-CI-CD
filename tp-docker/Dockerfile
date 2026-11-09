FROM python:3.13
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app.py /app/app.py
EXPOSE 8080

CMD ["python", "app.py"]