
FROM python:3.12-slim


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 8080 8000

RUN chmod +x run.sh
CMD ["./run.sh"]