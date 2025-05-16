# Dockerfile
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg wget unzip && \
    pip install websockets vosk soundfile && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download Vosk model
RUN mkdir /models && \
    cd /models && \
    wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip && \
    unzip vosk-model-small-en-us-0.15.zip && \
    rm vosk-model-small-en-us-0.15.zip

# Copy server code
WORKDIR /app
COPY server.py .

EXPOSE 8000

CMD ["python", "server.py"]