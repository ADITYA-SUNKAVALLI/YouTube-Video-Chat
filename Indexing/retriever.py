import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings

load_dotenv()

# --------------------------------------------------------
# NVIDIA Embedding Model
# (Use the SAME model that was used for indexing)
# --------------------------------------------------------

embeddings = NVIDIAEmbeddings(
    model="nvidia/llama-nemotron-embed-1b-v2",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# --------------------------------------------------------
# Load Chroma Vector Database
# --------------------------------------------------------

VECTOR_DB_PATH = "chroma_db"

def load_retriever():

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k":8
        }
    )


# --------------------------------------------------------
# Retrieve Documents
# --------------------------------------------------------

def retrieve_documents(query: str):

    retriever = load_retriever()
    documents = retriever.invoke(query)

    return documents


# --------------------------------------------------------
# Re-ranking
# (Currently simple ranking based on similarity order)
# Replace with NVIDIA Re-ranker later if needed.
# --------------------------------------------------------

def rerank_documents(documents, top_n=4):

    return documents[:top_n]


# --------------------------------------------------------
# Main Retrieval Pipeline
# --------------------------------------------------------

def retrieve_context(query):

    documents = retrieve_documents(query)

    best_documents = rerank_documents(documents)

    context = "\n\n".join(
        doc.page_content
        for doc in best_documents
    )

    return {
        "status": "success",
        "query": query,
        "context": context,
        "documents": best_documents
    }


# --------------------------------------------------------
# Testing
# --------------------------------------------------------

if __name__ == "__main__":

    query = "What is Artificial Intelligence?"

    result = retrieve_context(query)

    print("\n========== RETRIEVED CONTEXT ==========\n")

    print(result["context"])