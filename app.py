from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.api.system_routes import router as system_router
from backend.api.chat_routes import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    
    title="NAVSOFT Enterprise AI Assistant",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="templates")

# Static folder (future use)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/health")
async def health():
    return {
        "status": "running",
        "application": "NAVSOFT Enterprise AI Assistant"
    }

app.include_router(system_router)
app.include_router(chat_router)