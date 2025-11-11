import pandas as pd
from neo4j import GraphDatabase
import logging
from typing import Dict, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Neo4jLoader:
    def __init__(self):
        # Get Neo4j connection details from environment variables
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        """Close the Neo4j driver connection"""
        self.driver.close()
    
    def create_indexes_and_constraints(self):
        """Create indexes and constraints in Neo4j"""
        with self.driver.session() as session:
            # Create indexes
            session.run("CREATE INDEX person_id IF NOT EXISTS FOR (p:Person) ON (p.id)")
            session.run("CREATE INDEX work_id IF NOT EXISTS FOR (w:Work) ON (w.id)")
            session.run("CREATE INDEX concept_id IF NOT EXISTS FOR (c:Concept) ON (c.id)")
            session.run("CREATE INDEX term_id IF NOT EXISTS FOR (t:Term) ON (t.id)")
            session.run("CREATE INDEX place_id IF NOT EXISTS FOR (p:Place) ON (p.id)")
            session.run("CREATE INDEX event_id IF NOT EXISTS FOR (e:Event) ON (e.id)")
            session.run("CREATE INDEX school_id IF NOT EXISTS FOR (s:School) ON (s.id)")

            # Create constraints
            session.run("CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE")
            session.run("CREATE CONSTRAINT work_id_unique IF NOT EXISTS FOR (w:Work) REQUIRE w.id IS UNIQUE")
            session.run("CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE")
            session.run("CREATE CONSTRAINT term_id_unique IF NOT EXISTS FOR (t:Term) REQUIRE t.id IS UNIQUE")
    
    def load_persons(self, csv_path: str):
        """Load persons from CSV into Neo4j"""
        df = pd.read_csv(csv_path)
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (p:Person {id: $id})
                    SET p.name_en = $name_en,
                        p.name_zh = $name_zh,
                        p.name_de = $name_de,
                        p.birth_year = $birth_year,
                        p.death_year = $death_year,
                        p.notes = $notes
                    """,
                    id=row['id'],
                    name_en=row.get('name_en'),
                    name_zh=row.get('name_zh'),
                    name_de=row.get('name_de'),
                    birth_year=row.get('birth_year'),
                    death_year=row.get('death_year'),
                    notes=row.get('notes')
                )
    
    def load_works(self, csv_path: str):
        """Load works from CSV into Neo4j"""
        df = pd.read_csv(csv_path)
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (w:Work {id: $id})
                    SET w.title_en = $title_en,
                        w.title_zh = $title_zh, 
                        w.title_de = $title_de,
                        w.year = $year,
                        w.notes = $notes
                    """,
                    id=row['id'],
                    title_en=row.get('title_en'),
                    title_zh=row.get('title_zh'),
                    title_de=row.get('title_de'),
                    year=row.get('year'),
                    notes=row.get('notes')
                )
    
    def load_concepts(self, csv_path: str):
        """Load concepts from CSV into Neo4j"""
        df = pd.read_csv(csv_path)
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (c:Concept {id: $id})
                    SET c.label = $label,
                        c.alias_en = $alias_en,
                        c.alias_zh = $alias_zh,
                        c.alias_de = $alias_de,
                        c.notes = $notes
                    """,
                    id=row['id'],
                    label=row.get('label'),
                    alias_en=row.get('alias_en'),
                    alias_zh=row.get('alias_zh'),
                    alias_de=row.get('alias_de'),
                    notes=row.get('notes')
                )
    
    def load_relations(self, csv_path: str):
        """Load relationships from CSV into Neo4j"""
        df = pd.read_csv(csv_path)
        
        with self.driver.session() as session:
            for _, row in df.iterrows():
                # Determine relationship type and create appropriate relationship
                rel_type = row['rel_type']
                source_id = row['source_id']
                target_id = row['target_id']
                
                # We'll need to determine the source and target labels from their IDs
                # For simplicity, we'll assume prefixes determine the type:
                # p_ for Person, w_ for Work, c_ for Concept, t_ for Term
                source_label = self._get_label_from_id(source_id)
                target_label = self._get_label_from_id(target_id)
                
                session.run(
                    f"""
                    MATCH (source:{source_label} {{id: $source_id}})
                    MATCH (target:{target_label} {{id: $target_id}})
                    MERGE (source)-[:{rel_type}]->(target)
                    """,
                    source_id=source_id,
                    target_id=target_id
                )
    
    def _get_label_from_id(self, entity_id: str) -> str:
        """Determine label from ID prefix"""
        if entity_id.startswith('p_') or entity_id in ['kant', 'hume', 'leibniz', 'wolff']:
            return 'Person'
        elif entity_id.startswith('w_') or entity_id in ['pure_reason', 'practical_reason', 'judgment']:
            return 'Work'
        elif entity_id.startswith('c_') or entity_id in ['categorical_imperative', 'noumenon', 'phenomenon', 'transcendental', 'aesthetic']:
            return 'Concept'
        elif entity_id.startswith('t_'):
            return 'Term'
        else:
            # Default to Concept if uncertain
            return 'Concept'
    
    def run_sample_queries(self):
        """Run sample queries to verify data loading"""
        with self.driver.session() as session:
            # Query 1: Find who Kant influenced
            result1 = session.run(
                """
                MATCH (kant:Person {id: 'kant'})-[r:INFLUENCED_BY]-(influenced)
                RETURN influenced.name_en as influenced_name, r.type as relationship
                """
            )
            print("Kant influenced:")
            for record in result1:
                print(f"- {record['influenced_name']} ({record['relationship']})")
            
            # Query 2: Find works by Kant
            result2 = session.run(
                """
                MATCH (kant:Person {id: 'kant'})-[r:AUTHORED]->(work:Work)
                RETURN work.title_en as work_title
                """
            )
            print("\nWorks by Kant:")
            for record in result2:
                print(f"- {record['work_title']}")
            
            # Query 3: Find concepts defined by Kant
            result3 = session.run(
                """
                MATCH (kant:Person {id: 'kant'})-[r:DEFINES]->(concept:Concept)
                RETURN concept.label as concept_label
                """
            )
            print("\nConcepts defined by Kant:")
            for record in result3:
                print(f"- {record['concept_label']}")


def load_all_data():
    """Load all data from resource/kant directory"""
    loader = Neo4jLoader()
    
    try:
        # Create indexes and constraints first
        loader.create_indexes_and_constraints()
        
        # Load all data files
        loader.load_persons("resource/kant/persons.csv")
        loader.load_works("resource/kant/works.csv")
        loader.load_concepts("resource/kant/concepts.csv")
        loader.load_relations("resource/kant/relations.csv")
        
        # Run sample queries to verify
        print("Data loaded successfully. Running sample queries:")
        loader.run_sample_queries()
        
    finally:
        loader.close()


if __name__ == "__main__":
    load_all_data()