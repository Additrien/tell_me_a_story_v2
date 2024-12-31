from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ConversationTurn:
    user_input: str
    llm_response: str
    timestamp: datetime
    language: str

class ConversationManager:
    def __init__(self):
        self.history: List[ConversationTurn] = []
        
    def add_turn(self, user_input: str, llm_response: str, language: str) -> None:
        turn = ConversationTurn(
            user_input=user_input,
            llm_response=llm_response,
            timestamp=datetime.now(),
            language=language
        )
        self.history.append(turn)
        
    def get_formatted_history(self, max_turns: int = 3) -> str:
        """Formats the last conversation turns for LLM context"""
        if not self.history:
            return ""
            
        recent_history = self.history[-max_turns:]
        formatted = "\nPREVIOUS CONVERSATION CONTEXT:\n"
        
        for turn in recent_history:
            formatted += f"Child: {turn.user_input}\n"
            formatted += f"Story: {turn.llm_response}\n"
            
        return formatted
    
    def clear_history(self) -> None:
        """Clears the conversation history"""
        self.history = []

conversation_manager = ConversationManager() 