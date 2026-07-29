from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound
)
from urllib.parse import urlparse, parse_qs


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
        # Create API object
        ytt_api = YouTubeTranscriptApi()


        # Get available transcripts
        transcript_list = ytt_api.list(video_id)


        # Try English first
        try:
            transcript = transcript_list.find_transcript(["en"])

        except NoTranscriptFound:
            # Take first available language
            transcript = next(iter(transcript_list))


        # Fetch transcript
        transcript_data = transcript.fetch()


        # Convert to text
        text = " ".join(
            snippet.text for snippet in transcript_data
        )


        return {
            "status": "success",
            "video_id": video_id,
            "language": transcript.language,
            "language_code": transcript.language_code,
            "transcript": text
        }


    except TranscriptsDisabled:
        return {
            "status": "failed",
            "message": "No transcript available. Captions disabled."
        }


    except NoTranscriptFound:
        return {
            "status": "failed",
            "message": "No transcript found."
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