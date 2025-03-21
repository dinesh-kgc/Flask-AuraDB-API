// src/components/Dashboard.js
import React, { useState } from "react";
import SkillGraph from "./SkillGraph";
import JobRoleDetails from "./JobRoleDetails";

// TEMP: mock job role data (replace with dynamic later)
const mockJobRoles = [
  {
    name: "Data Scientist",
    description: "Analyzes complex data to support business decisions.",
    skills: ["Python", "Machine Learning", "SQL"],
    transitions: ["AI Engineer", "ML Researcher"],
    relatedRoles: ["Data Analyst", "Data Engineer"]
  },
  {
    name: "Frontend Developer",
    description: "Builds UI using HTML, CSS, JavaScript, React.",
    skills: ["HTML", "CSS", "React", "JavaScript"],
    transitions: ["UI/UX Designer", "Full Stack Developer"],
    relatedRoles: ["Backend Developer", "Web Designer"]
  }
];

const Dashboard = () => {
  const [selectedJob, setSelectedJob] = useState(null);

  const handleNodeClick = (jobName) => {
    const match = mockJobRoles.find(
      (job) => job.name.toLowerCase() === jobName.toLowerCase()
    );
    setSelectedJob(match ?? null);
  };

  return (
    <div className="p-4">
      {!selectedJob && (
        <SkillGraph onNodeClick={handleNodeClick} />
      )}

      {selectedJob && (
        <div>
          <button
            onClick={() => setSelectedJob(null)}
            className="mb-4 px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded"
          >
            ← Back to Graph
          </button>
          <JobRoleDetails jobData={selectedJob} />
        </div>
      )}
    </div>
  );
};

export default Dashboard;
