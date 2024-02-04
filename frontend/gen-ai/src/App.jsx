import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./pages/MainPage";
import Home from "./pages/Home";
import TextPage from "./pages/TextPage";
import AudioPage from "./pages/AudioPage";
import Navbar from "./components/Navbar";
import VivaPage from "./pages/VivaPage";
import SummaryPage from "./pages/SummaryPage";
import AuthenticatedWrapper from "./AuthenticatedWrapper"; // adjust the import path as needed

const App = () => {
  return (
    <div className="w-screen min-h-screen bg-gradient-to-r from-rose-100 to-teal-100">
    <BrowserRouter>
    <Navbar />
      <Routes>
          <Route path="/main" element={<AuthenticatedWrapper>
                <MainPage />
              </AuthenticatedWrapper>} />
          <Route path="/" element={<Home />} />
          <Route path="/text" element={<AuthenticatedWrapper><TextPage /></AuthenticatedWrapper>} />
          <Route path="/audio" element={<AuthenticatedWrapper><AudioPage /></AuthenticatedWrapper>} />
          <Route path="/viva" element={<AuthenticatedWrapper><VivaPage /></AuthenticatedWrapper> } />
          <Route path="/summary" element={<AuthenticatedWrapper><SummaryPage/></AuthenticatedWrapper> } />
      </Routes>
    </BrowserRouter>
    </div>
  );
};

export default App;