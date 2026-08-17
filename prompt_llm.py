import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# ---------------------------------------------------------
# NVIDIA LLM
# ---------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

# ---------------------------------------------------------
# Prompt Template
# ---------------------------------------------------------

PROMPT = """
You are an intelligent AI assistant that answers questions about YouTube videos.

The following text is retrieved from the video's transcript.

Your responsibility is to answer the user's question ONLY using the retrieved transcript.

Rules:

1. Use ONLY the retrieved transcript below.
2. Never use your own knowledge.
3. Never assume missing information.
4. Never hallucinate.
5. If the answer is not present in the retrieved transcript, reply exactly:

"I couldn't find the answer in the retrieved transcript."

6. If the retrieved transcript only partially answers the question,
state that the available transcript provides only partial information.

7. If timestamps are available inside the retrieved context,
include the relevant timestamps in your answer.

8. Keep the answer concise, accurate, and easy to understand.

Previous Conversation

{history}

------------------ Retrieved Transcript ------------------

{context}

----------------------------------------------------------

User Question:

{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(PROMPT)

# ---------------------------------------------------------
# Generate Answer
# ---------------------------------------------------------

def generate_answer(
    question,
    context,
    history=""):
    """
    Generates the final answer using the retrieved transcript.
    """

    chain = prompt | llm

    response = chain.invoke(
    {
        "question": question,
        "context": context,
        "history": history
    }
)

    return {
        "status": "success",
        "question": question,
        "answer": response.content
    }


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_question = "Why does he like Shanghai?"

    sample_context = """
                        [00:18]

                        He says Shanghai is his favorite city because he grew up there and
                        his friends are also there.

                        [00:42]

                        He also mentions that he lived in the United States for seven years.
                    """

    result = generate_answer(
        sample_question,
        sample_context
    )

    print("\n========== ANSWER ==========\n")
    print(result["answer"])