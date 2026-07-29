import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# ---------------------------------------------------------
# NVIDIA Embedding Model
# ---------------------------------------------------------

embeddings = NVIDIAEmbeddings(
    model="nvidia/llama-nemotron-embed-1b-v2",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# ---------------------------------------------------------
# Recursive Character Text Splitter
# ---------------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# ---------------------------------------------------------
# Chroma Database Path
# ---------------------------------------------------------

VECTOR_DB_PATH = "chroma_db"


def create_vector_store(translation_result: dict):
    """
    Receives translated transcript and creates a fresh vector database.
    """

    if translation_result["status"] != "success":
        return translation_result

    text = translation_result["text"]
    print("\n==============================")
    print("TEXT RECEIVED FROM TRANSLATOR")
    print("==============================")
    print(text[:1000])
    print("==============================\n")

    # -------------------------------------------------
    # Step 1 : Chunking
    # -------------------------------------------------

    chunks = text_splitter.split_text(text)

    documents = [
        Document(
            page_content=chunk,
            metadata={"chunk_id": i}
        )
        for i, chunk in enumerate(chunks)
    ]
    print("\n==============================")
    print("FIRST CHUNK")
    print("==============================")
    print(documents[0].page_content[:1000])
    print("==============================\n")

    print(f"Created {len(documents)} chunks.")
    print("\n========== FIRST CHUNK ==========\n")
    print(documents[0].page_content[:1500])
    print("\n=================================\n")

    # -------------------------------------------------
    # Step 2 : Open/Create Chroma
    # -------------------------------------------------

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    # -------------------------------------------------
    # Step 3 : Delete previous documents
    # -------------------------------------------------

    try:
        ids = vectorstore.get()["ids"]

        if ids:
            vectorstore.delete(ids=ids)

    except Exception:
        pass

    # -------------------------------------------------
    # Step 4 : Add new documents
    # -------------------------------------------------

    vectorstore.add_documents(documents)

    # -------------------------------------------------
    # Step 5 : Release object
    # -------------------------------------------------

    del vectorstore

    return {
        "status": "success",
        "chunks": len(documents)
    }


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    sample = {
        "status": "success",
        "translated": False,
        "text": """
Artificial Intelligence (AI) is transforming the world.

Machine Learning is a subset of AI.

Deep Learning is a subset of Machine Learning.

Large Language Models are trained on huge amounts of text.
""" * 50
    }

    result = create_vector_store(sample)

    print(result)