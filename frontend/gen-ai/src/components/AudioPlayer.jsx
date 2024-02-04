import React, { useState, useEffect } from 'react';

export default function AudioPlayer() {
  const [audioSrc, setAudioSrc] = useState('');

  useEffect(() => {
    // Dummy function to simulate updating the audio source
    const updateAudioSrc = () => {
      const timestamp = new Date().getTime(); // Get current timestamp
      setAudioSrc(`http://localhost:5000/audio?${timestamp}`);
    };

    updateAudioSrc(); // Call on component mount or in response to some event

    // Optional: set up an interval or listen to a specific event to update the source
  }, []); // Empty dependency array ensures this effect runs only once on mount

  return (
    <div className="flex justify-center items-center w-full">
      <audio controls src={audioSrc} className="w-full max-w-md z-0">
        Your browser does not support the audio element.
      </audio>
    </div>
  );
}