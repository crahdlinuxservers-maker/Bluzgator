"""
Słownik Bluzgatora - baza słów i wyrażeń
Zawiera bluzgi, komplementy, cytaty i inne treści
"""

import random
from typing import List, Dict, Any
import json
import os
from config import Config

class Dictionary:
    """Klasa zarządzająca słownikiem bluzgów i komplementów"""
    
    def __init__(self):
        self.dictionary_file = os.path.join(Config.DATA_DIR, "dictionary.json")
        self.data = self._load_dictionary()
    
    def _load_dictionary(self) -> Dict[str, Any]:
        """Ładuje słownik z pliku JSON lub tworzy domyślny"""
        try:
            if os.path.exists(self.dictionary_file):
                with open(self.dictionary_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Błąd ładowania słownika: {e}")
        
        # Domyślny słownik
        return {
            "bluzgi": self._get_default_bluzgi(),
            "komplementy": self._get_default_komplementy(),
            "cytat": self._get_default_cytaty(),
            "wrozby": self._get_default_wrozby(),
            "reakcje": self._get_default_reakcje(),
            "kategorie": {
                "bluzgi": ["łagodne", "średnie", "mocne", "epickie"],
                "komplementy": ["standard", "kreatywne", "epickie"]
            }
        }
    
    def save(self):
        """Zapisuje słownik do pliku"""
        try:
            Config.ensure_data_dir()
            with open(self.dictionary_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Błąd zapisywania słownika: {e}")
    
    # === GENERATORY BŁUZGÓW ===
    
    def generuj_bluzga(self, intensity: int = 50, target_name: str = "") -> str:
        """Generuje bluzga o określonej intensywności"""
        if intensity < 30:
            bluzgi = self.data["bluzgi"]["łagodne"]
        elif intensity < 60:
            bluzgi = self.data["bluzgi"]["średnie"]
        elif intensity < 85:
            bluzgi = self.data["bluzgi"]["mocne"]
        else:
            bluzgi = self.data["bluzgi"]["epickie"]
        
        bluzg = random.choice(bluzgi)
        if target_name:
            bluzg = bluzg.replace("{target}", target_name)
        return bluzg
    
    def generuj_komplement(self, intensity: int = 50, target_name: str = "") -> str:
        """Generuje komplement o określonej intensywności"""
        if intensity < 40:
            komplementy = self.data["komplementy"]["standard"]
        elif intensity < 75:
            komplementy = self.data["komplementy"]["kreatywne"]
        else:
            komplementy = self.data["komplementy"]["epickie"]
        
        komplement = random.choice(komplementy)
        if target_name:
            komplement = komplement.replace("{target}", target_name)
        return komplement
    
    def generuj_cytat(self) -> str:
        """Generuje losowy cytat"""
        return random.choice(self.data["cytat"])
    
    def generuj_wrozbe(self) -> str:
        """Generuje losową wróżbę"""
        return random.choice(self.data["wrozby"])
    
    def generuj_reakcje(self, count: int = 1) -> List[str]:
        """Generuje losowe reakcje (emojis)"""
        return random.sample(self.data["reakcje"], min(count, len(self.data["reakcje"])))
    
    # === DODAWANIE NOWYCH TREŚCI ===
    
    def dodaj_bluzga(self, bluzg: str, kategoria: str = "średnie"):
        """Dodaje nowego bluzga do słownika"""
        if kategoria not in self.data["bluzgi"]:
            self.data["bluzgi"][kategoria] = []
        
        if bluzg not in self.data["bluzgi"][kategoria]:
            self.data["bluzgi"][kategoria].append(bluzg)
            self.save()
            return True
        return False
    
    def dodaj_komplement(self, komplement: str, kategoria: str = "standard"):
        """Dodaje nowy komplement do słownika"""
        if kategoria not in self.data["komplementy"]:
            self.data["komplementy"][kategoria] = []
        
        if komplement not in self.data["komplementy"][kategoria]:
            self.data["komplementy"][kategoria].append(komplement)
            self.save()
            return True
        return False
    
    # === STATYSTYKI SŁOWNIKA ===
    
    def get_stats(self) -> Dict[str, int]:
        """Zwraca statystyki słownika"""
        stats = {
            "total_bluzgi": 0,
            "total_komplementy": 0,
            "total_cytaty": len(self.data["cytat"]),
            "total_wrozby": len(self.data["wrozby"])
        }
        
        for kategoria in self.data["bluzgi"].values():
            stats["total_bluzgi"] += len(kategoria)
        
        for kategoria in self.data["komplementy"].values():
            stats["total_komplementy"] += len(kategoria)
        
        return stats
    
    # === DOMYŚLNE TREŚCI ===
    
    def _get_default_bluzgi(self) -> Dict[str, List[str]]:
        """Zwraca domyślne bluzgi"""
        return {
            "łagodne": [
                "{target}, twój intelekt jest jak twoje szanse - minimalne.",
                "{target}, gdyby głupota była paliwem, miałbyś nieskończony zapas.",
                "{target}, twoje IQ jest niższe niż temperatura pokojowa.",
                "{target}, jesteś żywym dowodem, że ewolucja może iść wstecz.",
                "{target}, twój mózg pracuje na jednym neuronie.",
                "{target}, jesteś jak GPS bez sygnału - kompletnie zagubiony.",
                "{target}, twoje pomysły są jak twoja pamięć - nieistniejące.",
                "{target}, gdybyś miał dwa mózgi, nadal byłbyś głupi.",
                "{target}, twój rozum jest jak pusty kubek.",
                "{target}, jesteś mistrzem w robieniu z niczego jeszcze mniej."
            ],
            "średnie": [
                "{target}, twój mózg to jedyne miejsce gdzie nic się nie dzieje.",
                "{target}, jesteś tak bystry, że myślisz iż USB to rodzaj autobusu.",
                "{target}, twoja inteligencja jest jak twoje szanse - żadne.",
                "{target}, gdyby głupota była sportem, byłbyś olimpijczykiem.",
                "{target}, twój umysł to czarna dziura - wsysa światło i nadzieję.",
                "{target}, jesteś żywym przykładem darwinizmu w akcji.",
                "{target}, twój rozum jest jak zepsuty zegar - nawet dwa razy na dobę nie pokazuje dobrze.",
                "{target}, gdybyś miał mózg, byłbyś samotny.",
                "{target}, twoje pomysły są jak twoje szanse - żadne.",
                "{target}, jesteś jak ślepy kierowca w nocy - kompletnie zagubiony."
            ],
            "mocne": [
                "{target}, twój mózg to jedyne miejsce gdzie nic się nie dzieje od lat.",
                "{target}, jesteś tak głupi, że myślisz iż CTRL+Z cofa czas w rzeczywistości.",
                "{target}, twoja inteligencja jest jak twoje życie - pusta i bez sensu.",
                "{target}, gdyby głupota była chorobą, byłbyś pandemią.",
                "{target}, twój umysł to czarna dziura intelektu.",
                "{target}, jesteś żywym dowodem, że Bóg ma poczucie humoru.",
                "{target}, twój rozum jest jak twoja przyszłość - nieistniejący.",
                "{target}, gdybyś miał IQ, byłbyś niebezpieczny.",
                "{target}, twoje pomysły są jak twoje marzenia - nierealne.",
                "{target}, jesteś jak GPS w tunelu - kompletnie bezużyteczny."
            ],
            "epickie": [
                "{target}, twój mózg to jedyne miejsce gdzie cisza jest głośniejsza niż myśli.",
                "{target}, jesteś tak głupi, że myślisz iż HTML to choroba weneryczna.",
                "{target}, twoja inteligencja jest jak twoja osobowość - nieistniejąca.",
                "{target}, gdyby głupota była sztuką, byłbyś Picassem.",
                "{target}, twój umysł to czarna dziura, która wsysa nawet nadzieję.",
                "{target}, jesteś żywym dowodem, że ewolucja czasem się myli.",
                "{target}, twój rozum jest jak twoje życie - puste i bezcelowe.",
                "{target}, gdybyś miał mózg, byłbyś zagrożeniem dla siebie.",
                "{target}, twoje pomysły są jak twoja przyszłość - nie istnieją.",
                "{target}, jesteś jak ślepy w labiryncie - bez szans na wyjście."
            ]
        }
    
    def _get_default_komplementy(self) -> Dict[str, List[str]]:
        """Zwraca domyślne komplementy"""
        return {
            "standard": [
                "{target}, jesteś niesamowitą osobą!",
                "{target}, twój uśmiech rozjaśnia dzień!",
                "{target}, masz wspaniałą energię!",
                "{target}, jesteś bardzo inteligentny!",
                "{target}, twoja obecność uszczęśliwia innych!",
                "{target}, masz wielkie serce!",
                "{target}, jesteś inspiracją dla wielu!",
                "{target}, twój optymizm jest zaraźliwy!",
                "{target}, masz niezwykły talent!",
                "{target}, jesteś prawdziwym przyjacielem!"
            ],
            "kreatywne": [
                "{target}, twój umysł jest jak gwiazdy - pełen światła i inspiracji!",
                "{target}, jesteś jak świeży powiew wiatru - orzeźwiający i potrzebny!",
                "{target}, twoja dusza ma kolor tęczy - pełna barw i piękna!",
                "{target}, jesteś jak dobry film - wciągający i niezapomniany!",
                "{target}, twój uśmiech to jak słońce w pochmurny dzień!",
                "{target}, jesteś jak dobra książka - pełen mądrości i ciepła!",
                "{target}, twoje serce bije rytmem przyjaźni!",
                "{target}, jesteś jak latarnia morska - prowadzisz innych do bezpieczeństwa!",
                "{target}, twój duch jest jak ogień - pełen pasji i energii!",
                "{target}, jesteś jak klejnot - rzadki i cenny!"
            ],
            "epickie": [
                "{target}, twój umysł to galaktyka pełna niesamowitych pomysłów!",
                "{target}, jesteś jak supernowa - eksplodujesz pozytywną energią!",
                "{target}, twoja dusza ma moc zmieniania świata na lepsze!",
                "{target}, jesteś żywym dowodem, że dobro istnieje!",
                "{target}, twój uśmiech ma moc leczenia złamanego serca!",
                "{target}, jesteś jak feniks - zawsze powstajesz z popiołów!",
                "{target}, twoje serce jest jak ocean - głębokie i pełne tajemnic!",
                "{target}, jesteś jak półbóg - masz nadludzką siłę ducha!",
                "{target}, twój charakter jest jak diament - niezniszczalny i piękny!",
                "{target}, jesteś jak legenda - o tobie będą opowiadać przez wieki!"
            ]
        }
    
    def _get_default_cytaty(self) -> List[str]:
        """Zwraca domyślne cytaty"""
        return [
            "Głupota ma tę zaletę, że nigdy nie nudzi.",
            "Inteligencja to umiejętność ukrywania swojej głupoty.",
            "Największym błędem jest wierzyć, że się nie popełnia błędów.",
            "Mądry człowiek uczy się na cudzych błędach, głupi na swoich.",
            "Głupota jest jedyną rzeczą, która nie ma granic.",
            "Najtrudniej jest udawać głupiego, kiedy się nim nie jest.",
            "Głupota jest jak dobry humor - zaraźliwa.",
            "Inteligencja to zdolność do adaptacji do zmian.",
            "Największa mądrość to przyznać się do niewiedzy.",
            "Głupi się śmieje, mądry się uczy."
        ]
    
    def _get_default_wrozby(self) -> List[str]:
        """Zwraca domyślne wróżby"""
        return [
            "Dziś spotkasz kogoś mądrzejszego od siebie. Będzie to miłe doświadczenie.",
            "Twoje szczęście jest jak Twój intelekt – imponujące!",
            "Gwiazdy radzą: podążaj za swoimi marzeniami.",
            "Dziś unikaj luster. Twoje piękno może oślepić!",
            "Twój mózg dziś wejdzie w tryb geniuszu!",
            "Dziś odkryjesz nowy talent. Będzie to zaskoczenie!",
            "Twoja przyszłość jest jasna jak twoje myśli.",
            "Dziś spotkasz swojego anioła stróża. Będzie to miłe spotkanie.",
            "Twoje marzenia się spełnią. Będzie to niespodzianka!",
            "Dziś odkryjesz nową pasję. Będzie to ekscytujące!"
        ]
    
    def _get_default_reakcje(self) -> List[str]:
        """Zwraca domyślne reakcje (emojis)"""
        return [
            "😊", "😂", "🤣", "😎", "🤔", "😏", "😒", "🙄", "😴", "🥴",
            "😵", "🤯", "🤬", "😡", "🤮", "🤢", "😈", "👿", "💀", "☠️",
            "🤖", "👾", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿",
            "😾", "👋", "🤚", "🖐️", "✋", "🖖", "👌", "🤏", "✌️", "🤞",
            "🤟", "🤘", "🤙", "👈", "👉", "👆", "🖕", "👇", "☝️", "👍",
            "👎", "✊", "👊", "🤛", "🤜", "👏", "🙌", "👐", "🤲", "🤝",
            "🙏", "✍️", "💅", "🤳", "💪", "🦾", "🦵", "🦿", "🦶", "👂",
            "🦻", "👃", "🧠", "🦷", "🦴", "👀", "👁️", "👅", "👄", "💋",
            "🩸", "💘", "💝", "💖", "💗", "💓", "💞", "💕", "💟", "❣️",
            "💔", "❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍",
            "💯", "💢", "💥", "💫", "💦", "💨", "🕳️", "💣", "💬", "👁️‍🗨️",
            "🗨️", "🗯️", "💭", "💤", "👋", "🤚", "🖐️", "✋", "🖖", "👌"
        ]