import asyncio
import websockets
import json
import io
import whisper
import tempfile
import os
from time import perf_counter
import speech_recognition as sr


IP = '0.0.0.0'
PORT = 8000
r = sr.Recognizer()


temp_dir = tempfile.mkdtemp()
save_path = os.path.join(temp_dir, "temp.wav")

def check_stop_word(predicted_text: str, stop_word: str) -> bool:
    import re
    pattern = re.compile('[\W_]+', re.UNICODE) 
    return pattern.sub('', predicted_text).lower() == stop_word

async def audio_processor(websocket, path):
    print("Starting websockets server")
    config = await websocket.recv()
    if not isinstance(config, str):
        print("ERROR, no config")
        return

    config = json.loads(config)
    print("config:", config)
    model = config['model']
    # there are no english models for large
    if config['model'] != "large" and config['language'] == 'en':
        model = model + ".en"
    audio_model = whisper.load_model(model)

    print(f"{config["model"]} model loaded!!")


    while True:
        data = await websocket.recv()
        start = perf_counter()
        data = io.BytesIO(data)
        audio_clip = audio_clip = AudioSegment.from_file(data)
        audio_clip.export(save_path, format="wav")


        if config['language']:
            result = audio_model.transcribe(save_path, language='english')
        else:
            result = audio_model.transcribe(save_path)

        if not config['verbose']:
            predicted_text = result["text"]
            await websocket.send(predicted_text)
        else:
            predicted_text = result["text"]
            end = perf_counter()
            duration = end-start
            print("Time taken:", duration)
            await websocket.send(json.dumps(result['segments']))
            print("Processing delay: ", duration)
        
        if check_stop_word(predicted_text, config['stop_word']):
            break

start_server = websockets.serve(audio_processor, IP, PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

