import os
from graphrag.neo4j_client import neo4j_client
from graphrag.pgvector_client import pgvector_client

# We use a dummy embedding array of size 1536 to simulate an OpenAI text embedding
def get_dummy_embedding():
    return [0.0123] * 1536

def seed_databases():
    print("Seeding Neo4j Knowledge Graph...")
    
    # 1. Create Compliance Policies
    policy_soc2 = "SOC2-001"
    neo4j_client.create_policy_node(
        policy_soc2, 
        "SOC2 S3 Encryption", 
        "All S3 buckets containing PII must be encrypted and private."
    )
    
    policy_gdpr = "GDPR-001"
    neo4j_client.create_policy_node(
        policy_gdpr, 
        "GDPR Database Security", 
        "All databases storing EU citizen data must be encrypted at rest."
    )

    # 2. Create Infrastructure Resources
    res_s3 = "user-data-bucket"
    neo4j_client.create_resource_node(res_s3, "S3")
    
    res_rds = "finance-db"
    neo4j_client.create_resource_node(res_rds, "RDS")

    # 3. Create 'GOVERNS' Relationships (Mapping Policies to Infra)
    neo4j_client.create_governance_relationship(policy_soc2, res_s3)
    neo4j_client.create_governance_relationship(policy_gdpr, res_rds)
    print("✅ Neo4j Seeding Complete!")

    print("Seeding PostgreSQL pgvector Semantic Search Data...")
    
    # 4. Insert full compliance text and vector embeddings into Postgres
    pgvector_client.insert_document(
        policy_soc2, 
        "According to SOC2 guidelines, to protect PII, any S3 bucket utilized for storage must strictly enforce server-side encryption (SSE-S3 or SSE-KMS) and block public access completely. Unencrypted buckets pose a severe risk.",
        get_dummy_embedding()
    )
    
    pgvector_client.insert_document(
        policy_gdpr, 
        "GDPR Article 32 requires the implementation of appropriate technical and organizational measures to ensure a level of security appropriate to the risk, including encryption of personal data at rest in RDS databases.",
        get_dummy_embedding()
    )
    print("✅ PostgreSQL Seeding Complete!")
    
    neo4j_client.close()
    pgvector_client.close()

if __name__ == "__main__":
    seed_databases()
