# kaldi_liepa_asr_docker
Kaldi recognition works with Liepa models. Recognition client is buildit on JS/HTML and websockets

# Work based on 

* Liepa2: https://www.raštija.lt/liepa-2/apie-projektą-liepa-2/7666
* Kaldi: https://kaldi-asr.org/
* Vosk: https://github.com/alphacep/vosk-api

# How it works

It is based on vosk server, please, find details in the link above. In short. Docker image with kaldi server and model is build. Docker image is deployed on any docker container(e.g. local machine, public server). Docker image consists of HTML and JS to connect to server through webscokets. Browser loads(see Build Steps to find URL) the page, page records microphone audio and sends stream to server.Server on recognition event will send back the message with result. It is possible write other clients to get recognition trhough webscokets e.g. for Java(Android), Python(Desktop), etc. 

![Liepa Kaldi Server](https://raw.githubusercontent.com/liepa-project/kaldi_liepa_asr_docker/master/doc/liepa_kaldi_server.png)

# Build Docker Image

Step 1. Get the acoustic and language model "kaldi-lt-lt-liepa2-0.1.tar.gz" and copy it to ```src/model/kaldi-lt-lt-liepa2-0.1.tar.gz```

Step 2. Go to ```src``` dir and run:
```
  docker build -t "liepa-kaldi" .
  docker run --rm -e"PORT=2700" -p 2700:2700 -it liepa-kaldi
```

Step 3. test in browser: ```http://localhost:2700```. UI in in is hardcoded and in Lithuanian.

# Works in Heroku Cloud

Works with in Heroku cloud.
Step 1. Setup account and Docker registry project
Step 2. In ```src``` folder run
```
  heroku apps:create liepa-kaldi --region eu
  heroku container:push web
  heroku container:release web 
```
You can access deployed version: https://liepa-kaldi.herokuapp.com/

# Other Clients

Please visit Vosk-Server(https://github.com/alphacep/vosk-server/tree/master/client-samples)  to get for samples for different programming langueges: angluar.js, csharp, node.js, php, python. 

# Observations

Provided Html client works only with local host or https due to browser restrictions. 

Vosk server uses 8000Hz sampling audio. Liepa2 model was build on 16kHz audio samples. It might be needed sent to server ```{"config" : {"sample_rate" : 16000.0}}``` 
