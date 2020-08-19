#!/usr/bin/env python3

import asyncio
import websockets
import sys
import wave
import json, os


'''
client.py - demo how interact with recognition server.
AUTHOR: Mindaugas Greibus
Create wav dir, put some sounds file 16kHz and execute script
'''

async def recognize(uri, dirName, fname):
    async with websockets.connect(uri) as websocket:
        #"word_list" : "zero one two three four five six seven eight nine oh",

        await websocket.send('''{"config" : 
                { "sample_rate" : 16000.0}}''')
        #print('Found directory: %s' % dirName)
        class_name = os.path.basename(dirName+"/")

        #print('\t%s' % fname)
        #wav_path=sys.argv[1]
        wav_path=dirName+"/"+fname
        wf = wave.open(wav_path, "rb")
        while True:
            data = wf.readframes(4000)

            if len(data) == 0:
                break

            await websocket.send(data)
            response = await websocket.recv()
            result = json.loads(response)
            if "result" in result:            
                #print(result)
                words = result["result"]
                begining = words[0]["start"]
                ending = words[-1]["end"]
                text = result["text"]
                print("{}/{},{},{},{}".format(class_name, fname, begining, ending, text))

        await websocket.send('{"eof" : 1}')
        response_do_not_care = await websocket.recv()

for dirName, subdirList, fileList in os.walk("wav", topdown=False):
    for fname in fileList:
        asyncio.get_event_loop().run_until_complete(
            recognize('wss://liepa-kaldi.herokuapp.com:443', dirName, fname ))
