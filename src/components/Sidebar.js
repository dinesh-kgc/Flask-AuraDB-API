import React from "react";
import { Link } from "react-router-dom";
import "../App.css";

const Sidebar = () => (
  <div className="sidebar">
    <h2>Skill Mapping</h2>
    <nav>
      <ul>
        <li><Link to="/">Dashboard</Link></li>
        <li><Link to="/skill-graph">Skill Graph</Link></li>
        <li><Link to="/job-details">Job Role Details</Link></li>
      </ul>
    </nav>
  </div>
);

export default Sidebar;
