import React, { useState } from 'react';
import TextInput from '../components/TextInput'; // Ensure this path matches your file structure

const TextPage = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const addToChatHistory = (userText, serverResponse) => {
    setIsLoading(true);
    setChatHistory(prevHistory => [...prevHistory, { userText, serverResponse }]);
  };

  return (
    <div className="flex h-screen w-screen">
      {/* Main content */}
      <div className="flex flex-col flex-1">
      {isLoading && (
         <div className="flex justify-center items-center h-screen">
         <div className="rounded-full h-20 w-20 bg-violet-800 animate-ping"></div>
       </div>
        )}
        {!isLoading && (
          <>
          <div className="overflow-y-auto p-4 space-y-4 bg-gray-100 flex-1">
          {chatHistory.map((chat, index) => (
            <div key={index} className="text-left space-y-2">
              <div className="inline-block bg-blue-300 rounded px-4 py-2 text-black">
                User: {chat.userText}
              </div>
              <div className="inline-block bg-gray-300 rounded px-4 py-2 text-black">
                Server: {chat.serverResponse}
              </div>
            </div>
          ))}
        </div>
        <TextInput updateTextValue={addToChatHistory}  setIsLoading={setIsLoading} />
          </>
        )}
        
      </div>
    </div>
  );
};

export default TextPage;
