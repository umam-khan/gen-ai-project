import React from 'react';

const TextInput = () => {
  const sendDataToServer = async (data) => {
    try {
      const response = await fetch("http://localhost:5000/gettext", {
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
  };

  const sendTextInputToServer = async () => {
    const textInput = document.getElementById("text").value;

    const formData = new FormData();
    formData.append("inputType", "text");
    formData.append("language", "English");
    formData.append("text", textInput);
    formData.append("audio", null); // Audio input is NULL for text input

    sendDataToServer(formData);
  };

  return (
    <div>
      <form onSubmit={(e)=>{
        e.preventDefault();
      }} className="">
        {/* <label htmlFor="text" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          your question
        </label> */}
        <div p-4 border-gray-200>
        <div className='flex gap-4'>
        <input
          type="text"
          id="text"
          aria-describedby="helper-text-explanation"
          className="flex-1 p-2 border border-gray-300 rounded"
          placeholder="what do you wanna know.."
        />
        <button className='btn-default text-white rounded px-4 py-2'
        onClick={() => {
          sendTextInputToServer();
        }}
      >
        send text
      </button>
      </div>
      </div>
        
      </form>
      <p id="helper-text-explanation" className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          We’ll never share your details. Read our{' '}
          <a href="#" className="font-medium text-blue-600 hover:underline dark:text-blue-500">
            Privacy Policy
          </a>
        </p>
    </div>
  );
};

export default TextInput;
