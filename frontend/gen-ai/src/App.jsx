import "./App.css";
import { useState } from "react";

import AudioRecorder from "../src/AudioRecorder";
import TextInput from "./TextInput";

const App = () => {
	let [recordOption, setRecordOption] = useState("text");

	const toggleRecordOption = (type) => {
		return () => {
			setRecordOption(type);
		};
	};
	const sendDataToServer = async (data) => {
		try {
		  const response = await fetch("http://localhost:5000/getinput", {
			method: "POST",
			body: data,
		  });
	
		  if (response.ok) {
			console.log("Data successfully sent to server");
		  } else {
			console.error("Failed to send data to server");
		  }
		} catch (error) {
		  console.error("Error sending data to server:", error);
		}
	  };
	
	  return (
		<div className="min-h-screen flex flex-col justify-center items-center space-y-5">
		  <h1>Query Your PDF</h1>
		  <div className="button-flex">
			<button onClick={toggleRecordOption("text")}>Send Text</button>
			<button onClick={toggleRecordOption("audio")}>Record Audio</button>
		  </div>
		  <div>
			{recordOption === "text" ? (
			  <TextInput />
			) : (
			  <AudioRecorder />
			)}
		  </div>
		</div>
	  );
	};

export default App;