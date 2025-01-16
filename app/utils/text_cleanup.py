import re

def clean_text_for_tts(text: str) -> str:
    """
    Clean text from special characters that might cause issues with TTS.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text safe for TTS processing
    """
    # Replace common sound effect patterns
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Remove asterisks around words
    
    # Replace multiple types of quotes with simple quotes
    text = re.sub(r'[''""„"]', '"', text)
    
    # Replace various dashes with simple space
    text = re.sub(r'[—–-]', ' ', text)
    
    # Remove other special characters
    text = re.sub(r'[*_~^(){}\[\]…]', '', text)
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip() 