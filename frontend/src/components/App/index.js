import React from 'react';
import './scoped.css';
import VoicEmail from '../../img/VoicEmail.png';
import FootImg from '../../img/foot.png';
import ChatBox from '../ChatBox/index';

const App = () => {
  return (
    < div className="App" >
      < div className="container" >
        <div className="nav-bar">
          <img style={{height:40,paddingRight:15}} src={VoicEmail} alt="voicemail"></img>
          <div className="nav-text">LinguAI</div>
        </div>
        <div className="header">VoicEmail Assistant</div>
        <div className="chat-box-container">
          <ChatBox></ChatBox>
        </div>
        <div className="foot">
          <img style={{ height: 50 }} src={FootImg}></img>
        </div>
      </div >
    </div >
  );
}

export default App;
