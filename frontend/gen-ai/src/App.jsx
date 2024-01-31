import "./App.css";
import { useState } from "react";

import AudioRecorder from "../src/AudioRecorder";

const App = () => {
	// let [recordOption, setRecordOption] = useState("video");

	// const toggleRecordOption = (type) => {
	// 	return () => {
	// 		setRecordOption(type);
	// 	};
	// };

	return (
		<div className="min-h-screen flex flex-col py-5 space-x-8 space-y-5 justify-center items-center">
			<h1 className="font-semibold underline">Audio Recorder</h1>
      <div>
			<div className="button-flex">
				<button className="bg-red-100">Record Audio</button>
			</div>
			<div>
				{<AudioRecorder />}
			</div>
      </div>
		</div>
	);
};

export default App;