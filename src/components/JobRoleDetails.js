// src/components/JobRoleDetails.js
import React from "react";
import "../styles/JobRoleDetails.css";

const JobRoleDetails = ({ jobData }) => {
  if (!jobData) return <div>No data available.</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">{jobData.name}</h1>
      <p className="text-gray-700">{jobData.description}</p>

      <section>
        <h2 className="text-xl font-semibold">Required Skills</h2>
        <ul className="list-disc list-inside">
          {jobData.skills.map((skill, idx) => <li key={idx}>{skill}</li>)}
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold">Career Transitions</h2>
        <ul className="list-disc list-inside">
          {jobData.transitions.map((role, idx) => <li key={idx}>{role}</li>)}
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold">Related Roles</h2>
        <ul className="list-disc list-inside">
          {jobData.relatedRoles.map((role, idx) => <li key={idx}>{role}</li>)}
        </ul>
      </section>
    </div>
  );
};

export default JobRoleDetails;
