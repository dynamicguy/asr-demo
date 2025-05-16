# asr-demo
Realtime Automatic Speech Recognition (ASR) pipeline

## Sequence Diagram
![sequence diagram](asr-sequence-diagram.png)

## download models

    mkdir ./models && \
    cd ./models && \
    wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip && \
    unzip vosk-model-small-en-us-0.15.zip && \
    rm vosk-model-small-en-us-0.15.zip
