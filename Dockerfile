FROM debian:stable-slim

WORKDIR /app/

COPY . .

RUN apt-get update && \
    apt-get -y --no-install-recommends install python3-minimal python3-pip python3-setuptools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]
