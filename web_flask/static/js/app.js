
//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream;              //stream from getUserMedia()
var rec;                    //Recorder.js object
var input;                  //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //new audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

window.onload = init;
var context;    // Audio context
var buf;        // Audio buffer

function init() {
if (!window.AudioContext) {
    if (!window.webkitAudioContext) {
        alert("Your browser does not support any AudioContext and cannot play back this audio.");
        return;
    }
        window.AudioContext = window.webkitAudioContext;
    }

    context = new AudioContext();
}

// Audio 파일 만들기
function playByteArray(byteArray) {

    var arrayBuffer = new ArrayBuffer(byteArray.length);
    var bufferView = new Uint8Array(arrayBuffer);
    for (i = 0; i < byteArray.length; i++) {
      bufferView[i] = byteArray[i];
    }

    context.decodeAudioData(arrayBuffer, function(buffer) {
        buf = buffer;
        console.log(buf)
        play();
    });
}

// // Play the loaded file
// function play() {
//     // Create a source node from the buffer
//     var source = context.createBufferSource();
//     source.buffer = buf;
//     // Connect to the final output node (the speakers)
//     source.connect(context.destination);
//     // Play immediately
//     source.start(0);
// }

function startRecording() {
  console.log("recordButton clicked");

  // Disable the record button until we get a success or fail from getUserMedia()
  recordButton.disabled = true;
  stopButton.disabled = false;

  navigator.mediaDevices.getUserMedia({audio: true, video: false}).then(function(stream) {
      console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

      audioContext = new AudioContext({sampleRate: 16000});

      // assign to gumStream for later use
      gumStream = stream;

      // use the stream
      input = audioContext.createMediaStreamSource(stream);

      // Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size
      rec = new Recorder(input, {numChannels: 1})

      //start the recording process
      rec.record()

      console.log("Recording started");

  }).catch(function(err) {
      //enable the record button if getUserMedia() fails
      recordButton.disabled = false;
      stopButton.disabled = true;
  });
}

function stopRecording() {
  console.log("stopButton clicked");

  //disable the stop button, enable the record too allow for new recordings
  stopButton.disabled = true;
  recordButton.disabled = false;

  //tell the recorder to stop the recording
  rec.stop(); //stop microphone access
  gumStream.getAudioTracks()[0].stop();

  //create the wav blob and pass it on to createDownloadLink
  rec.exportWAV(createDownloadLink);



function createDownloadLink(blob) {
  var url = URL.createObjectURL(blob);
  var au = document.createElement('audio');
  var li = document.createElement('li');
  var link = document.createElement('a');

  //name of .wav file to use during upload and download (without extension)
  var filename = new Date().toISOString();

  //add controls to the <audio> element
  au.controls = true;
  au.src = url;

  //save to disk link
  link.href = url;
  link.download = filename+".wav"; //download forces the browser to download the file using the  filename
  link.innerHTML = "Save to disk";

  // //add the new audio element to li
  // li.appendChild(au);
  
  // //add the filename to the li
  // li.appendChild(document.createTextNode(filename+".wav "))

  // //add the save to disk link to li
  // li.appendChild(link);

  // //add the li element to the ol
  // recordingsList.appendChild(li);

    /* button이 클릭되었을때 이벤트 */

    var data = new FormData();
    data.append('file', blob, 'filename');

    var xhr = new XMLHttpRequest();


    data.enctype='multipart/form-data';
    data.method='post';
    // formdata.action='FormDataResult.jsp';


    xhr.open('post','/service_qa', true); 
    
    xhr.responseType = "json";

    // xhr.onreadystatechange = 콜백함수명;
    xhr.send(data);
    /* 통신에 사용 될 XMLHttpRequest 객체 정의 */
    /* httpRequest의 readyState가 변화했을때 함수 실행 */
      xhr.onreadystatechange = () => {
        /* readyState가 Done이고 응답 값이 200일 때, 받아온 response로 name과 age를 그려줌 */
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
            var result = xhr.response;
            console.log(result)
            // https://stackoverflow.com/questions/38926335/flask-redirecturl-for-returning-html-but-not-loading-page
            window.location = "/feedback";

              // document.getElementById("ans_t").innerText = result.answer[0];
              // document.getElementById("ans_p").innerText = result.answer[1];
              // document.getElementById("deaf_t").innerText = result.deaf[0];
              // document.getElementById("deaf_p").innerText = result.deaf[1];
              // document.getElementById("result_acc").innerText = result.result[0];
              // document.getElementById("result_score").innerText = result.result[1];
              // playByteArray(result.wav)
              // console.log(document.getElementsByClassName("invisible"));
              // const inv =  document.querySelector('.invisible');
              // inv.classList.remove('invisible');

            } else {
              alert('request에 뭔가 문제가 있어요.');
            }
      }
      };
    //   /* Post 방식으로 요청 */
    //   httpRequest.open('POST', '/record', true);
    //   /* Response Type을 Json으로 사전 정의 */
    //   httpRequest.responseType = "json";
    //   /* 요청 Header에 컨텐츠 타입은 Json으로 사전 정의 */
    //   httpRequest.setRequestHeader('Content-Type', 'application/blob');
    //   /* 정의된 서버에 Json 형식의 요청 Data를 포함하여 요청을 전송 */
    //   // httpRequest.send(JSON.stringify(reqJson));
    // httpRequest.send(data)
      

  }


}

