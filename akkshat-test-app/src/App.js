import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";
import Dashboard from "./components/Dashboard";
// import QRGenerator from "./components/QRGenerator";
// import BusinessCard from "./components/BusinessCard";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {/* <Route path="/qr-generator" element={<QRGenerator />} />
        <Route path="/business-card" element={<BusinessCard />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
