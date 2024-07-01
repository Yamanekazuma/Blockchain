#! /bin/bash

cd /app && openssl genrsa 2048 > private-key.pem && openssl rsa -in private-key.pem -pubout -out public-key.pem
python3 /app/main.py
