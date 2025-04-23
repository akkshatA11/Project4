import React from "react";
import "./Dashboard.css";
import Navbar from "./Navbar";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <>
      <Navbar />
      <div className="dashboard-container">
        <div className="dashboard-buttons">
          <button
            onClick={() => navigate("/qr-generator")}
            className="dashboard-btn"
          >
            QR Code Generator
          </button>
          <button
            onClick={() => navigate("/business-card")}
            className="dashboard-btn"
          >
            Business Card Generator
          </button>
        </div>
      </div>
    </>
  );
};

export default Dashboard;
