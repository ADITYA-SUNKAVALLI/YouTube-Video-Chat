from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = NVIDIAEmbeddings(
    model="nvidia/llama-nemotron-embed-1b-v2",
    api_key=os.getenv("NVIDIA_API_KEY")
)

print(embeddings.embed_query("Hello world"))