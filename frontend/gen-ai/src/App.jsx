import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./pages/MainPage";
import Home from "./pages/Home";
import TextPage from "./pages/TextPage";
import AudioPage from "./pages/AudioPage";
import Navbar from "./components/Navbar";
import VivaPage from "./pages/VivaPage";
import SummaryPage from "./pages/SummaryPage";

const App = () => {
  return (
    <div>
    <BrowserRouter>
    <Navbar />
      <Routes>
          <Route path="/main" element={<MainPage />} />
          <Route path="/" element={<Home />} />
          <Route path="/text" element={<TextPage />} />
          <Route path="/audio" element={<AudioPage />} />
          <Route path="/viva" element={<VivaPage /> } />
          <Route path="/summary" element={<SummaryPage/> } />
      </Routes>
    </BrowserRouter>
    </div>
  );
};

export default App;