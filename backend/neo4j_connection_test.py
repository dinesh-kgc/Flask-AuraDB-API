from neo4j import GraphDatabase

NEO4J_URI = "neo4j+s://c6616c00.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "HQJae1LsEdIVYEyJYstlKgSQgG3GsjqGQKKnZw-08Sc"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def test_connection():
    try:
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN COUNT(n) AS node_count")
            for record in result:
                print(f"Node Count: {record['node_count']}")
        print("✅ Neo4j Connection Successful!")
    except Exception as e:
        print(f"❌ Neo4j Connection Failed: {e}")

test_connection()
