import React, { useState } from "react";
import axios from "axios";

function McqPage() {
  const [topic, setTopic] = useState("");
  const [number, setNumber] = useState(1);
  const [mcqs, setMcqs] = useState(null);
  const [error, setError] = useState("");

  const [check, setCheck] = useState(null);
  const fetchMCQs = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/getmcq",
        new URLSearchParams({
          topic,
          number,
        })
      );
      setMcqs(response.data);
      console.log(response);
      console.log(response.data);
      console.log(response.data[0]);
      setError("");
    } catch (err) {
      setError("Failed to fetch MCQs.");
      console.error(err);
    }
  };

  function tryParseJSONObject(jsonString) {
    try {
      var o = JSON.parse(jsonString);

      // Handle non-exception-throwing cases:
      // Neither JSON.parse(false) or JSON.parse(1234) throw errors, hence the type-checking,
      // but... JSON.parse(null) returns null, and typeof null === "object",
      // so we must check for that, too. Thankfully, null is falsey, so this suffices:
      if (o && typeof o === "object") {
        console.log(`yes json`);
        console.log(o);
        return o;
      }
    } catch (e) {}
    console.log(`not json`);
    return false;
  }

  return (
    <div className="App">
      <h1>Fetch MCQs</h1>
      <form onSubmit={fetchMCQs}>
        <div>
          <label>Topic: </label>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
        </div>
        <div>
          <label>Number: </label>
          <input
            type="number"
            value={number}
            onChange={(e) => setNumber(e.target.value)}
          />
        </div>
        <button type="submit">Fetch MCQs</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div>
        <div style={{ color: "red" }}>{mcqs && <p>{mcqs}</p>}</div>
        <div style={{ color: "blue" }}>{mcqs && <p>{mcqs[0]}</p>}</div>
        <div style={{ color: "green" }}>
          {mcqs?.length > 0 && <p>{mcqs[0].question}</p>}
        </div>
        <div>
          <button
            onClick={() => {
              tryParseJSONObject(mcqs);
            }}
            className="rounded text-xl p-3"
          >
            check json
          </button>
        </div>
      </div>
    </div>
  );
}

export default McqPage;
