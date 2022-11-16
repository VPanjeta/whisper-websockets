# Whisper-Websockets
## Implementation of OpenAI Whisper library with websockets for real time ASR
This is a rudimentary implementation of Whisper ASR over websockets for test purposes only. Implementation for a production level system would require major refactoring and code sanitisation.
## Installtion

- Install libraries by `sudo apt install ffmpeg portaudio19-dev`
- Install python pacakges by `pip3 install -r requirements.txt`

## Run
- Run the websocket server with `python3 server.py` which starts to listen for incoming socket connections.
- Connect to the server with the client using `python3 client.py`.
- To change config params, check the `client.py` file for config object.

## ToDo
- [ ] Configure arument parser for client to take config.
- [ ] User configurable stream input chunk window.
- [ ] Support for multiple connections.
- [ ] Implement real time language translation over websockets.
