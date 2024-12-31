"""
Language configuration for MMS-TTS.
Auto-generated from: https://dl.fbaipublicfiles.com/mms/misc/language_coverage_mms.html
"""

from typing import Dict, List

# Full mapping of language codes to their names
LANGUAGE_CODES: Dict[str, str] = {
    "abi": "Abidji",
    "abp": "Ayta, Abellen",
    "aca": "Achagua",
    "acd": "Gikyode",
    "ace": "Aceh",
    "acf": "Lesser Antillean French Creole",
    "ach": "Acholi",
    "acn": "Achang",
    "acr": "Achi",
    "acu": "Achuar-Shiwiar",
    "ade": "Adele",
    "adj": "Adioukrou",
    "agd": "Agarabi",
    "agn": "Agutaynen",
    "agr": "Aguaruna",
    "agu": "Aguacateco",
    "agx": "Aghul",
    "ahs": "Ashe",
    "aia": "Arosi",
    "akb": "Batak Angkola",
    "alp": "Alune",
    "amh": "Amharic",
    "ara": "Arabic",
    "azb": "South Azerbaijani",
    "bba": "Baatonum",
    "bbc": "Batak Toba",
    "bcl": "Bikol Central",
    "bfa": "Bari",
    "blt": "Tai Dam",
    "bqc": "Boko",
    "bqp": "Busa",
    "bru": "Eastern Bru",
    "bss": "Akoose",
    "bul": "Bulgarian",
    "byr": "Baruya",
    "cce": "Chopi",
    "ces": "Czech",
    "deu": "German",
    "eng": "English",
    "fin": "Finnish",
    "fra": "French",
    "heb": "Hebrew",
    "hin": "Hindi",
    "hun": "Hungarian",
    "ind": "Indonesian",
    "ita": "Italian",
    "jpn": "Japanese",
    "kor": "Korean",
    "nld": "Dutch",
    "pol": "Polish",
    "por": "Portuguese",
    "ron": "Romanian",
    "rus": "Russian",
    "spa": "Spanish",
    "swe": "Swedish",
    "tha": "Thai",
    "tur": "Turkish",
    "ukr": "Ukrainian",
    "vie": "Vietnamese",
    "zho": "Chinese"
}

# Common languages with their codes (subset of most used languages)
COMMON_LANGUAGES: Dict[str, str] = {
    "french": "fra",
    "english": "eng",
    "spanish": "spa",
    "german": "deu",
    "italian": "ita",
    "portuguese": "por",
    "polish": "pol",
    "turkish": "tur",
    "russian": "rus",
    "dutch": "nld",
    "czech": "ces",
    "arabic": "ara",
    "chinese": "zho",
    "japanese": "jpn",
    "korean": "kor",
    "vietnamese": "vie",
    "thai": "tha",
    "hebrew": "heb",
    "hindi": "hin",
    "indonesian": "ind",
    "romanian": "ron",
    "bulgarian": "bul",
    "ukrainian": "ukr",
    "swedish": "swe",
    "finnish": "fin",
    "hungarian": "hun"
}

def get_language_name(code: str) -> str:
    """Get the full language name from its ISO code."""
    return LANGUAGE_CODES.get(code, code)

def get_language_code(name: str) -> str:
    """Get the ISO code from a language name."""
    # Try common languages first (case insensitive)
    name_lower = name.lower()
    if name_lower in COMMON_LANGUAGES:
        return COMMON_LANGUAGES[name_lower]
    
    # Try to find in full mapping (case sensitive)
    for code, lang_name in LANGUAGE_CODES.items():
        if lang_name == name:
            return code
    
    raise ValueError(f"Language '{name}' not found in supported languages") 