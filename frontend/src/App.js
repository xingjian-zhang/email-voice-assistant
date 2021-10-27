import React, { useState, useEffect } from 'react';
import './App.css';
import VoicEmail from './img/VoicEmail.png';
import MicRecorder from 'mic-recorder-to-mp3';
import FootImg from './img/foot.png';
import { AudioOutlined, AudioMutedOutlined } from '@ant-design/icons'
const Mp3Recorder = new MicRecorder({ bitRate: 128 });

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [blobURL, setBlobURL] = useState('');
  const [isBlocked, setIsBlocked] = useState(false);

  useEffect(() => {
    navigator.getUserMedia({ audio: true },
      () => {
        console.log('Permission Granted');
        setIsBlocked(false);
      },
      () => {
        console.log('Permission Denied');
        setIsBlocked(true);
      },
    );
  }, [])

  const startRecord = (() => {
    if (isBlocked) {
      console.log('Permission Denied');
    } else {
      setBlobURL('');
      Mp3Recorder
        .start()
        .then(() => {
          setIsRecording(true);
        }).catch((e) => console.error(e));
    }
  })

  const stopRecord = (() => {
    Mp3Recorder
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        // Create URL
        const curBlobURL = URL.createObjectURL(blob)
        setBlobURL(curBlobURL);
        setIsRecording(false);
        console.log(typeof (blob))

        // Save as file
        var file = new File(buffer, 'test.mp3', {
          type: blob.type,
          lastModified: Date.now()
        });

        var formData = new FormData();
        formData.append("voice", file, "test.mp3");
        formData.append("string", "sss")
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            console.log(xhr.responseText);
          }
        }
        xhr.open('POST', '/voice/');
        xhr.send(formData);

      }).catch((e) => console.log(e));
  })

  return (

    < div className="App" >
      < div className="container" >
        <div className="nav-bar">
          <img style={{height:55,paddingRight:15}} src={VoicEmail} alt="voicemail"></img>
          <div className="nav-text">LinguAI</div>
        </div>
        <div className="header">VoicEmail Assistant</div>
        <div className="intruction">Click on the mic to activate the intelligent VoicEmail assistant!</div>
        <div className="record-listen">
          {
            isRecording && (
              <AudioOutlined style={{ fontSize: 50 }} onClick={stopRecord} />
            )
          }
          {
            !isRecording && (
              < AudioMutedOutlined style={{ fontSize: 50 }} onClick={startRecord} />
            )
          }
          <audio src={blobURL} controls="controls" />
        </div>
        <div className="foot">
          <img style={{ height: 50 }} src={FootImg}></img>
        </div>
      </div >
    </div >
  );
}

export default App;
