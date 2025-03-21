
from flask import Flask, jsonify, request
from flask_cors import CORS
from neo4j import GraphDatabase

import os



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "https://skill-mapping-ui.vercel.app"}})


# Neo4j Connection Details (Replace with your AuraDB credentials)
NEO4J_URI = "neo4j+s://c6616c00.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "HQJae1LsEdIVYEyJYstlKgSQgG3GsjqGQKKnZw-08Sc"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Function to execute a query
def execute_query(query, parameters={}):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]

# API Endpoints

@app.route('/test', methods=['GET'])
def test():
    return "Flask is working!", 200

@app.route('/get_skills_graph', methods=['GET'])
def get_skills_graph():
    try:
        query = """
        MATCH (s:Skill)
        OPTIONAL MATCH (s)-[r:COMPLEMENTS|REQUIRES]->(s2:Skill)
        RETURN s.name AS skill_name, 
               collect({related_skill: s2.name}) AS related_skills
        """
        result = execute_query(query)

        # Formatting the response
        nodes = []
        edges = []
        for record in result:
            skill_name = record["skill_name"]
            nodes.append({"id": skill_name, "label": skill_name, "type": "skill"})

            # Add relationships (edges)
            for related in record["related_skills"]:
                if related["related_skill"]:  # Avoid None values
                    edges.append({"source": skill_name, "target": related["related_skill"], "relationship": "COMPLEMENTS/REQUIRES"})

        return jsonify({"nodes": nodes, "edges": edges})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/get_job_roles', methods=['GET'])
def get_job_roles():
    try:
        query = """
            MATCH (j:JobRole)
            OPTIONAL MATCH (j)-[:REQUIRES]->(s:Skill)
            OPTIONAL MATCH (j)-[:TRANSITIONS_TO]->(nextRole:JobRole)
            OPTIONAL MATCH (j)-[:RELATED_TO]->(relatedRole:JobRole)
            RETURN j.name AS job_role,
                j.description AS description,
                collect(DISTINCT s.name) AS required_skills,
                collect(DISTINCT nextRole.name) AS career_transitions,
                collect(DISTINCT relatedRole.name) AS related_roles
        """
        result = execute_query(query)

        job_roles = []
        for record in result:
            job_roles.append({
                "job_role": record["job_role"],
                "description": record["description"] if record["description"] else "No description available",
                "required_skills": record["required_skills"],
                "career_transitions": record["career_transitions"],
                "related_roles": record["related_roles"]
            })
        return jsonify(job_roles)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/get_career_transitions', methods=['GET'])
def get_career_transitions():
    query = """
    MATCH (j1:JobRole)-[:TRANSITIONS_TO]->(j2:JobRole)
    RETURN j1.name AS from_role, j2.name AS to_role
    """
    result = execute_query(query)
    return jsonify(result)

@app.route('/get_role_skills', methods=['GET'])
def get_role_skills():
    job_role = request.args.get('job_role')
    query = """
    MATCH (j:JobRole {name: $job_role})-[:REQUIRES]->(s:Skill)
    RETURN s.name AS required_skill
    """
    result = execute_query(query, {'job_role': job_role})
    return jsonify(result)

@app.route('/recommend_roles', methods=['POST'])
def recommend_roles():
    user_skills = request.json.get('skills', [])
    query = """
    MATCH (j:JobRole)-[:REQUIRES]->(s:Skill)
    WHERE s.name IN $skills
    RETURN j.name AS recommended_role, COUNT(s) AS matching_skills
    ORDER BY matching_skills DESC LIMIT 3
    """
    result = execute_query(query, {'skills': user_skills})
    return jsonify(result)

@app.route('/get_skill_details', methods=['GET'])
def get_skill_details():
    skill_name = request.args.get('skill', '').strip()
    if not skill_name:
        return jsonify({"error": "Missing skill parameter"}), 400

    query = """
    MATCH (s:Skill {name: $skill_name})
    OPTIONAL MATCH (s)<-[:REQUIRES]-(j:JobRole)
    RETURN s.name AS name,
           s.type AS type,
           s.category AS category,
           s.weightage AS weightage,
           COLLECT(j.name) AS job_roles
    """
    result = execute_query(query, {'skill_name': skill_name})
    record = result[0] if result else None

    if not record:
        return jsonify({"error": "Skill not found"}), 404

    return jsonify({
        "name": record["name"],
        "type": record["type"] or "Unknown",
        "category": record["category"] or "Uncategorized",
        "weightage": record["weightage"] or "N/A",
        "job_roles": record["job_roles"] or []
    })



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if no PORT env var
    app.run(host="0.0.0.0", port=port, debug=True)
