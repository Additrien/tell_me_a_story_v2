from fastapi import APIRouter, HTTPException, Query, Request, WebSocket, WebSocketDisconnect, Body
from app.services.audio_recorder import audio_recorder, cleanup_audio_file
from app.services.speech_to_text import speech_to_text_service, AudioInput
from app.api.websockets import story_ws
from app.services.conversation_manager import conversation_manager
from app.core.config import settings
from app.services.tts_factory import tts_factory
import soundfile as sf
import librosa
import uuid
from datetime import datetime
from app.core.languages import LANGUAGE_TO_BCP47, DEFAULT_LANGUAGE
from app.core.language_manager import language_manager
from app.models.user import User  # Import the User model
# Import the correct get_current_user from app.core.security
from app.core.security import hash_password, verify_password, create_access_token, get_current_user 
from fastapi import Depends, HTTPException, status # Add necessary imports for auth
from pydantic import BaseModel # For request body validation
from fastapi.security import OAuth2PasswordRequestForm # For login form
from datetime import timedelta # For token expiration

router = APIRouter()

# Pydantic models for request bodies
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Placeholder for database session - in a real app, this would be a dependency
async def get_db():
    # This is a placeholder. In a real application, this would yield a database session.
    # For example, using SQLAlchemy:
    # from app.db.session import SessionLocal
    # db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
    yield None # Returning None as we don't have a real DB session here

# Removed the placeholder get_current_user function from here.
# The correct one is imported from app.core.security

def validate_input_method(method: str):
    if method not in settings.ENABLED_INPUT_METHODS:
        raise HTTPException(
            status_code=400,
            detail=f"Input method '{method}' is not enabled. Enabled methods: {settings.ENABLED_INPUT_METHODS}"
        )

@router.websocket("/ws/story/{client_id}")
async def websocket_story_endpoint(websocket: WebSocket, client_id: str):
    await story_ws.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "transcription":
                await story_ws.stream_story(
                    websocket,
                    transcription=data["text"],
                    language=data.get("language", "french"),
                    client_id=client_id
                )
            elif data["type"] == "interaction_response" and story_ws.story_states.get(client_id, {}).get("awaiting_interaction"):
                # Handle user interaction response
                continue  # The _request_user_interaction method will handle this
    except WebSocketDisconnect:
        story_ws.disconnect(client_id)
    except Exception as e:
        print(f"Error in WebSocket connection: {str(e)}")
        story_ws.disconnect(client_id)

@router.get("/stories")
async def get_story_history(limit: int = Query(default=5, ge=1, le=20)):
    """Get recent story history"""
    stories = conversation_manager.get_recent_stories(limit)
    return [{
        "transcription": story.transcription,
        "story": story.story,
        "language": story.language,
        "timestamp": story.timestamp.isoformat()
    } for story in stories]

@router.post("/stories/clear")
async def clear_story_history():
    """Clear story history"""
    conversation_manager.clear_history()
    return {"message": "Story history cleared"}

@router.post("/start-recording")
async def start_recording_post(language: str = Query(default=None)):
    validate_input_method("voice")
    try:
        language = language or language_manager.current_language
        audio_recorder.start_recording(language)
        return {"status": "recording_started"}
    except Exception as e:
        print(f"Error in start_recording: {str(e)}")
        raise

@router.post("/stop-recording")
async def stop_recording_post(request: Request, language: str = Query(default="french")):
    audio_file = None
    try:
        audio_file, language = audio_recorder.stop_recording()
        
        audio_data, sample_rate = sf.read(audio_file)
        if len(audio_data) == 0:
            raise HTTPException(status_code=400, detail="Recorded audio file is empty")
            
        print(f"USER INPUT: Audio length: {len(audio_data)} samples, Sample rate: {sample_rate}")
        
        resampled_audio = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
        
        audio_input = AudioInput(
            array=resampled_audio.tolist(), 
            sampling_rate=16000,
            language=language
        )
        
        transcription = await speech_to_text_service.transcribe(audio_input)
        if not transcription or transcription.isspace():
            raise HTTPException(status_code=400, detail="Failed to transcribe audio - no text detected")
            
        print(f"TRANSCRIPTION: {transcription}")
        
        client_id = str(uuid.uuid4())
        return {
            "transcription": transcription,
            "client_id": client_id,
            "websocket_url": f"/api/v1/ws/story/{client_id}"
        }

    except Exception as e:
        print(f"Error in stop_recording: {str(e)}")
        raise
    finally:
        if audio_file:
            await cleanup_audio_file(audio_file)

@router.post("/text-input")
async def text_input(
    text: str = Body(..., embed=True),
    language: str = Query(default=None)
):
    validate_input_method("text")
    if not text or text.isspace():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
        
    language = language or language_manager.current_language
    client_id = str(uuid.uuid4())
    return {
        "transcription": text,
        "client_id": client_id,
        "websocket_url": f"/api/v1/ws/story/{client_id}"
    }

@router.get("/languages")
async def get_languages():
    """Get available languages and their codes"""
    return {
        "available_languages": list(LANGUAGE_TO_BCP47.keys()),
        "default_language": DEFAULT_LANGUAGE
    }

@router.post("/language")
async def set_language(language: str = Body(..., embed=True)):
    """Set the current language"""
    if language not in LANGUAGE_TO_BCP47:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported language. Available languages: {list(LANGUAGE_TO_BCP47.keys())}"
        )
    language_manager.set_language(language)
    return {"language": language}

@router.post("/reload-config")
async def reload_config():
    """Reload configuration and reset services"""
    settings.Config.env_file = ".env"
    tts_factory.reset()
    return {"message": "Configuration reloaded and services reset"}

@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db = Depends(get_db)):
    """
    Register a new user.
    """
    # In a real app, you would check if the user already exists in the database
    # For example:
    # existing_user = db.query(User).filter(User.email == user_in.email).first()
    # if existing_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pass = hash_password(user_in.password)
    
    # In a real app, you would create a new User model instance and save it to the database
    # For example:
    # new_user = User(email=user_in.email, hashed_password=hashed_pass)
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    
    # Placeholder response
    return {"email": user_in.email, "message": "User created successfully (placeholder)"}

@router.post("/users/login")
async def login_user(user_in: UserLogin, db = Depends(get_db)):
    """
    Login an existing user.
    """
    # In a real app, you would fetch the user from the database
    # For example:
    # user = db.query(User).filter(User.email == user_in.email).first()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    # Placeholder for fetching user and verifying password
    # For now, let's assume we fetched a user with a known hashed password
    # (This is NOT secure and only for demonstration without a DB)
    placeholder_hashed_password = hash_password("testpassword") # Simulate a stored hash

    # if not verify_password(user_in.password, user.hashed_password if user else placeholder_hashed_password):
    # In a real app, you'd use user.hashed_password from the DB
    if not verify_password(user_in.password, placeholder_hashed_password): # Simplified for placeholder
        raise HTTPException(status_code=400, detail="Incorrect password")

    # In a real app, you would fetch the user from the database.
    # user = db.query(User).filter(User.email == form_data.username).first()
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # Placeholder for fetching user and verifying password
    # This is NOT secure and only for demonstration without a DB
    placeholder_hashed_password = hash_password("testpassword") # Simulate a stored hash for form_data.username

    # if not verify_password(form_data.password, user.hashed_password if user else placeholder_hashed_password):
    # In a real app, you'd use user.hashed_password from the DB
    if not verify_password(form_data.password, placeholder_hashed_password): # Simplified for placeholder
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/stories/generate")
async def generate_story_protected(current_user: User = Depends(get_current_user)):
    """
    Protected route to generate a story.
    Requires authentication.
    """
    return {"message": f"Hello {current_user.email}, you can generate a story!"}
