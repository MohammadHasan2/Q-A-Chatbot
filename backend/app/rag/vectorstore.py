from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def load_chroma(pdf_path, collection_name="LuminaCloudSystem"):
    reader = PdfReader(pdf_path)
    pdf_texts = [p.extract_text().strip() for p in reader.pages]
    pdf_texts = [text for text in pdf_texts if text]

    # Character and token splitting
    char_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=1000,
        chunk_overlap=0)
    char_texts = char_splitter.split_text('\n\n'.join(pdf_texts))

    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
    token_texts = []
    for text in char_texts:
        token_texts += token_splitter.split_text(text)

    embedding_function = SentenceTransformerEmbeddingFunction()

    client = chromadb.Client()
    
    try:
        collection = client.get_collection(collection_name)
    except:
        collection = client.create_collection(collection_name, embedding_function=embedding_function)

    # Add documents if collection empty
    if collection.count() == 0:
        ids = [str(i) for i in range(len(token_texts))]
        collection.add(ids=ids, documents=token_texts)

    return collection

def query_chroma(collection, query, n_results=4):
    results = collection.query(query_texts=[query], n_results=n_results)
    return results['documents'][0]
