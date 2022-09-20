# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install production dependencies.
COPY requirements.txt ./

RUN apt-get update -q \
  && apt-get install --no-install-recommends -qy python3-dev g++ gcc inetutils-ping python3-opencv\
  && pip install --no-cache-dir -r ./requirements.txt \
  && apt-get remove -qy python3-dev g++ gcc --purge \
  && rm -rf /var/lib/apt/lists/* 


# Copy local code to container image
COPY main.py ./
ADD models/ ./models

ENV PRODUCTION=true

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]