from .llm import llm
from .cross_encoder import retrieve_and_rerank
def rag(query):
    retrieved_documents = retrieve_and_rerank(query)

    context = "\n\n".join(retrieved_documents)

    prompt = f"""
You are a knowledgeable and precise Q&A assistant.

Your task is to answer the user's question using ONLY the information provided in the context.
If the answer is not contained in the context, say clearly:
"I don’t have enough information in the provided documents to answer this question."

Rules:
- Do not use external knowledge.
- Do not guess or assume.
- Keep answers concise and factual.

Question:
{query}

Information:
{context}
"""

    response = llm.invoke(prompt)
    return response.content
