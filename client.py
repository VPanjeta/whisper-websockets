import asyncio
import websockets
import json
import io
import speech_recognition as sr

config = {
    "language": 'en',
    "model": "base",
    "verbose": False,
    "stop_word": "stop"
}

async def microphone_client():
    async with websockets.connect(
            'ws://0.0.0.0:8000/') as websocket:
        await websocket.send(json.dumps(config))
        r = sr.Recognizer()

        while True:
            with sr.Microphone(sample_rate=16000) as source:
                audio = r.listen(source)
                data = io.BytesIO(audio.get_wav_data())
                await websocket.send(data)
                print(await websocket.recv())


asyncio.get_event_loop().run_until_complete(microphone_client())
