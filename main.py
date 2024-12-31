from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.api.routes import router
from app.services.speech_to_text import speech_to_text_service

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/test")
async def websocket_test():
    """Serve the WebSocket test page"""
    return FileResponse("app/static/websocket_test.html")

@app.on_event("startup")
async def startup_event():
    # Initialize Whisper model at startup
    speech_to_text_service.initialize()

app.include_router(router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

