from sentence_transformers import CrossEncoder
from .vectorstore import query_chroma, load_chroma
import os

def get_collection():
    pdf_path = os.path.join(os.path.dirname(__file__), "../data/LuminaCloudSystems.pdf")
    pdf_path = os.path.abspath(pdf_path)
    
    if not os.path.exists(pdf_path):
        print(f"WARNING: PDF not found at {pdf_path}")
        return None
    
    return load_chroma(pdf_path)


def retrieve_and_rerank(query, collection_name=None, top_k=4, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
    if collection_name is None:
        collection_name = get_collection()
        if collection_name is None:
            print("No collection loaded, returning empty list.")
            return []

    retrieved_documents = query_chroma(collection_name, query)

    if not retrieved_documents:
        return []

    cross_encoder = CrossEncoder(model_name)

    pairs = [[query, doc] for doc in retrieved_documents]

    scores = cross_encoder.predict(pairs)

    doc_scores_sorted = sorted(zip(retrieved_documents, scores), key=lambda x: x[1], reverse=True)
    reranked_documents = [doc for doc, score in doc_scores_sorted]

    return reranked_documents[:2]


