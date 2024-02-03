import React from 'react';

function AudioPlayer() {
  const audioSrc = 'http://localhost:5000/audio'; // Change this URL to match your Flask server's address

  return (
    <div>
      <audio controls src={audioSrc}>
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}

export default AudioPlayer;
