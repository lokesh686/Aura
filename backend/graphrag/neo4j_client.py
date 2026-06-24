import os
from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self):
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "aura_password")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_policy_node(self, policy_id: str, title: str, description: str):
        query = """
        MERGE (p:Policy {id: $policy_id})
        SET p.title = $title, p.description = $description
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query, policy_id=policy_id, title=title, description=description)
            return result.single()

    def create_resource_node(self, resource_id: str, resource_type: str):
        query = """
        MERGE (r:Resource {id: $resource_id})
        SET r.type = $resource_type
        RETURN r
        """
        with self.driver.session() as session:
            result = session.run(query, resource_id=resource_id, resource_type=resource_type)
            return result.single()

    def create_governance_relationship(self, policy_id: str, resource_id: str):
        query = """
        MATCH (p:Policy {id: $policy_id})
        MATCH (r:Resource {id: $resource_id})
        MERGE (p)-[:GOVERNS]->(r)
        """
        with self.driver.session() as session:
            session.run(query, policy_id=policy_id, resource_id=resource_id)

    def get_policies_for_resource(self, resource_id: str):
        query = """
        MATCH (p:Policy)-[:GOVERNS]->(r:Resource {id: $resource_id})
        RETURN p.id AS policy_id, p.title AS title, p.description AS description
        """
        with self.driver.session() as session:
            result = session.run(query, resource_id=resource_id)
            return [{"policy_id": record["policy_id"], "title": record["title"], "description": record["description"]} for record in result]

# Singleton instance for the app
neo4j_client = Neo4jClient()
