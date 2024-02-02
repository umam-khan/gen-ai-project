import { useState, useRef } from "react";

const mimeType = "audio/webm";

const AudioRecorder = () => {
  const [permission, setPermission] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState("english");
  const mediaRecorder = useRef(null);
  const [recordingStatus, setRecordingStatus] = useState("inactive");
  const [stream, setStream] = useState(null);
  const [audio, setAudio] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);

  const getMicrophonePermission = async () => {
    if ("MediaRecorder" in window) {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          audio: true,
          video: false,
        });
        setPermission(true);
        setStream(mediaStream);
      } catch (err) {
        alert(err.message);
      }
    } else {
      alert("The MediaRecorder API is not supported in your browser.");
    }
  };

  const startRecording = async () => {
    setRecordingStatus("recording");
    const media = new MediaRecorder(stream, { type: mimeType });

    mediaRecorder.current = media;

    mediaRecorder.current.start();

    let localAudioChunks = [];

    mediaRecorder.current.ondataavailable = (event) => {
      if (typeof event.data === "undefined") return;
      if (event.data.size === 0) return;
      localAudioChunks.push(event.data);
    };

    setAudioChunks(localAudioChunks);
  };

  const stopRecording = async () => {
    setRecordingStatus("inactive");
    mediaRecorder.current.stop();

    mediaRecorder.current.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: mimeType });

      // const reader = new FileReader();
      // reader.onloadend = () => {
        // const audioBase64 = reader.result;

        const formData = new FormData();
        formData.append("inputType", "audio");
        formData.append("language", selectedLanguage);
        formData.append("text", "NULL");
        formData.append("audio", audioBlob, "recordedAudio.weba");

        sendDataToServer(formData);
      // };

      // reader.readAsDataURL(audioBlob);
    };
  };

  const sendDataToServer = async (data) => {
    try {
      const response = await fetch("http://localhost:5000/getaudio", {
        method: "POST",
        body: data,
      });

      if (response.ok) {
        console.log("Data successfully sent to server");
        console.log(data);
      } else {
        console.error("Failed to send data to server");
      }
    } catch (error) {
      console.error("Error sending data to server:", error);
    }

    setAudioChunks([]);
  };

  return (
    <div>
      <main className="font-sans text-base leading-6">
        <div className="space-y-4">
          {!permission ? (
            <button
              onClick={getMicrophonePermission}
              className="btn-default"
              type="button"
            >
              Get Microphone
            </button>
          ) : null}
          {permission && recordingStatus === "inactive" ? (
            <div className="space-x-4">
              <button
                onClick={startRecording}
                className="btn-dark"
                type="button"
              >
                Start Recording
              </button>
              <label className="flex items-center space-x-2 mr-2">
                Language:
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="py-2 px-4 border border-gray-300 rounded-md bg-white focus:outline-none focus-visible:ring focus-visible:border-blue-300 transition-border-color"
                >
                  <option value="english">English</option>
                  <option value="hindi">Hindi</option>
                </select>
              </label>
            </div>
          ) : null}
          {recordingStatus === "recording" ? (
            <button
              onClick={stopRecording}
              className="btn-danger"
              type="button"
            >
              Stop Recording
            </button>
          ) : null}
        </div>
        {audio ? (
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <audio
                src={audio}
                controls
                className="border border-gray-300 rounded-md"
              ></audio>
              <a
                download
                href={audio}
                className="text-blue-500 hover:underline"
              >
                Download Recording
              </a>
            </div>
          </div>
        ) : null}
      </main>
    </div>
  );
};

export default AudioRecorder;
