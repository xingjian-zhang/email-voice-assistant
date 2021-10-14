import React, { useState, useEffect } from 'react';
import './App.css';
import MicRecorder from 'mic-recorder-to-mp3';
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
        const curBlobURL = URL.createObjectURL(blob)
        setBlobURL(curBlobURL);
        setIsRecording(false);
        console.log(typeof (blob))
      }).catch((e) => console.log(e));
  })

  return (

    < div className="App" >
      < div className="container" >
        <div className="header">VoicEmail Assistant</div>
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
      </div >
    </div >
  );
}

export default App;
