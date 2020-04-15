#!/usr/bin/env python3

import json
import os
import sys
import asyncio
import pathlib
import websockets
import concurrent.futures
import http
from vosk import Model, KaldiRecognizer

vosk_interface = os.environ.get('VOSK_SERVER_INTERFACE', '0.0.0.0')
vosk_port = int(os.environ.get('VOSK_SERVER_PORT', 2700))
vosk_model_path = os.environ.get('VOSK_MODEL_PATH', 'model')

if len(sys.argv) > 1:
   vosk_model_path = sys.argv[1]

model = Model(vosk_model_path)
pool = concurrent.futures.ThreadPoolExecutor()
loop = asyncio.get_event_loop()

def process_chunk(rec, message):
    if message == '{"eof" : 1}':
        return rec.FinalResult(), True
    elif rec.AcceptWaveform(message):
        return rec.Result(), False
    else:
        return rec.PartialResult(), False


async def process_file(path, request_headers):
    """Serves a file when doing a GET request with a valid path."""

    sever_root="/opt/vosk-server/websocket/web"
    MIME_TYPES = {
        "html": "text/html",
        "js": "text/javascript",
        "css": "text/css"
    }
    if "Upgrade" in request_headers:
        return  # Probably a WebSocket connection

    if path == '/':
        path = '/index.html'

    response_headers = [
        ('Server', 'asyncio websocket server'),
        ('Connection', 'close'),
    ]

    # Derive full system path
    full_path = os.path.realpath(os.path.join(sever_root, path[1:]))

    # Validate the path
    if os.path.commonpath((sever_root, full_path)) != sever_root or \
            not os.path.exists(full_path) or not os.path.isfile(full_path):
        print("HTTP GET {} 404 NOT FOUND".format(full_path))
        return http.HTTPStatus.NOT_FOUND, [], b'404 NOT FOUND'

    # Guess file content type
    extension = full_path.split(".")[-1]
    mime_type = MIME_TYPES.get(extension, "application/octet-stream")
    response_headers.append(('Content-Type', mime_type))

    # Read the whole file into memory and send it out
    body = open(full_path, 'rb').read()
    response_headers.append(('Content-Length', str(len(body))))
    print("HTTP GET {} 200 OK".format(path))
    return http.HTTPStatus.OK, response_headers, body


async def recognize(websocket, path):

    rec = None
    word_list = None
    sample_rate = 8000.0

    while True:

        message = await websocket.recv()

        # Load configuration if provided
        if isinstance(message, str) and 'config' in message:
            jobj = json.loads(message)['config']
            if 'word_list' in jobj:
                word_list = jobj['word_list']
            if 'sample_rate' in jobj:
                sample_rate = float(jobj['sample_rate'])
            continue

        # Create the recognizer, word list is temporary disabled since not every model supports it
        if not rec:
            if False and word_list:
                 rec = KaldiRecognizer(model, sample_rate, word_list)
            else:
                 rec = KaldiRecognizer(model, sample_rate)

        response, stop = await loop.run_in_executor(pool, process_chunk, rec, message)
        await websocket.send(response)
        if stop: break

start_server = websockets.serve(
    recognize, vosk_interface, vosk_port, process_request=process_file)

loop.run_until_complete(start_server)
loop.run_forever()
