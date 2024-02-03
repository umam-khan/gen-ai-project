import React, { useState, useEffect } from 'react';

const SummaryPage = () => {
  const [vivaData, setVivaData] = useState({ hindi: '', english: '' }); // State to store fetched data
  const [isLoading, setIsLoading] = useState(true); // State to handle loading status
  const [error, setError] = useState(null); // State to handle any errors

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Assuming your Flask backend expects a POST request
        const response = await fetch('http://localhost:5000/getsummary', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          // If your POST request requires a body, add it here
          // body: JSON.stringify({ someKey: 'someValue' }),
        });

        if (!response.ok) {
          throw new Error('Something went wrong'); // Throw an error if response is not ok
        }

        const data = await response.json(); // Parse JSON response

        if (data.success) {
          setVivaData({ hindi: data.hindi, english: data.english }); // Update state with fetched data
        } else {
          setError(data.message || 'Failed to fetch data'); // Set error message if success is false
        }
      } catch (error) {
        setError(error.message); // Catch and set any errors that occur during fetch
      } finally {
        setIsLoading(false); // Ensure loading is set to false after fetch operation is complete
      }
    };

    fetchData(); // Call the async function to fetch data
  }, []); // Empty dependency array means this effect runs once on mount

  return (
    <div className="flex h-screen w-screen">
      {/* Sidebar */}
      <div className="bg-gray-800 text-white w-64 p-4 space-y-4">
        {/* Sidebar content */}
      </div>

      {/* Chat Container */}
      <div className="flex flex-col flex-1">
        <div className="overflow-y-auto p-4 space-y-4 bg-gray-100 flex-1">
          {/* Check for loading state */}
          {isLoading && <div>Loading...</div>}

          {/* Check for error state */}
          {error && <div>Error: {error}</div>}

          {/* Display the data if available and not loading */}
          {!isLoading && !error && (
            <div className="text-left">
              <div className="inline-block bg-gray-300 rounded px-4 py-2">
                <p><strong>English:</strong> {vivaData.english}</p>
                <p><strong>Hindi:</strong> {vivaData.hindi}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SummaryPage;
