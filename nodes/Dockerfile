FROM python:latest

COPY Block.py /app/Block.py
COPY ChainLink.py /app/ChainLink.py
COPY Blockchain.py /app/Blockchain.py
COPY FlaskClient.py /app/main.py
COPY start.sh /app/start.sh

RUN pip install requests pycryptodome flask

RUN cd /app && openssl genrsa 2048 > private-key.pem && openssl rsa -in private-key.pem -pubout -out public-key.pem

CMD ["./app/start.sh"]
