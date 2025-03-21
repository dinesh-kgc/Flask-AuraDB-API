import React, { useEffect, useState, useRef } from 'react';
import CytoscapeComponent from 'react-cytoscapejs';
import axios from 'axios';

const SkillGraph = ({ onNodeClick }) => {
  const [elements, setElements] = useState([]);
  const cyRef = useRef(null);

  useEffect(() => {
    axios.get('https://flask-auradb-api.onrender.com/get_skills_graph')
      .then(response => {
        const { nodes, edges } = response.data;

        const formattedNodes = nodes.map(node => ({
          data: { id: node.id, label: node.label }
        }));

        const formattedEdges = edges.map(edge => ({
          data: { source: edge.source, target: edge.target }
        }));

        setElements([...formattedNodes, ...formattedEdges]);
      })
      .catch(error => console.error('Error fetching skills:', error));
  }, []);

  useEffect(() => {
    if (cyRef.current) {
      cyRef.current.on('tap', 'node', (evt) => {
        const nodeName = evt.target.data('label');
        console.log('Node clicked:', nodeName);
        if (onNodeClick) onNodeClick(nodeName);
      });
    }
  }, [elements, onNodeClick]);

  return (
    <div style={{ height: '600px', width: '100%' }}>
      <CytoscapeComponent
        elements={elements}
        style={{ width: '100%', height: '100%' }}
        cy={(cy) => {
          cyRef.current = cy;
          cy.layout({ name: 'cose' }).run();
        }}
      />
    </div>
  );
};

export default SkillGraph;
