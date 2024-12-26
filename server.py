from query import summarize_text, get_thumbnail_from_url, get_transcript_from_url, summarize_transcript
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def render_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"summary": "", "transcript": ""}
    )

@app.post("/")
async def render_page_summary(request: Request, youtube_url: Annotated[str, Form()], language: Annotated[str, Form()], transcript: Annotated[bool, Form()]):
    youtube_transcript = get_transcript_from_url(youtube_url)
    summary = summarize_transcript(youtube_transcript, lang=language)
    if transcript:
        return templates.TemplateResponse(
            request=request, 
            name="index.html",
            context={"summary": summary, "transcript": youtube_transcript}
        )
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"summary": summary, "transcript": ""}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")