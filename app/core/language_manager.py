from app.core.languages import DEFAULT_LANGUAGE

class LanguageManager:
    def __init__(self):
        self._current_language = DEFAULT_LANGUAGE
        
    @property
    def current_language(self) -> str:
        return self._current_language
        
    def set_language(self, language: str):
        self._current_language = language
        
    def get_language(self) -> str:
        return self._current_language

# Global instance
language_manager = LanguageManager() 