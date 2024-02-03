import { useState } from "react";

import { Link } from "react-router-dom";
import PdfUpload from "../components/PdfUpload";

const MainPage = () => {
  let [recordOption, setRecordOption] = useState("text");

  const toggleRecordOption = (type) => {
    return () => {
      setRecordOption(type);
    };
  };

  // const sendDataToServer = async (data) => {
  //   try {
  //     const response = await fetch("http://localhost:5000/getinput", {
  //       method: "POST",
  //       body: data,
  //     });

  //     if (response.ok) {
  //       console.log("Data successfully sent to server");
  //     } else {
  //       console.error("Failed to send data to server");
  //     }
  //   } catch (error) {
  //     console.error("Error sending data to server:", error);
  //   }
  // };

  return (
    <div className="h-screen flex flex-col justify-center items-center space-y-5 font-sans text-base leading-6">
      <h1 className="text-4xl leading-11">Query Your PDF</h1>
      <PdfUpload />
      <div className="flex justify-center items-center gap-10">
        <Link to="/text">
          <button className="btn-dark">
            want to use text
          </button>
        </Link>
        <Link to="/audio">
          <button className="btn-dark">
            want to use audio
          </button>
        </Link>
        {/* <button
          onClick={toggleRecordOption("text")}
          className="btn-dark"
        >
          Send Text
        </button>
        <button
          onClick={toggleRecordOption("audio")}
          className="btn-dark"
        >
          Record Audio
  </button> */}
      </div>
      {/* <div>{recordOption === "text" ? <TextInput /> : <AudioRecorder />}</div>  */}
    </div>
  );
};

export default MainPage;
