import os
import requests
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")
SUPADATA_URL = "https://api.supadata.ai/v1/youtube/transcript"


def extract_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]

    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    return None


def get_transcript_from_video(url):

    video_id = extract_video_id(url)

    if not video_id:
        return {
            "status": "error",
            "message": "Invalid YouTube URL"
        }

    try:
        resp = requests.get(
            SUPADATA_URL,
            params={"videoId": video_id},
            headers={"x-api-key": SUPADATA_API_KEY},
            timeout=20,
        )

        # No captions / no transcript available for this video
        if resp.status_code == 404:
            return {
                "status": "failed",
                "message": "No transcript found."
            }

        resp.raise_for_status()
        data = resp.json()

        # Combine all segments into a single text block
        segments = data.get("content", [])
        text = " ".join(seg["text"] for seg in segments)

        if not text.strip():
            return {
                "status": "failed",
                "message": "No transcript available. Captions disabled."
            }

        language_code = data.get("lang", "en")

        return {
            "status": "success",
            "video_id": video_id,
            "language": language_code,       # Supadata doesn't return a full language name, only the code
            "language_code": language_code,
            "transcript": text
        }

    except requests.exceptions.HTTPError as e:
        return {
            "status": "error",
            "message": f"Supadata API error: {str(e)}"
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Request failed: {str(e)}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# Test

if __name__ == "__main__":

    url = "https://www.youtube.com/watch?v=c1Pz6H6YLQQ&t=68s"

    result = get_transcript_from_video(url)

    print(result)