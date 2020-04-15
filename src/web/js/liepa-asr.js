var gworker;
var gpaused = true;
var gintervalKey;
//const wsUrl  = "wss://liepa-kaldi.herokuapp.com/0.0.0.0";
const wsUrl  = "ws://localhost:2700";
var gws;

document.getElementById("startBtn").onclick = function() {
  if(gws === undefined){
    navigator.mediaDevices.getUserMedia({ audio: true, sampleRate: 16000, video: false })
      .then(handleSuccess);
      
  }
  resume();
  
      
};

const handleSuccess = function(stream) {
  const context = new AudioContext();
  const source = context.createMediaStreamSource(stream);
  const processor = context.createScriptProcessor(1024, 1, 1);

  source.connect(processor);
  processor.connect(context.destination);

  initWorker(source, processor);
  createWebSocket();

};


function initWorker(source, processor){
  gworker = new Worker('js/recorder-worker.js');

  gworker.onmessage = (e) => {
    if (gpaused) return;
    var blob = e.data;
    socketSend(blob);
  };
  processor.onaudioprocess = function(e) {
    if (gpaused) return;
    gworker.postMessage({
      command: 'record',
      buffer: [
        e.inputBuffer.getChannelData(0)
      ]
    });
  };
  console.log("source.context.sampleRate", source.context.sampleRate);
  
  gworker.postMessage({
    command: 'init',
    config: {
      sampleRate: source.context.sampleRate
    }
  })
}


function createWebSocket() {
  gws = new WebSocket(wsUrl);  
  gws.onopen = function() {
      // Web Socket is connected, send data using send()
      gws.send('{"config" : {"sample_rate" : 16000.0}}');
      console.log("Connection is opened..."); 
      gintervalKey = setInterval(exportWorkerData, 250)
  };
  gws.onmessage = function (evt) { 
      var received_msg = evt.data;
      // console.log("Message is received...", received_msg);
      const msg_obj = JSON.parse(received_msg);
      // console.log(msg_obj);
      
      if(msg_obj["result"]){
          // console.log("msg_obj", msg_obj);
          
          document.getElementById("tipsForRecognition").textContent = "Girdėjau, kad sakėte: ";
          document.getElementById("recognized").textContent = msg_obj["text"];
          pause();
      }else if(msg_obj["partial"]){
          // console.log("msg_obj", msg_obj);
          document.getElementById("tipsForRecognition").textContent = "Šnekėkite, aš girdžiu: ";
          document.getElementById("recognized").textContent = msg_obj["partial"];
      }
  };
  gws.onclose = function() {   
      // websocket is closed.
      console.log("Connection is closed..."); 
  };
  gws.onerror = function(e) {   
    // websocket is closed.
    console.log("Connection error...", e); 
  };
  
  
}

function socketSend(blob) {
  if (gpaused)
    return;
  if (gws) {
    var state = gws.readyState;
    if (state == 1) {
      // If blob is an audio blob
      if (blob instanceof Blob) {
        if (blob.size > 0) {
          gws.send(blob);
          // this.config.onEvent(this.MSG_SEND, 'Send: blob: ' + blob.type + ', ' + blob.size);
          console.log('Send: blob: ' + blob.type + ', ' + blob.size);
        } else {
          // this.config.onEvent(this.MSG_SEND_EMPTY, 'Send: blob: ' + blob.type + ', EMPTY');
          console.log('Send: blob: ' + blob.type + ', EMPTY');
          
        }
        // Otherwise it's the EOS tag (string)
      } else {
        gws.send(blob);
      //   this.config.onEvent(this.MSG_SEND_EOS, 'Send tag: ' + blob);
      console.log('Send tag: ' + blob);
      }
    } else {mediaDevices.getUserMedia({ audio: true, video: false })
    //     .then(ha
      // this.config.onError(this.ERR_NETWORK, 'WebSocket: readyState!=1: ' + state + ": failed to send: " + blob);
      console.log('WebSocket: readyState!=1: ' + state + ": failed to send: " + blob);
      
    }
  } else {
    // this.config.onError(this.ERR_CLIENT, 'No web socket connection: failed to send: ' + blob);
    console.log( 'No web socket connection: failed to send: ' + blob);
  }
}


function exportWorkerData() {
  gworker.postMessage({ command: 'exportData' });
}

function resume() {
  gpaused = false;
  document.getElementById("tipsForRecognition").textContent = "Šnekėkite. ";
  document.getElementById("recognized").textContent ="";
  document.getElementById("startBtn").classList.toggle("invisible");
}

function pause() {
  gpaused = true;
  // document.getElementById("startBtn").style.display = "block";
  document.getElementById("startBtn").classList.toggle("invisible");
}
