"""
System bazy danych JSON dla Bluzgatora
Przechowuje dane użytkowników, statystyki, rankingi itp.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio
from config import Config

class JSONDatabase:
    """Klasa zarządzająca bazą danych JSON"""
    
    def __init__(self):
        self.data_file = Config.DATABASE_FILE
        self.data = self._load_data()
        self._save_task = None
        
    def _load_data(self) -> Dict[str, Any]:
        """Ładuje dane z pliku JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Błąd ładowania bazy danych: {e}")
        
        # Domyślna struktura bazy danych
        return {
            "users": {},           # Dane użytkowników
            "guilds": {},          # Dane serwerów
            "stats": {             # Statystyki globalne
                "total_bluzgi": 0,
                "total_komplementy": 0,
                "total_commands": 0,
                "start_time": datetime.now().isoformat()
            },
            "blacklist": [],       # Zablokowani użytkownicy
            "cooldowns": {},       # Cooldowny użytkowników
            "settings": {          # Ustawienia globalne
                "auto_bluzg": False,
                "bluzg_intensity": 50
            }
        }
    
    def save(self) -> bool:
        """Zapisuje dane do pliku JSON"""
        try:
            Config.ensure_data_dir()
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Błąd zapisywania bazy danych: {e}")
            return False
    
    async def auto_save(self):
        """Automatycznie zapisuje bazę danych co określony interwał"""
        while True:
            await asyncio.sleep(Config.AUTO_SAVE_INTERVAL)
            self.save()
            print(f"[AUTO-SAVE] Baza danych zapisana: {datetime.now()}")
    
    # === METODY DLA UŻYTKOWNIKÓW ===
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Pobiera dane użytkownika"""
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = self._create_user_template()
        return self.data["users"][user_id]
    
    def update_user(self, user_id: str, data: Dict[str, Any]):
        """Aktualizuje dane użytkownika"""
        user_data = self.get_user(user_id)
        user_data.update(data)
        self.data["users"][user_id] = user_data
        self.save()
    
    def add_bluzg(self, user_id: str, target_id: str, bluzg_type: str = "normal"):
        """Dodaje bluzga do statystyk użytkownika"""
        user = self.get_user(user_id)
        target = self.get_user(target_id)
        
        # Statystyki nadawcy
        user["stats"]["bluzgi_sent"] = user["stats"].get("bluzgi_sent", 0) + 1
        user["stats"]["total_activity"] = user["stats"].get("total_activity", 0) + 1
        
        # Statystyki odbiorcy
        target["stats"]["bluzgi_received"] = target["stats"].get("bluzgi_received", 0) + 1
        
        # Statystyki globalne
        self.data["stats"]["total_bluzgi"] = self.data["stats"].get("total_bluzgi", 0) + 1
        
        # Zapisz typ bluzga
        if "bluzgi_by_type" not in user["stats"]:
            user["stats"]["bluzgi_by_type"] = {}
        user["stats"]["bluzgi_by_type"][bluzg_type] = user["stats"]["bluzgi_by_type"].get(bluzg_type, 0) + 1
        
        self.save()
    
    def add_komplement(self, user_id: str, target_id: str):
        """Dodaje komplement do statystyk"""
        user = self.get_user(user_id)
        target = self.get_user(target_id)
        
        user["stats"]["komplementy_sent"] = user["stats"].get("komplementy_sent", 0) + 1
        target["stats"]["komplementy_received"] = target["stats"].get("komplementy_received", 0) + 1
        self.data["stats"]["total_komplementy"] = self.data["stats"].get("total_komplementy", 0) + 1
        
        self.save()
    
    # === RANKINGI ===
    
    def get_top_bluzgi(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Zwraca ranking użytkowników z najwięcej bluzgami"""
        users_with_bluzgi = []
        for user_id, user_data in self.data["users"].items():
            bluzgi_sent = user_data["stats"].get("bluzgi_sent", 0)
            if bluzgi_sent > 0:
                users_with_bluzgi.append({
                    "user_id": user_id,
                    "username": user_data.get("username", "Unknown"),
                    "bluzgi_sent": bluzgi_sent,
                    "bluzgi_received": user_data["stats"].get("bluzgi_received", 0)
                })
        
        users_with_bluzgi.sort(key=lambda x: x["bluzgi_sent"], reverse=True)
        return users_with_bluzgi[:limit]
    
    def get_top_victims(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Zwraca ranking ofiar (najwięcej otrzymanych bluzgów)"""
        victims = []
        for user_id, user_data in self.data["users"].items():
            bluzgi_received = user_data["stats"].get("bluzgi_received", 0)
            if bluzgi_received > 0:
                victims.append({
                    "user_id": user_id,
                    "username": user_data.get("username", "Unknown"),
                    "bluzgi_received": bluzgi_received,
                    "bluzgi_sent": user_data["stats"].get("bluzgi_sent", 0)
                })
        
        victims.sort(key=lambda x: x["bluzgi_received"], reverse=True)
        return victims[:limit]
    
    # === BLACKLIST ===
    
    def add_to_blacklist(self, user_id: str, reason: str = ""):
        """Dodaje użytkownika do blacklisty"""
        if user_id not in self.data["blacklist"]:
            self.data["blacklist"].append({
                "user_id": user_id,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            })
            self.save()
    
    def remove_from_blacklist(self, user_id: str) -> bool:
        """Usuwa użytkownika z blacklisty"""
        for i, entry in enumerate(self.data["blacklist"]):
            if entry["user_id"] == user_id:
                self.data["blacklist"].pop(i)
                self.save()
                return True
        return False
    
    def is_blacklisted(self, user_id: str) -> bool:
        """Sprawdza czy użytkownik jest na blackliście"""
        return any(entry["user_id"] == user_id for entry in self.data["blacklist"])
    
    # === COOLDOWN SYSTEM ===
    
    def set_cooldown(self, user_id: str, command: str, seconds: int):
        """Ustawia cooldown dla komendy"""
        cooldown_key = f"{user_id}_{command}"
        expire_time = datetime.now() + timedelta(seconds=seconds)
        self.data["cooldowns"][cooldown_key] = expire_time.isoformat()
        self.save()
    
    def check_cooldown(self, user_id: str, command: str) -> Optional[int]:
        """Sprawdza czy cooldown jest aktywny, zwraca pozostałe sekundy"""
        cooldown_key = f"{user_id}_{command}"
        if cooldown_key in self.data["cooldowns"]:
            expire_time = datetime.fromisoformat(self.data["cooldowns"][cooldown_key])
            if datetime.now() < expire_time:
                remaining = (expire_time - datetime.now()).seconds
                return remaining
            else:
                del self.data["cooldowns"][cooldown_key]
                self.save()
        return None
    
    # === POMOCNICZE ===
    
    def _create_user_template(self) -> Dict[str, Any]:
        """Tworzy szablon danych użytkownika"""
        return {
            "username": "",
            "joined_at": datetime.now().isoformat(),
            "stats": {
                "bluzgi_sent": 0,
                "bluzgi_received": 0,
                "komplementy_sent": 0,
                "komplementy_received": 0,
                "total_activity": 0,
                "commands_used": 0,
                "last_active": datetime.now().isoformat()
            },
            "settings": {
                "auto_translate": False,
                "bluzg_preference": "balanced"
            },
            "achievements": []
        }
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Zwraca globalne statystyki"""
        return self.data["stats"]
    
    def increment_command_count(self):
        """Zwiększa licznik użytych komend"""
        self.data["stats"]["total_commands"] = self.data["stats"].get("total_commands", 0) + 1
        self.save()