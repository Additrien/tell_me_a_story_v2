from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import argparse
from app.core.config import settings
from app.api.routes import router
from app.api.websockets import story_ws
from app.services.speech_to_text import speech_to_text_service
from app.services.llm.base import LLMServiceFactory
from app.services.llm.global_service import llm_service
from app.services.tts.tts_factory import TTSFactory
import os

def create_app(llm_type: str = None, tts_type: str = None) -> FastAPI:
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
            from app.services.llm.global_service import llm_service as global_llm_service
            global_llm_service = LLMServiceFactory.create_service(llm_type)
            print(f"LLM service initialized in startup event: {type(global_llm_service).__name__}")
        
        # Override the default TTS service if specified
        if tts_type:
            from app.services.tts.tts_factory import TTSFactory
            TTSFactory.reset()  # Reset any existing instances
            print(f"TTS service set to: {tts_type}")
    
    app.include_router(router, prefix=settings.API_V1_STR)
    return app

if __name__ == "__main__":
    import uvicorn
    import sys
    
    parser = argparse.ArgumentParser(description='Run the Story Teller API')
    parser.add_argument('--llm', type=str, choices=['gemini', 'local', 'openrouter'], 
                       help='LLM service to use (overrides config setting)')
    parser.add_argument('--tts', type=str, choices=['fal', 'fallback'],
                       help='TTS service to use (overrides config setting)')
    parser.add_argument('--deployment-type', type=str, choices=['children', 'adults'],
                       default='children',
                       help='Type of deployment (children or adults content)')
    args = parser.parse_args()
    
    # Set deployment type before creating the app
    os.environ['DEPLOYMENT_TYPE'] = args.deployment_type
    
    # Create the LLM service after setting environment variables
    from app.services.llm.global_service import llm_service as global_llm_service
    
    # Initialize the global LLM service
    llm_type = args.llm if args.llm else settings.LLM_SERVICE
    print(f"Initializing LLM service: {llm_type}")
    
    # Import the module directly to modify the global variable
    import app.services.llm.global_service
    app.services.llm.global_service.llm_service = LLMServiceFactory.create_service(llm_type)
    
    # Verify the service was initialized
    if app.services.llm.global_service.llm_service:
        print(f"LLM service initialized successfully: {type(app.services.llm.global_service.llm_service).__name__}")
    else:
        print("ERROR: Failed to initialize LLM service")
        sys.exit(1)
    
    # Set TTS service if specified
    if args.tts:
        print(f"Setting TTS service to: {args.tts}")
        os.environ['TTS_SERVICE'] = args.tts
    
    app = create_app(args.llm, args.tts)
    uvicorn.run(app, host="127.0.0.1", port=8000)

