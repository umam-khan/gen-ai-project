import React, { useState } from 'react';
// Assuming TextInput and AudioRecorder are your custom components
import TextInput from '../TextInput';
import AudioRecorder from '../AudioRecorder';

const AudioPage = () => {
  const [textValue, setTextValue] = useState('');
  // URL of the audio file placed in the public folder
  const audioSrc = '/Conference.wav'; // Adjust this path if your setup is different

  const updateTextValue = (value) => {
    setTextValue(value);
  };

  return (
    <div className="flex h-screen w-screen">
      {/* Sidebar */}
      <div className="bg-gray-800 text-white w-64 p-4 space-y-4">
        <div className="text-xl font-semibold">ChatGPT</div>
        <div>
          <div className="text-gray-300 text-sm">History</div>
          <ul className="space-y-2 mt-3">
            <li>Conversation 1</li>
            <li>Conversation 2</li>
            {/* More conversations can be added here */}
          </ul>
        </div>
      </div>

      {/* Chat Container */}
      <div className="flex flex-col flex-1">
        <div className="overflow-y-auto p-4 space-y-4 bg-gray-100 flex-1">
          {/* Instead of displaying textValue, an audio player is shown */}
          <audio controls src={audioSrc}>
            Your browser does not support the audio element.
          </audio>
        </div>
  
        {/* Below is where your AudioRecorder component is rendered */}
        <AudioRecorder />
      </div>
    </div>
  );
}

export default AudioPage;
