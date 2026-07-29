import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

# ---------------------------------------------------
# Initialize NVIDIA Translation Model
# ---------------------------------------------------
translation_model = ChatNVIDIA(
    model="nvidia/nemotron-3-super-120b-a12b",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=0
)


def load_translation_model():
    """
    Returns the initialized translation model.
    """
    return translation_model


def translate_transcript(transcript_result: dict):
    """
    Translate transcript to English if it is not already in English.
    """

    # If transcript extraction failed
    if transcript_result["status"] != "success":
        return transcript_result

    language_code = transcript_result["language_code"]
    transcript = transcript_result["transcript"]

    # ------------------------------------------
    # English -> No translation needed
    # ------------------------------------------
    if language_code.lower() == "en":
        return {
            "status": "success",
            "translated": False,
            "language": "English",
            "language_code": "en",
            "text": transcript
        }

    # ------------------------------------------
    # Translate to English
    # ------------------------------------------
    model = load_translation_model()

    prompt = f"""
You are an expert translator.

Translate the following transcript into fluent English.

Rules:
- Preserve the original meaning.
- Do not summarize.
- Do not add explanations.
- Return ONLY the translated text.

Transcript:
{transcript}
"""

    try:
        response = model.invoke(prompt)

        translated_text = response.content


        return {
            "status": "success",
            "translated": True,
            "original_language": transcript_result["language"],
            "language": "English",
            "language_code": "en",
            "text": translated_text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":

    sample = {
        "status": "success",
        "video_id": "abc123",
        "language": "Chinese",
        "language_code": "zh",
        "transcript": """
                        哦没有，我是出差在这边，工作出差在这边。
                        你有多高？
                        一米八五。
                        好高啊！
                        你最喜欢的城市是哪个？
                        呃，上海。
                        为什么？
                        因为我在那边长大，我的朋友也在那边。
                        """
    }

    result = translate_transcript(sample)

    print("\n========== RESULT ==========\n")

    if result["status"] == "success":
        print(result["text"])
    else:
        print(result["message"])                        