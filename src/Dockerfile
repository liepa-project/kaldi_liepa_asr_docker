FROM alphacep/kaldi-vosk-server:latest

ENV MODEL_VERSION 0.1
ENV PYTHONPATH "${PYTHONPATH}:/root/.local/lib/python3.7/site-packages"
RUN mkdir /opt/kaldi-lt

COPY ./model/kaldi-lt-lt-liepa2-0.1.tar.gz /opt/kaldi-lt/model.tar.gz
RUN cd /opt/kaldi-lt && tar -xzf model.tar.gz && rm model.tar.gz && mv kaldi-lt-lt-liepa2-0.1 model



COPY ./web /opt/vosk-server/websocket/web
COPY ./py/asr_server_lt.py /opt/vosk-server/websocket


EXPOSE 2700
WORKDIR /opt/vosk-server/websocket
CMD VOSK_SERVER_PORT=$PORT python3 ./asr_server_lt.py /opt/kaldi-lt/model
#CMD ["./wrapper_server.sh"]
