import streamlit as st

from Indexing.transcript_extractor import get_transcript_from_video
from Indexing.translate import translate_transcript
from Indexing.chunk_embed_store import create_vector_store
from Indexing.retriever import retrieve_context

from prompt_llm import generate_answer


# -------------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="YouTube Video Chat",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------------
# Custom CSS Styling
# -------------------------------------------------------

st.markdown(
    """
    <style>
        /* Overall app background */
        .stApp {
            background: linear-gradient(180deg, #0f1116 0%, #14171f 100%);
        }

        /* Main content width */
        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Hero header */
        .hero-title {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ff4b4b, #ff8a8a);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .hero-subtitle {
            color: #a0a4ad;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }

        /* Section labels */
        .section-label {
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #ff6b6b;
            margin-bottom: 0.5rem;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            width: 100%;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(255, 75, 75, 0.35);
        }

        /* Text inputs */
        .stTextInput > div > div > input {
            background-color: #12141c;
            border: 1px solid #2a2e3d;
            border-radius: 10px;
            color: #f0f0f0;
            padding: 0.7rem;
        }

        /* Chat bubbles */
        .chat-bubble-user {
            background: #262a3a;
            border-radius: 14px 14px 4px 14px;
            padding: 0.8rem 1rem;
            margin: 0.4rem 0;
            color: #e6e6e6;
            max-width: 85%;
            margin-left: auto;
        }
        .chat-bubble-assistant {
            background: #1f2937;
            border-left: 3px solid #ff6b6b;
            border-radius: 4px 14px 14px 14px;
            padding: 0.8rem 1rem;
            margin: 0.4rem 0;
            color: #e6e6e6;
            max-width: 85%;
        }
        .chat-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #8a8f9c;
            margin-bottom: 0.15rem;
        }

        /* Status pill */
        .status-pill {
            display: inline-block;
            background: #16351f;
            color: #6bff8f;
            border: 1px solid #245c33;
            border-radius: 999px;
            padding: 0.25rem 0.9rem;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }

        /* Divider tweak */
        hr {
            border-color: #2a2e3d !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: #ff8a8a;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Session State
# -------------------------------------------------------

if "current_url" not in st.session_state:
    st.session_state.current_url = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "video_processed" not in st.session_state:
    st.session_state.video_processed = False

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.markdown('<div class="hero-title">🎥 YouTube Video Chat</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Ask questions about any YouTube video using '
    'Retrieval-Augmented Generation (RAG).</div>',
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Video URL
# -------------------------------------------------------

st.markdown('<div class="section-label">📌 Video Source</div>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])

with col1:
    video_url = st.text_input(
        "Enter YouTube Video URL",
        label_visibility="collapsed",
        placeholder="https://www.youtube.com/watch?v=...",
    )

with col2:
    process = st.button("🚀 Process Video")

if st.session_state.video_processed and st.session_state.current_url:
    st.markdown(
        '<span class="status-pill">✅ Video ready — ask away below</span>',
        unsafe_allow_html=True,
    )

# -------------------------------------------------------
# Process Video
# -------------------------------------------------------

if process:

    if video_url.strip() == "":
        st.warning("Please enter a YouTube URL.")

    else:

        # ------------------------------------------------
        # Process only if the URL is different
        # ------------------------------------------------

        if video_url != st.session_state.current_url:

            st.session_state.current_url = video_url

            # Clear previous conversation
            st.session_state.chat_history = []

            # New video
            st.session_state.video_processed = False

            progress = st.progress(0, text="Starting...")

            # Step 1
            with st.spinner("🎧 Extracting transcript..."):

                transcript = get_transcript_from_video(video_url)
                progress.progress(33, text="Transcript extracted")

            if transcript["status"] != "success":
                st.error(transcript["message"])
                st.stop()

            # Step 2
            with st.spinner("🌐 Translating transcript..."):

                translated = translate_transcript(transcript)
                progress.progress(66, text="Translation complete")

            if translated["status"] != "success":
                st.error(translated["message"])
                st.stop()

            # Step 3
            with st.spinner("🧠 Creating vector database..."):

                result = create_vector_store(translated)
                progress.progress(100, text="Vector store ready")

            if result["status"] != "success":
                st.error("Failed to create vector database.")
                st.stop()

            st.session_state.video_processed = True

            st.success("✅ Video processed successfully! Scroll down to start chatting.")

        else:

            st.info("ℹ️ This video is already processed.")

# -------------------------------------------------------
# Ask Questions
# -------------------------------------------------------

if st.session_state.video_processed:

    st.markdown('<div class="section-label">💬 Ask a Question</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])

    with col1:
        question = st.text_input(
            "Your Question",
            label_visibility="collapsed",
            placeholder="What is this video about?",
        )

    with col2:
        ask = st.button("✨ Get Answer")

    if ask:

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:

            # --------------------------------------------
            # Retrieve Context
            # --------------------------------------------

            with st.spinner("🔍 Retrieving relevant information..."):

                retrieval = retrieve_context(question)

            # --------------------------------------------
            # Build Previous Conversation
            # --------------------------------------------

            history = ""

            for chat in st.session_state.chat_history:

                history += f"""
User:
{chat['question']}

Assistant:
{chat['answer']}

"""

            # --------------------------------------------
            # Generate Answer
            # --------------------------------------------

            with st.spinner("🤖 Generating answer..."):

                response = generate_answer(
                    question=question,
                    context=retrieval["context"],
                    history=history
                )

            # --------------------------------------------
            # Save Conversation
            # --------------------------------------------

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": response["answer"]
                }
            )

            # --------------------------------------------
            # Show Retrieved Context
            # --------------------------------------------

            with st.expander("📄 Retrieved Context"):

                st.write(retrieval["context"])

    # ------------------------------------------------
    # Conversation History (styled chat bubbles)
    # ------------------------------------------------

    if st.session_state.chat_history:

        st.divider()
        st.markdown('<div class="section-label">🗨️ Conversation</div>', unsafe_allow_html=True)

        for chat in reversed(st.session_state.chat_history):

            st.markdown(
                f'''
                <div class="chat-label">You asked</div>
                <div class="chat-bubble-user">{chat["question"]}</div>
                <div class="chat-label">Assistant</div>
                <div class="chat-bubble-assistant">{chat["answer"]}</div>
                ''',
                unsafe_allow_html=True,
            )