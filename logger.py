"""
System logowania dla Bluzgatora
Zapisuje zdarzenia do pliku i konsoli
"""

import logging
import os
from datetime import datetime
from typing import Optional
from config import Config

class BluzgatorLogger:
    """Klasa zarządzająca logowaniem"""
    
    def __init__(self):
        self.log_file = Config.LOG_FILE
        self.log_level = Config.LOG_LEVELS.get(Config.LOG_LEVEL, 20)
        self._setup_logger()
    
    def _setup_logger(self):
        """Konfiguruje system logowania"""
        # Tworzymy katalog logów jeśli nie istnieje
        Config.ensure_data_dir()
        
        # Konfigurujemy logger
        self.logger = logging.getLogger('bluzgator')
        self.logger.setLevel(self.log_level)
        
        # Usuwamy istniejące handlery
        self.logger.handlers.clear()
        
        # Handler do pliku
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Handler do konsoli
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def log(self, level: str, message: str, **kwargs):
        """Loguje wiadomość na określonym poziomie"""
        level_num = Config.LOG_LEVELS.get(level.upper(), 20)
        
        # Dodajemy dodatkowe informacje do wiadomości
        if kwargs:
            extra_info = ' '.join([f'{k}={v}' for k, v in kwargs.items()])
            message = f'{message} [{extra_info}]'
        
        self.logger.log(level_num, message)
    
    def debug(self, message: str, **kwargs):
        """Loguje wiadomość debug"""
        self.log('DEBUG', message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Loguje wiadomość informacyjną"""
        self.log('INFO', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Loguje ostrzeżenie"""
        self.log('WARNING', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Loguje błąd"""
        self.log('ERROR', message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Loguje krytyczny błąd"""
        self.log('CRITICAL', message, **kwargs)
    
    def command_log(self, user_id: str, username: str, command: str, success: bool = True, **kwargs):
        """Specjalny log dla komend"""
        status = "SUCCESS" if success else "FAILED"
        self.info(f"COMMAND: {command} by {username} ({user_id}) - {status}", **kwargs)
    
    def bluzg_log(self, sender_id: str, sender_name: str, target_id: str, target_name: str, bluzg: str, intensity: int):
        """Loguje użycie bluzga"""
        self.info(
            f"BLUZG: {sender_name} -> {target_name}",
            sender_id=sender_id,
            target_id=target_id,
            intensity=intensity,
            bluzg_length=len(bluzg)
        )
    
    def komplement_log(self, sender_id: str, sender_name: str, target_id: str, target_name: str, komplement: str, intensity: int):
        """Loguje użycie komplementu"""
        self.info(
            f"KOMPLEMENT: {sender_name} -> {target_name}",
            sender_id=sender_id,
            target_id=target_id,
            intensity=intensity,
            komplement_length=len(komplement)
        )
    
    def get_log_tail(self, lines: int = 50) -> Optional[str]:
        """Zwraca ostatnie linie logu"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    return ''.join(all_lines[-lines:])
        except Exception as e:
            self.error(f"Błąd odczytu logu: {e}")
        return None
    
    def clear_logs(self, days_to_keep: int = 7) -> bool:
        """Czyści stare logi (archiwizuje)"""
        try:
            if not os.path.exists(self.log_file):
                return True
            
            # Sprawdzamy datę modyfikacji pliku
            file_time = os.path.getmtime(self.log_file)
            file_date = datetime.fromtimestamp(file_time)
            now = datetime.now()
            
            # Jeśli plik jest starszy niż days_to_keep dni
            if (now - file_date).days > days_to_keep:
                # Tworzymy nazwę archiwalną
                archive_name = f"{self.log_file}.{file_date.strftime('%Y%m%d')}.bak"
                
                # Przenosimy stary plik
                os.rename(self.log_file, archive_name)
                
                # Tworzymy nowy pusty plik logu
                open(self.log_file, 'w').close()
                
                self.info(f"Zarchiwizowano stare logi do: {archive_name}")
                return True
                
        except Exception as e:
            self.error(f"Błąd czyszczenia logów: {e}")
        
        return False
    
    def get_log_stats(self) -> Dict[str, Any]:
        """Zwraca statystyki logów"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                stats = {
                    "total_lines": len(lines),
                    "file_size_kb": os.path.getsize(self.log_file) / 1024,
                    "last_modified": datetime.fromtimestamp(os.path.getmtime(self.log_file)).isoformat(),
                    "levels_count": {}
                }
                
                # Liczymy linie per poziom
                for line in lines:
                    for level in Config.LOG_LEVELS.keys():
                        if f' {level} ' in line or f' {level}:' in line:
                            stats["levels_count"][level] = stats["levels_count"].get(level, 0) + 1
                            break
                
                return stats
                
        except Exception as e:
            self.error(f"Błąd pobierania statystyk logów: {e}")
        
        return {"error": "Nie udało się pobrać statystyk"}