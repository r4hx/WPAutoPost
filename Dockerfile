FROM python:3.9.6-slim

WORKDIR /app/

COPY . .

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
