// Neo4j schema for Kant knowledge graph

// Create indexes for better query performance
CREATE INDEX person_id IF NOT EXISTS FOR (p:Person) ON (p.id);
CREATE INDEX work_id IF NOT EXISTS FOR (w:Work) ON (w.id);
CREATE INDEX concept_id IF NOT EXISTS FOR (c:Concept) ON (c.id);
CREATE INDEX term_id IF NOT EXISTS FOR (t:Term) ON (t.id);
CREATE INDEX place_id IF NOT EXISTS FOR (p:Place) ON (p.id);
CREATE INDEX event_id IF NOT EXISTS FOR (e:Event) ON (e.id);
CREATE INDEX school_id IF NOT EXISTS FOR (s:School) ON (s.id);

// Create constraints to ensure uniqueness
CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT work_id_unique IF NOT EXISTS FOR (w:Work) REQUIRE w.id IS UNIQUE;
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT term_id_unique IF NOT EXISTS FOR (t:Term) REQUIRE t.id IS UNIQUE;

// Example MERGE statements for sample data
// Person nodes
MERGE (kant:Person {id: 'kant', name_en: 'Immanuel Kant', name_zh: '伊曼努尔·康德', name_de: 'Immanuel Kant', birth_year: 1724, death_year: 1804, notes: 'German philosopher'})
MERGE (hume:Person {id: 'hume', name_en: 'David Hume', name_zh: '大卫·休谟', name_de: 'David Hume', birth_year: 1711, death_year: 1776, notes: 'Scottish philosopher'})

// Work nodes
MERGE (pure_reason:Work {id: 'pure_reason', title_en: 'Critique of Pure Reason', title_zh: '纯粹理性批判', title_de: 'Kritik der reinen Vernunft', year: 1781, notes: 'Kant\'s first critique'})
MERGE (practical_reason:Work {id: 'practical_reason', title_en: 'Critique of Practical Reason', title_zh: '实践理性批判', title_de: 'Kritik der praktischen Vernunft', year: 1788, notes: 'Kant\'s second critique'})

// Concept nodes
MERGE (categorical_imperative:Concept {id: 'categorical_imperative', label: 'Categorical Imperative', alias_en: 'moral law; CI', alias_zh: '定言令式; 道德律', alias_de: 'kategorischer Imperativ', notes: 'Core ethical concept'})
MERGE (noumenon:Concept {id: 'noumenon', label: 'Noumenon', alias_en: 'thing-in-itself', alias_zh: '物自体; 本体', alias_de: 'Ding an sich', notes: 'Distinction between phenomenon and noumenon'})

// Create relationships
MERGE (kant)-[:AUTHORED]->(pure_reason)
MERGE (kant)-[:AUTHORED]->(practical_reason)
MERGE (hume)-[:INFLUENCED_BY]->(kant)
MERGE (kant)-[:DEFINES]->(categorical_imperative)
MERGE (kant)-[:DEFINES]->(noumenon)
MERGE (pure_reason)-[:DEFINES]->(noumenon)
MERGE (categorical_imperative)-[:RELATES_TO]->(practical_reason)