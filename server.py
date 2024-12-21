from query import summarize_text, get_thumbnail_from_url, get_transcript_from_url, summarize_transcript
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def render_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"summary": ""}
    )

@app.post("/")
async def render_page_summary(request: Request, youtube_url: Annotated[str, Form()], language: Annotated[str, Form()]):
    transcript = get_transcript_from_url(youtube_url)
    summary = summarize_transcript(transcript, lang=language)
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"summary": summary}
    )