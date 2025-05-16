# server.py
import asyncio
import websockets
import json
from vosk import Model, KaldiRecognizer
import time

MODEL_PATH = "/models/vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)

TURN_TIMEOUT = 2.0  # seconds of silence to trigger end-of-turn

async def handle_client(websocket):
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)

    last_audio_time = time.time()
    transcript_buffer = ""

    async def timeout_monitor():
        nonlocal transcript_buffer
        while True:
            await asyncio.sleep(0.5)
            if time.time() - last_audio_time > TURN_TIMEOUT and transcript_buffer:
                await websocket.send(json.dumps({"text": transcript_buffer.strip(), "is_final": True}))
                transcript_buffer = ""

    asyncio.create_task(timeout_monitor())

    while True:
        try:
            audio_chunk = await websocket.recv()
            last_audio_time = time.time()

            if isinstance(audio_chunk, str):
                continue

            if recognizer.AcceptWaveform(audio_chunk):
                result_json = json.loads(recognizer.Result())
                text = result_json.get("text", "")
                if text:
                    transcript_buffer += text + " "
            else:
                partial_json = json.loads(recognizer.PartialResult())
                partial_text = partial_json.get("partial", "")
                if partial_text:
                    await websocket.send(json.dumps({"text": partial_text, "is_final": False}))

        except websockets.exceptions.ConnectionClosed:
            break

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8000):
        print("WebSocket server running on ws://0.0.0.0:8000")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
