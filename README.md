# kaldi_liepa_asr_docker
Kaldi recognition works with Liepa models. Recognition client is buildit on JS/HTML and websockets

# Work based on 

Liepa2: https://www.raštija.lt/liepa-2/apie-projektą-liepa-2/7666
Kaldi: https://kaldi-asr.org/
Vosk: https://github.com/alphacep/vosk-api

#Build Docker Image
Step 1. Get the acoustic and language model and copy it to ```src/model/```

Step 2. Go to ```src``` dir and run:
```
  docker build -t "liepa-kaldi" .
  docker run --rm -e"PORT=2700" -p 2700:2700 -it liepa-kaldi
```

Step 3. test in browser: ```http://localhost:2700```. UI in in is hardcoded and lithuanian.

# Works in Heroku 
Works with in Heroku cloud.
Step 1. Setup account and Docker registry project
Step 2. In ```src``` folder run
```
  heroku apps:create liepa-kaldi --region eu
  heroku container:push web
  heroku container:release web 
```
You can access deployed version: https://liepa-kaldi.herokuapp.com/

# Observation
Provided Html client works only with local host or https due to browser restrictions.
