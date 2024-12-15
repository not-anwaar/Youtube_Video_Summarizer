import google.generativeai as genai
import os
from scrape import extract_video_id, download_thumbnail, get_transcript

def summarize_text(text, lang='en'):
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
        The following text is in its original language. Provide the output in this lanuage: {lang}. 
        Format the output as follows:

        Summary:
        short summary of the video

        Key Takeaways:
        succinct bullet point list of key takeaways

        input text: {text}
        """
    response = model.generate_content(prompt)
    return response.text

def get_thumbnail_from_url(url):
    video_id = extract_video_id(url)
    download_thumbnail(video_id)

def get_transcript_from_url(url):
    video_id = extract_video_id(url)
    transcript = get_transcript(video_id)
    return transcript

def summarize_transcript(transcript, lang):
    summary = summarize_text(transcript, lang=lang)
    return summary



