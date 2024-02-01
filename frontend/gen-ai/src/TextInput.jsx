import React from 'react';

const TextInput = () => {
  const sendDataToServer = async (data) => {
    try {
      const response = await fetch("http://localhost:5000/getinput", {
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
      <h2>Text Input</h2>
      <form className="max-w-sm mx-auto">
        <label htmlFor="text" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          your question
        </label>
        <input
          type="text"
          id="text"
          aria-describedby="helper-text-explanation"
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="what do you wanna know.."
        />

        <p id="helper-text-explanation" className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          We’ll never share your details. Read our{' '}
          <a href="#" className="font-medium text-blue-600 hover:underline dark:text-blue-500">
            Privacy Policy
          </a>
          .
        </p>
      </form>
      <button
        onClick={() => {
          sendTextInputToServer();
        }}
      >
        send text
      </button>
    </div>
  );
};

export default TextInput;
