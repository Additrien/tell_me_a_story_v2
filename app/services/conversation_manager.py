from typing import List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class StoryTurn:
    transcription: str
    story: str
    language: str
    timestamp: datetime

class ConversationManager:
    def __init__(self):
        self.history: List[StoryTurn] = []
        
    def add_story(self, transcription: str, story: str, language: str) -> None:
        """Add a new story to the history"""
        turn = StoryTurn(
            transcription=transcription,
            story=story,
            language=language,
            timestamp=datetime.now()
        )
        self.history.append(turn)
        
    def get_recent_stories(self, limit: int = 5) -> List[StoryTurn]:
        """Get the most recent stories"""
        return sorted(self.history, key=lambda x: x.timestamp, reverse=True)[:limit]
        
    def clear_history(self) -> None:
        """Clear the story history"""
        self.history = []

conversation_manager = ConversationManager()