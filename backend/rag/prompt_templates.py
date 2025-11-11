# Prompt templates for the Kant knowledge system

QA_PROMPT = """You are a Kantian philosophy assistant. Please answer the user's question based on the provided evidence, following these requirements:
1) Provide a concise conclusion first
2) List the evidence sources (work_id/para_id/lang)
3) Avoid making inferences beyond the provided evidence

User question: {question}

Candidate evidence:
{evidence_blocks}

Answer:"""

SUMMARY_PROMPT = """Create a summary of the key points from the following evidence about Kantian philosophy:
{evidence_blocks}

Summary:"""

CONCEPT_DEFINITION_PROMPT = """Provide a precise definition of the concept mentioned in the user's question based on the provided evidence.
User question: {question}

Relevant evidence:
{evidence_blocks}

Definition and explanation:"""

# Additional prompt for multi-language queries
MULTI_LANGUAGE_QA_PROMPT = """You are a Kantian philosophy expert. Answer the user's question in {response_lang} based on the provided evidence.
Question: {question}

Relevant evidence:
{evidence_blocks}

Requirements:
1. Answer in {response_lang}
2. Cite evidence sources (work_id/para_id/lang)
3. Stay within bounds of provided evidence

Answer:"""