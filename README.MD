# 🤖 Bluzgator v5.0 Armagedon

**Zaawansowany bot rozrywkowy na Discord**  
*System z bazą JSON, logami, statystykami i super funkcjami*

---

## 📋 Spis Treści
- [📖 O Projekcie](#-o-projekcie)
- [✨ Funkcje](#-funkcje)
- [⚙️ Wymagania](#️-wymagania)
- [🚀 Instalacja](#-instalacja)
- [🔧 Konfiguracja](#-konfiguracja)
- [🎮 Komendy](#-komendy)
- [📊 Struktura Projektu](#-struktura-projektu)
- [🐛 Rozwiązywanie Problemów](#-rozwiązywanie-problemów)
- [🤝 Współpraca](#-współpraca)
- [📄 Licencja](#-licencja)

---

## 📖 O Projekcie

**Bluzgator v5.0 Armagedon** to zaawansowany bot Discord stworzony przez **Stanisława Kozioła**. Bot łączy w sobie funkcje rozrywkowe (bluzgi, komplementy) z profesjonalnym systemem zarządzania (baza danych, logi, statystyki).

### 👨‍💻 Autor
- **Imię i nazwisko:** Stanisław Kozioł
- **Email:** crahdlinuxservers@gmail.com
- **GitHub:** https://github.com/crahdlinuxservers-maker/
- **Discord:** Crahd

### 🎯 Cel Projektu
Stworzenie zaawansowanego bota Discord z:
- Systemem bazy danych JSON
- Kompleksowym logowaniem
- Statystykami i rankingami
- Trybami specjalnymi (snajper, auto-bluzg)
- Interfejsem administratorskim

---

## ✨ Funkcje

### 🎯 Podstawowe
- **Bluzgi** - Losowe bluzgi o różnej intensywności
- **Komplementy** - Pochwały i komplementy
- **Cytaty** - Losowe mądre cytaty
- **Wróżby** - Wróżby na dziś

### 📊 Statystyki
- **Statystyki użytkowników** - Aktywność, bluzgi, komplementy
- **Rankingi** - Top 10 bluzgaczy i ofiar
- **Statystyki globalne** - Podsumowanie całego bota
- **Statystyki słownika** - Ilość treści w bazie

### ⚙️ System
- **Baza danych JSON** - Auto-save co 5 minut
- **System logowania** - Logi do pliku i konsoli
- **Cooldowny** - Zabezpieczenie przed spamem
- **Blacklista** - Blokowanie użytkowników

### 👑 Funkcje Właściciela
- **Tryb snajpera** - Automatyczne bluzganie celu
- **Auto-bluzg mode** - Losowe bluzganie użytkowników
- **Czyszczenie wiadomości** - Usuwanie wiadomości z kanału
- **Zarządzanie blacklistą** - Blokowanie/odblokowywanie
- **Podgląd logów** - Przeglądanie systemowych logów

### 🎨 Interfejs
- **Piękne embedy** - Kolorowe wiadomości z ikonkami
- **Reakcje** - Automatyczne dodawanie emoji
- **Menu pomocy** - Kompletna lista komend
- **Status bota** - Dynamiczny status w Discord

---

## ⚙️ Wymagania

### 📦 Wymagania systemowe
- Python 3.8 lub nowszy
- Discord Developer Account
- Bot token z Discord Developer Portal

### 📚 Biblioteki Python
Wszystkie wymagane biblioteki znajdują się w `requirements.txt`:
```
discord.py>=2.3.0
```

---

## 🚀 Instalacja

### Krok 1: Pobranie projektu
```bash
# Klonowanie repozytorium
git clone https://github.com/crahdlinuxservers-maker/bluzgator.git
cd bluzgator

# Lub pobranie jako ZIP i rozpakowanie
```

### Krok 2: Instalacja zależności
```bash
# Instalacja discord.py
pip install discord.py

# Lub użycie requirements.txt
pip install -r requirements.txt
```

### Krok 3: Konfiguracja bota
1. Otwórz plik `config.py`
2. Znajdź linię: `DISCORD_TOKEN = "TUTAJ_WPISZ_SWOJ_TOKEN"`
3. Zamień na swój token Discord

### Krok 4: Uruchomienie
```bash
python main.py
```

### Krok 5: Dodanie bota na serwer
1. Wejdź na: https://discord.com/developers/applications
2. Wybierz swoją aplikację
3. Przejdź do "OAuth2" → "URL Generator"
4. Zaznacz: `bot` i `applications.commands`
5. Skopiuj wygenerowany link
6. Otwórz link w przeglądarce i dodaj bota na serwer

---

## 🔧 Konfiguracja

### Plik config.py
```python
# Podstawowa konfiguracja
BOT_NAME = "Bluzgator"
BOT_VERSION = "5.0"
OWNER_NAME = "Crahd"  # Twój nick na Discord
BOT_PREFIX = "!"      # Prefix komend

# Token Discord (WAŻNE!)
DISCORD_TOKEN = "TWÓJ_TOKEN_TUTAJ"

# Kolory embedów
EMBED_COLORS = {
    "info": 0x3498db,      # Niebieski
    "success": 0x2ecc71,   # Zielony
    "warning": 0xf39c12,   # Pomarańczowy
    "error": 0xe74c3c,     # Czerwony
    "admin": 0x9b59b6      # Fioletowy
}
```

### Dostosowanie ustawień
Możesz zmienić:
- `BOT_STATUS` - Status wyświetlany w Discord
- `COOLDOWN_SECONDS` - Czas cooldownu między komendami
- `LOG_LEVEL` - Poziom logowania (DEBUG, INFO, WARNING, ERROR)
- `DATA_DIR` - Katalog na dane i logi

---

## 🎮 Komendy

### 🎯 Bluzgi i Komplementy
```
!bluzg [@użytkownik]      - Wyślij bluzga
!komplement [@użytkownik] - Wyślij komplement
!intensywnosc <1-100>     - Ustaw intensywność
!cytat                    - Losowy cytat
!wrozba [@użytkownik]     - Wróżba na dziś
```

### 📊 Statystyki i Rankingi
```
!statystyki [@użytkownik] - Statystyki użytkownika
!ranking                  - Top 10 bluzgów
!ofiary                   - Top 10 ofiar
!globalne                 - Statystyki globalne
!avatar [@użytkownik]     - Avatar z komentarzem
```

### ⚙️ System i Narzędzia
```
!ping                     - Sprawdź ping bota
!info                     - Informacje o bocie
!logi [ilość]            - Pokaż logi (tylko właściciel)
!słownik                  - Statystyki słownika
!dodaj <typ> <treść>     - Dodaj do słownika (tylko właściciel)
```

### 👑 Panel Właściciela
```
!snajper [@użytkownik]   - Tryb snajpera
!autobluzg               - Auto-bluzg mode
!czysc [ilość]           - Czyść wiadomości
!blacklist [@użytkownik] - Zarządzaj blacklistą
!poklon                  - Hołd dla Pana
!zapisz                  - Wymuś zapis bazy
!restart                 - Restart bota
```

### ℹ️ Pomoc
```
!help                    - Główne menu pomocy
!pomoc                   - To samo co !help
!komendy                 - Lista wszystkich komend
```

---

## 📊 Struktura Projektu

```
bluzgator/
├── 📁 data/                    # Katalog na dane (tworzony automatycznie)
│   ├── 📄 database.json       # Baza danych użytkowników
│   ├── 📄 dictionary.json     # Słownik bluzgów i komplementów
│   └── 📄 bluzgator.log       # Plik logów
├── 📄 main.py                 # Główny plik bota
├── 📄 config.py               # Konfiguracja bota
├── 📄 database.py             # System bazy danych JSON
├── 📄 dictionary.py           # Słownik bluzgów i komplementów
├── 📄 logger.py               # System logowania
├── 📄 requirements.txt        # Wymagane biblioteki
├── 📄 README.md               # Ten plik
└── 📄 .gitignore              # Ignorowane pliki Git
```

### Opis plików:
1. **main.py** - Główny plik bota, obsługa komend i eventów
2. **config.py** - Konfiguracja bota, token, ustawienia
3. **database.py** - System bazy danych z auto-save
4. **dictionary.py** - Słownik z bluzgami i komplementami
5. **logger.py** - System logowania do pliku i konsoli
6. **requirements.txt** - Lista wymaganych bibliotek

---

## 🐛 Rozwiązywanie Problemów

### ❌ Błąd: "Nieprawidłowy token Discord"
**Rozwiązanie:**
1. Sprawdź czy token w `config.py` jest poprawny
2. Upewnij się że bot ma wymagane uprawnienia
3. Sprawdź czy bot jest dodany na serwerze

### ❌ Błąd: "Missing Permissions"
**Rozwiązanie:**
1. Sprawdź uprawnienia bota na serwerze
2. Upewnij się że bot ma rolę z odpowiednimi uprawnieniami
3. Sprawdź czy kanał nie jest zablokowany dla botów

### ❌ Błąd: "Command not found"
**Rozwiązanie:**
1. Sprawdź prefix komend w `config.py`
2. Upewnij się że używasz poprawnego prefixu
3. Sprawdź czy komenda istnieje w `!help`

### ❌ Błąd: "Cannot send messages"
**Rozwiązanie:**
1. Sprawdź uprawnienia bota na kanale
2. Upewnij się że bot może czytać i pisać na kanale
3. Sprawdź czy kanał nie jest NSFW (jeśli bot nie ma uprawnień)

### 🔧 Debugowanie
```bash
# Uruchom bota z debugowaniem
python -m pdb main.py

# Sprawdź logi
tail -f data/bluzgator.log

# Sprawdź błąd składni
python -m py_compile main.py
```

---

## 🤝 Współpraca

### 📝 Jak zgłosić błąd?
1. Sprawdź czy problem nie jest już zgłoszony
2. Stwórz nowe issue na GitHub
3. Opisz problem szczegółowo:
   - Co się stało?
   - Co powinno się stać?
   - Jak odtworzyć błąd?
   - Zrzuty ekranu/logi

### 💡 Jak zaproponować funkcję?
1. Sprawdź czy funkcja nie jest już w planach
2. Stwórz issue z propozycją
3. Opisz:
   - Jaka to funkcja?
   - Dlaczego jest potrzebna?
   - Jak powinna działać?

### 🔧 Jak współtworzyć?
1. Forkuj repozytorium
2. Stwórz branch dla swojej funkcji
3. Zrób commit zmian
4. Stwórz Pull Request
5. Opisz co zmieniłeś i dlaczego

### 📋 Zasady współpracy
- Pisz czytelny, czysty kod
- Dokumentuj nowe funkcje
- Testuj zmiany przed PR
- Szanuj innych współtwórców

---

## 📄 Licencja

### 📝 Informacje o licencji
Projekt jest dostępny na licencji MIT. Oznacza to że możesz:
- Używać projektu komercyjnie
- Modyfikować kod
- Dystrybuować kopie
- Używać projektu prywatnie

### 📄 Pełna treść licencji MIT
```
MIT License

Copyright (c) 2024 Stanisław Kozioł

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 👨‍💻 Autorzy
- **Stanisław Kozioł** - Główny developer
- **Współtwórcy** - Lista osób które przyczyniły się do projektu

### 📧 Kontakt
- **Email:** crahdlinuxservers@gmail.com
- **GitHub:** https://github.com/crahdlinuxservers-maker/
- **Discord:** Crahd

---

## 🎉 Podziękowania

Dziękuję wszystkim którzy:
- Testowali bota i zgłaszali błędy
- Proponowali nowe funkcje
- Wspierali rozwój projektu
- Używali bota i się nim bawili

### 🌟 Specjalne podziękowania dla:
- Społeczności Discord
- Wszystkich testerów
- Osoby które inspirowały do stworzenia bota

---

## 🔮 Plany na przyszłość

### 🚀 Nadchodzące funkcje
- [ ] System poziomów i doświadczenia
- [ ] Ekonomia (wirtualna waluta)
- [ ] Minigry i zabawy
- [ ] Integracja z API zewnętrznymi
- [ ] Panel webowy do zarządzania
- [ ] Więcej języków (angielski, niemiecki)
- [ ] System sklepów i przedmiotów

### 📅 Roadmap
1. **v5.1** - Poprawki błędów i optymalizacja
2. **v5.5** - Nowe komendy i funkcje
3. **v6.0** - System poziomów i ekonomia
4. **v6.5** - Minigry i zabawy
5. **v7.0** - Panel webowy

### 💡 Pomysły
- System klanów/gildii
- Eventy sezonowe
- Integracja z Twitch/YouTube
- Customowe komendy
- System osiągnięć

---

## 📊 Statystyki projektu

### 📈 Aktualne statystyki
- **Wersja:** 5.0 Armagedon
- **Komendy:** 20+
- **Funkcje:** 50+
- **Linie kodu:** 2000+
- **Testy:** W trakcie rozwoju

### 🏆 Osiągnięcia
- ✅ Pełny system bazy danych
- ✅ Kompleksowe logowanie
- ✅ System statystyk i rankingów
- ✅ Panel administratorski
- ✅ Auto-save danych

### 🎯 Cele
- [x] Stworzenie stabilnej bazy
- [x] Implementacja wszystkich podstawowych funkcji
- [x] System logowania i debugowania
- [ ] 100% pokrycie testami
- [ ] Dokumentacja API

---

**⭐ Jeśli podoba Ci się projekt, zostaw gwiazdkę na GitHub!**  
**🐛 Zgłaszaj błędy i propozycje funkcji!**  
**🤝 Dołącz do rozwoju projektu!**

---
*Ostatnia aktualizacja: Kwiecień 2026*  
*Wersja dokumentacji: 1.0*