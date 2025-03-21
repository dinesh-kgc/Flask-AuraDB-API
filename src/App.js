import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import SkillGraph from "./components/SkillGraph";
import JobRoleDetails from "./components/JobRoleDetails";
import "./App.css";

const App = () => (
  <Router>
    <div className="container">
      <Sidebar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/skill-graph" element={<SkillGraph />} />
        <Route path="/job-details" element={<JobRoleDetails />} />
        <Route path="/job-role/:jobRoleName" element={<JobRoleDetails />} />
      </Routes>
    </div>
  </Router>
);

export default App;
