FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    pkg-config \
    libjpeg-dev \
    libgif-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install mediapipe and pycairo
RUN pip install --upgrade pip \
    && pip install mediapipe pycairo

# Install mysqlclient
RUN pip install mysqlclient

COPY ./requirements.txt ./

# Install other dependencies from requirements.txt
RUN pip install -r requirements.txt

COPY ./  ./

# Start Django development server
CMD ["sh", "entrypoint.sh"]
