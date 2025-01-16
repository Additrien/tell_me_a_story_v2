from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import argparse
from app.core.config import settings
from app.api.routes import router
from app.services.speech_to_text import speech_to_text_service
from app.services.llm_service import LLMServiceFactory

def create_app(llm_type: str = None) -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    
    @app.get("/test")
    async def websocket_test():
        """Serve the WebSocket test page"""
        return FileResponse("app/static/websocket_test.html")
    
    @app.on_event("startup")
    async def startup_event():
        speech_to_text_service.initialize()
        # Override the default LLM service if specified
        if llm_type:
            global llm_service
            llm_service = LLMServiceFactory.create_service(llm_type)
    
    app.include_router(router, prefix=settings.API_V1_STR)
    return app

if __name__ == "__main__":
    import uvicorn
    
    parser = argparse.ArgumentParser(description='Run the Story Teller API')
    parser.add_argument('--llm', type=str, choices=['gemini', 'local', 'openrouter'], 
                       help='LLM service to use (overrides config setting)')
    args = parser.parse_args()
    
    app = create_app(args.llm)
    uvicorn.run(app, host="127.0.0.1", port=8000)

