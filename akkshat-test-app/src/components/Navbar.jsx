import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();

  const handleSignOut = (e) => {
    e.preventDefault(); // prevent page refresh
    localStorage.removeItem('user'); // clear login state
    navigate('/');
  };

  return (
    <nav className="navbar">
      <h2 className="logo">MyApp</h2>
      <ul className="nav-links">
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/qr-generator">QR Generator</Link></li>
        <li><Link to="/business-card">Business Card</Link></li>
        <li><a href="/" onClick={handleSignOut} className="nav-link-btn">Sign Out</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;
