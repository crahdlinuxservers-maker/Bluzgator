"""
Konfiguracja Bluzgatora v5.0 Armagedon
Plik konfiguracyjny z ustawieniami bota
"""

import os
from typing import Dict, Any
import json

class Config:
    """Klasa zarządzająca konfiguracją bota"""
    
    # Podstawowe ustawienia
    BOT_NAME = "Bluzgator v5.0 Armagedon"
    BOT_VERSION = "5.0.0"
    BOT_PREFIX = "!"
    BOT_STATUS = "Bluzganie na maksa"
    
    # Właściciel bota
    OWNER_NAME = "Crahd"  # Twój nick na Discordzie
    OWNER_ID = None  # ID właściciela (automatycznie wykrywane)
    
    # Ścieżki do plików
    DATA_DIR = "data"
    CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
    DATABASE_FILE = os.path.join(DATA_DIR, "database.json")
    LOG_FILE = os.path.join(DATA_DIR, "bluzgator.log")
    BLACKLIST_FILE = os.path.join(DATA_DIR, "blacklist.json")
    
    # Ustawienia Discord
    INTENTS = {
        "message_content": True,
        "members": True,
        "guilds": True,
        "reactions": True
    }
    
    # Limity i ustawienia
    MAX_MESSAGES_PER_USER = 1000
    COOLDOWN_SECONDS = 2
    MAX_PURGE_MESSAGES = 100
    AUTO_SAVE_INTERVAL = 300  # sekundy
    
    # Kolory embedów
    EMBED_COLORS = {
        "info": 0x3498db,      # Niebieski
        "success": 0x2ecc71,   # Zielony
        "warning": 0xf39c12,   # Pomarańczowy
        "error": 0xe74c3c,     # Czerwony
        "bluzg": 0x9b59b6,     # Fioletowy
        "admin": 0x1abc9c      # Turkusowy
    }
    
    # Poziomy logowania
    LOG_LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }
    
    # Domyślny poziom logowania
    LOG_LEVEL = "INFO"
    
    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """Ładuje konfigurację z pliku JSON"""
        try:
            if os.path.exists(cls.CONFIG_FILE):
                with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Błąd ładowania konfiguracji: {e}")
            return {}
    
    @classmethod
    def save_config(cls, config_data: Dict[str, Any]) -> bool:
        """Zapisuje konfigurację do pliku JSON"""
        try:
            os.makedirs(cls.DATA_DIR, exist_ok=True)
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Błąd zapisywania konfiguracji: {e}")
            return False
    
    @classmethod
    def get_discord_intents(cls):
        """Tworzy obiekt intents Discord"""
        from discord import Intents
        intents = Intents.default()
        for intent_name, enabled in cls.INTENTS.items():
            if hasattr(intents, intent_name):
                setattr(intents, intent_name, enabled)
        return intents
    
    @classmethod
    def ensure_data_dir(cls):
        """Tworzy katalog danych jeśli nie istnieje"""
        os.makedirs(cls.DATA_DIR, exist_ok=True)