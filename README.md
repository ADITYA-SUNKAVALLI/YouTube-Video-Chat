# 🎥 YouTube Video Chat — RAG-Based Question Answering System

A Retrieval-Augmented Generation (RAG) application that lets you chat with any YouTube video using natural language. Paste a URL, ask questions, and get answers grounded in the video's actual transcript.

## Overview

YouTube Video Chat provides a **Streamlit** interface where users enter a YouTube video URL. The system:

1. Extracts the video ID from the URL
2. Fetches the available transcript
3. Translates it to English via the **NVIDIA API** if it isn't already in English
4. Splits the transcript into chunks and embeds them into **ChromaDB**
5. Answers user questions by retrieving and re-ranking the most relevant chunks, then generating a response with an LLM

If no transcript is available for a video, the app detects this and informs the user directly rather than failing silently.

## Key Workflow

```
User enters YouTube URL
        │
        ▼
  Extract Video ID
        │
        ▼
 Fetch YouTube Transcript
        │
        ▼
  Language Detection
        │
   ┌────┴────┐
   │         │
English   Other Language
   │         │
   │         ▼
   │  NVIDIA Translation API
   │         │
   └────┬────┘
        ▼
 Recursive Text Splitting
        │
        ▼
  Generate Embeddings
        │
        ▼
Store in ChromaDB Vector DB
        │
        ▼
     User Query
        │
        ▼
Query Embedding + Similarity Search
        │
        ▼
Re-rank Top Relevant Chunks
        │
        ▼
   Prompt Generation
        │
        ▼
     LLM Response
        │
        ▼
Display Answer in Streamlit
```

## Features

- 🔗 **Simple URL input** — just paste a YouTube link to get started
- 🌍 **Multilingual support** — automatic translation of non-English transcripts via the NVIDIA API
- ✂️ **Smart chunking** — recursive text splitting preserves context across chunk boundaries
- 🔍 **Semantic search** — vector similarity search over transcript embeddings using ChromaDB
- 🎯 **Re-ranking** — narrows retrieval down to the top 4 most relevant chunks for higher answer quality
- 🤖 **LLM-powered answers** — context-aware responses generated from retrieved transcript chunks
- ⚠️ **Graceful fallback** — clearly notifies the user when a transcript isn't available

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| Orchestration | LangChain |
| Translation | NVIDIA API |
| Vector Store | ChromaDB |
| Embeddings | Embedding Models (via LangChain) |
| Generation | Large Language Models (LLM) |
| Approach | Retrieval-Augmented Generation (RAG), NLP |

## Getting Started

### Prerequisites

- Python 3.9+
- An NVIDIA API key (for translation)
- An API key for your chosen LLM/embedding provider

### Installation

```bash
# Clone the repository
git clone https://github.com/ADITYA-SUNKAVALLI/youtube-video-chat.git
cd youtube-video-chat

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root with your API credentials:

```env
NVIDIA_API_KEY=your_nvidia_api_key
```

### Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (typically `http://localhost:8501`).

## Usage

1. Launch the app and paste a YouTube video URL into the input field
2. Wait while the transcript is fetched, translated (if needed), and indexed
3. Type a question about the video in the chat box
4. Review the generated answer, grounded in the video's content

## Project Structure

```
youtube-video-chat/
├── app.py                 # Streamlit entry point
├── src/
│   ├── transcript.py       # Video ID extraction + transcript fetching
│   ├── translation.py      # NVIDIA API translation logic
│   ├── chunking.py         # Recursive text splitting
│   ├── embeddings.py       # Embedding generation
│   ├── vectorstore.py      # ChromaDB storage and retrieval
│   ├── reranker.py         # Re-ranking retrieved chunks
│   └── rag_pipeline.py     # Prompt construction + LLM invocation
├── requirements.txt
├── .env.example
└── README.md
```

## Objective

The goal of this project is to build an intelligent YouTube assistant that can understand video content and answer user questions accurately, using retrieval-augmented generation to ground responses in the actual transcript rather than relying on the LLM's general knowledge alone.

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.

