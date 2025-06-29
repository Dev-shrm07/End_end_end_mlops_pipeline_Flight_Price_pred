FROM python:3.12-slim

WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8000 8080 5000

RUN chmod +x run.sh

CMD ["./run.sh"]