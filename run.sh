#!/bin/bash

docker build -t app:latest .
docker run -d -p 5000:5000 app