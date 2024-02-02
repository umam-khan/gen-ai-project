import React from 'react'
import AudioRecorder from '../AudioRecorder'

const AudioPage = () => {
  return (
    <div className="flex h-screen w-screen">
    {/* <!-- Sidebar --> */}
    <div className="bg-gray-800 text-white w-64 p-4 space-y-4">
      <div className="text-xl font-semibold">ChatGPT</div>
      <div>
        <div className="text-gray-300 text-sm">History</div>
  
        <ul className="space-y-2 mt-3">
          <li>Conversation 1</li>
          <li>Conversation 2</li>
          {/* <!-- More conversations --> */}
        </ul>
      </div>
    </div>
  
    {/* <!-- Chat Container --> */}
    <div className="flex flex-col flex-1">
      <div className="overflow-y-auto p-4 space-y-4 bg-gray-100 flex-1">
        <div className="text-right">
          <div className="inline-block bg-blue-500 text-white rounded px-4 py-2">
            User message
          </div>
        </div>
        <div className="text-left">
          <div className="inline-block bg-gray-300 rounded px-4 py-2">
            ChatGPT response
          </div>
        </div>
      </div>
  
      {/* <!-- Input Area --> */}
      <AudioRecorder />
    </div>
  </div>
    // <div><h1>audio page</h1>

    // <AudioRecorder />
    // </div>
  )
}

export default AudioPage