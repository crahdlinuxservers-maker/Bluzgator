"""
Bluzgator v5.0 Armagedon - Zaawansowany bot Discord
Zintegrowany system z bazą JSON, logami, konfiguracją i super funkcjami
"""

import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime
import os

# Import naszych modułów
from config import Config
from database import JSONDatabase
from dictionary import Dictionary
from logger import BluzgatorLogger

# Inicjalizacja systemów
config = Config
db = JSONDatabase()
dictionary = Dictionary()
logger = BluzgatorLogger()

# Bot Discord
intents = config.get_discord_intents()
bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)
bot.remove_command('help')

# Zmienne globalne
snajper_cel = None
auto_bluzg_mode = False

# === POMOCNICZE FUNKCJE ===

def is_owner(user):
    """Sprawdza czy użytkownik jest właścicielem"""
    return user.name == config.OWNER_NAME

async def check_cooldown(ctx, command_name):
    """Sprawdza cooldown dla komendy"""
    user_id = str(ctx.author.id)
    remaining = db.check_cooldown(user_id, command_name)
    
    if remaining:
        embed = discord.Embed(
            title="⏰ Cooldown Aktywny",
            description=f"Poczekaj **{remaining} sekund** przed użyciem tej komendy.",
            color=config.EMBED_COLORS["warning"]
        )
        await ctx.send(embed=embed)
        return False
    return True

async def apply_cooldown(ctx, command_name, seconds=config.COOLDOWN_SECONDS):
    """Ustawia cooldown dla komendy"""
    user_id = str(ctx.author.id)
    db.set_cooldown(user_id, command_name, seconds)

def update_user_stats(user):
    """Aktualizuje statystyki użytkownika"""
    user_id = str(user.id)
    user_data = db.get_user(user_id)
    user_data["username"] = user.name
    user_data["stats"]["last_active"] = datetime.now().isoformat()
    db.update_user(user_id, user_data)

# === EVENTY ===

@bot.event
async def on_ready():
    """Event uruchomienia bota"""
    logger.info(f"Bot {config.BOT_NAME} v{config.BOT_VERSION} - ONLINE")
    logger.info(f"Zalogowano jako: {bot.user.name}")
    logger.info(f"ID bota: {bot.user.id}")
    logger.info(f"Właściciel: {config.OWNER_NAME}")
    
    # Ustaw status bota
    await bot.change_presence(
        activity=discord.Game(name=config.BOT_STATUS),
        status=discord.Status.online
    )
    
    # Uruchom auto-save bazy danych
    asyncio.create_task(db.auto_save())
    
    # Piękne powitanie w konsoli
    print("╔══════════════════════════════════════════════════════╗")
    print("║               BLUZGATOR v5.0 ARMAGEDON              ║")
    print("║                Zaawansowany Bot Discord             ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  Bot: {bot.user.name:<43} ║")
    print(f"║  Wersja: {config.BOT_VERSION:<41} ║")
    print(f"║  Właściciel: {config.OWNER_NAME:<37} ║")
    print(f"║  Serwery: {len(bot.guilds):<41} ║")
    print("╚══════════════════════════════════════════════════════╝")

@bot.event
async def on_message(message):
    """Obsługa wiadomości"""
    if message.author == bot.user:
        return
    
    # Aktualizuj statystyki użytkownika
    update_user_stats(message.author)
    
    # Tryb snajpera
    global snajper_cel
    if snajper_cel and message.author.mention == snajper_cel:
        bluzg = dictionary.generuj_bluzga(intensity=70, target_name=message.author.name)
        await message.channel.send(f"{message.author.mention}, {bluzg}")
        db.add_bluzg(str(bot.user.id), str(message.author.id), "snajper")
        logger.bluzg_log(
            str(bot.user.id), bot.user.name,
            str(message.author.id), message.author.name,
            bluzg, 70
        )
    
    # Auto-bluzg mode
    global auto_bluzg_mode
    if auto_bluzg_mode and random.randint(1, 100) < 20:  # 20% szans
        bluzg = dictionary.generuj_bluzga(intensity=50, target_name=message.author.name)
        await message.channel.send(f"{message.author.mention}, {bluzg}")
        db.add_bluzg(str(bot.user.id), str(message.author.id), "auto")
        logger.bluzg_log(
            str(bot.user.id), bot.user.name,
            str(message.author.id), message.author.name,
            bluzg, 50
        )
    
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    """Event wywołania komendy"""
    user_id = str(ctx.author.id)
    username = ctx.author.name
    command = ctx.command.name if ctx.command else "unknown"
    
    logger.command_log(user_id, username, command)
    db.increment_command_count()
    
    # Aktualizuj statystyki użytkownika
    user_data = db.get_user(user_id)
    user_data["stats"]["commands_used"] = user_data["stats"].get("commands_used", 0) + 1
    db.update_user(user_id, user_data)

@bot.event
async def on_command_error(ctx, error):
    """Obsługa błędów komend"""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❓ Nieznana Komenda",
            description=f"Komenda `{ctx.invoked_with}` nie istnieje.\nUżyj `{config.BOT_PREFIX}help` aby zobaczyć listę komend.",
            color=config.EMBED_COLORS["error"]
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="⚠️ Brakujący Argument",
            description=f"Brakuje wymaganego argumentu: `{error.param.name}`",
            color=config.EMBED_COLORS["warning"]
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="🚫 Brak Uprawnień",
            description="Nie masz wymaganych uprawnień do użycia tej komendy.",
            color=config.EMBED_COLORS["error"]
        )
        await ctx.send(embed=embed)
    else:
        logger.error(f"Błąd komendy: {error}", command=ctx.command.name if ctx.command else "unknown")
        embed = discord.Embed(
            title="💥 Wystąpił Błąd",
            description=f"```{str(error)[:100]}...```",
            color=config.EMBED_COLORS["error"]
        )
        await ctx.send(embed=embed)

# === KOMENDY GŁÓWNE ===

@bot.command(name="help", aliases=["pomoc", "komendy"])
async def help_command(ctx):
    """Główne menu pomocy"""
    embed = discord.Embed(
        title=f"🛠️ {config.BOT_NAME} - Centrum Pomocy",
        description=f"Witaj w systemie **{config.BOT_NAME}**!\nPrefix komend: `{config.BOT_PREFIX}`",
        color=config.EMBED_COLORS["info"]
    )
    
    embed.add_field(
        name="🎯 BLUZGI I KOMPLEMENTY",
        value=(
            f"`{config.BOT_PREFIX}bluzg [@użytkownik]` - Wyślij bluzga\n"
            f"`{config.BOT_PREFIX}komplement [@użytkownik]` - Wyślij komplement\n"
            f"`{config.BOT_PREFIX}intensywnosc <1-100>` - Ustaw intensywność\n"
            f"`{config.BOT_PREFIX}cytat` - Losowy cytat\n"
            f"`{config.BOT_PREFIX}wrozba [@użytkownik]` - Wróżba na dziś"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 STATYSTYKI I RANKINGI",
        value=(
            f"`{config.BOT_PREFIX}statystyki [@użytkownik]` - Statystyki użytkownika\n"
            f"`{config.BOT_PREFIX}ranking` - Top 10 bluzgów\n"
            f"`{config.BOT_PREFIX}ofiary` - Top 10 ofiar\n"
            f"`{config.BOT_PREFIX}globalne` - Statystyki globalne\n"
            f"`{config.BOT_PREFIX}avatar [@użytkownik]` - Avatar z komentarzem"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚙️ SYSTEM I NARZĘDZIA",
        value=(
            f"`{config.BOT_PREFIX}ping` - Sprawdź ping bota\n"
            f"`{config.BOT_PREFIX}info` - Informacje o bocie\n"
            f"`{config.BOT_PREFIX}logi [ilość]` - Pokaż logi\n"
            f"`{config.BOT_PREFIX}słownik` - Statystyki słownika\n"
            f"`{config.BOT_PREFIX}dodaj <typ> <treść>` - Dodaj do słownika"
        ),
        inline=False
    )
    
    if is_owner(ctx.author):
        embed.add_field(
            name="👑 PANEL WŁAŚCICIELA",
            value=(
                f"`{config.BOT_PREFIX}snajper [@użytkownik]` - Tryb snajpera\n"
                f"`{config.BOT_PREFIX}autobluzg` - Auto-bluzg mode\n"
                f"`{config.BOT_PREFIX}czysc [ilość]` - Czyść wiadomości\n"
                f"`{config.BOT_PREFIX}blacklist [@użytkownik]` - Zarządzaj blacklistą\n"
                f"`{config.BOT_PREFIX}poklon` - Hołd dla Pana\n"
                f"`{config.BOT_PREFIX}zapisz` - Wymuś zapis bazy\n"
                f"`{config.BOT_PREFIX}restart` - Restart bota"
            ),
            inline=False
        )
    
    embed.set_footer(text=f"Wersja {config.BOT_VERSION} | Właściciel: {config.OWNER_NAME}")
    await ctx.send(embed=embed)

@bot.command(name="bluzg", aliases=["bluzgnij", "obraź"])
async def bluzg_command(ctx, member: discord.Member = None):
    """Wyślij bluzga do użytkownika"""
    if not await check_cooldown(ctx, "bluzg"):
        return
    
    # Sprawdź blacklistę
    if db.is_blacklisted(str(ctx.author.id)):
        embed = discord.Embed(
            title="🚫 Zablokowany",
            description="Jesteś na blackliście i nie możesz używać komend.",
            color=config.EMBED_COLORS["error"]
        )
        await ctx.send(embed=embed)
        return
    
    target = member if member else ctx.author
    
    # Ochrona właściciela
    if target.name == config.OWNER_NAME:
        embed = discord.Embed(
            title="🛡️ Ochrona Właściciela",
            description=f"Mój Pan **{config.OWNER_NAME}** jest nietykalny!",
            color=config.EMBED_COLORS["success"]
        )
        await ctx.send(embed=embed)
        return
    
    # Generuj bluzga
    intensity = random.randint(30, 95)
    bluzg = dictionary.generuj_bluzga(intensity=intensity, target_name=target.name)
    
    # Wyślij wiadomość
    prefix = f"Mój Panie **{config.OWNER_NAME}**, na rozkaz: " if is_owner(ctx.author) else ""
    msg = await ctx.send(f"{prefix}{target.mention}, {bluzg}")
    
    # Dodaj reakcje
    reactions = dictionary.generuj_reakcje(3)
    for reaction in reactions:
        await msg.add_reaction(reaction)
    
    # Zapisz statystyki
    db.add_bluzg(str(ctx.author.id), str(target.id))
    logger.bluzg_log(
        str(ctx.author.id), ctx.author.name,
        str(target.id), target.name,
        bluzg, intensity
    )
    
    # Ustaw cooldown
    await apply_cooldown(ctx, "bluzg")

@bot.command(name="komplement", aliases=["pochwal", "komplementuj"])
async def komplement_command(ctx, member: discord.Member = None):
    """Wyślij komplement do użytkownika"""
    if not await check_cooldown(ctx, "komplement"):
        return
    
    target = member if member else ctx.author
    
    # Specjalny komplement dla właściciela
    if target.name == config.OWNER_NAME:
        embed = discord.Embed(
            title="👑 Komplement dla Właściciela",
            description=f"Mój Pan **{config.OWNER_NAME}**, jesteś najwspanialszy!",
            color=config.EMBED_COLORS["admin"]
        )
        await ctx.send(embed=embed)
        return
    
    # Generuj komplement
    intensity = random.randint(40, 90)
    komplement = dictionary.generuj_komplement(intensity=intensity, target_name=target.name)
    
    # Wyślij wiadomość
    msg = await ctx.send(f"{target.mention}, {komplement}")
    
    # Dodaj reakcje
    reactions = ["❤️", "🌟", "✨"]
    for reaction in reactions:
        await msg.add_reaction(reaction)
    
    # Zapisz statystyki
    db.add_komplement(str(ctx.author.id), str(target.id))
    logger.komplement_log(
        str(ctx.author.id), ctx.author.name,
        str(target.id), target.name,
        komplement, intensity
    )
    
    # Ustaw cooldown
    await apply_cooldown(ctx, "komplement")

@bot.command(name="intensywnosc", aliases=["moc", "siła"])
async def intensity_command(ctx, level: int = 50):
    """Ustaw intensywność bluzgów/komplementów"""
    if level < 1 or level > 100:
        embed = discord.Embed(
            title="⚠️ Nieprawidłowa Wartość",
            description="Intensywność musi być w zakresie 1-100.",
            color=config.EMBED_COLORS["warning"]
        )
        await ctx.send(embed=embed)
        return
    
    user_id = str(ctx.author.id)
    user_data = db.get_user(user_id)
    user_data["settings"]["bluzg_preference"] = "custom"
    user_data["settings"]["custom_intensity"] = level
    db.update_user(user_id, user_data)
    
    embed = discord.Embed(
        title="⚡ Intensywność Ustawiona",
        description=f"Twoja intensywność została ustawiona na **{level}%**",
        color=config.EMBED_COLORS["success"]
    )
    await ctx.send(embed=embed)

# === KOMENDY STATYSTYK ===

@bot.command(name="statystyki", aliases=["stats", "staty"])
async def stats_command(ctx, member: discord.Member = None):
    """Pokaż statystyki użytkownika"""
    target = member if member else ctx.author
    user_id = str(target.id)
    user_data = db.get_user(user_id)
    
    embed = discord.Embed(
        title=f"📊 Statystyki: {target.name}",
        color=config.EMBED_COLORS["info"]
    )
    
    stats = user_data["stats"]
    embed.add_field(name="🎯 Bluzgi Wysłane", value=f"`{stats.get('bluzgi_sent', 0)}`", inline=True)
    embed.add_field(name="🎯 Bluzgi Otrzymane", value=f"`{stats.get('bluzgi_received', 0)}`", inline=True)
    embed.add_field(name="💖 Komplementy Wysłane", value=f"`{stats.get('komplementy_sent', 0)}`", inline=True)
    embed.add_field(name="💖 Komplementy Otrzymane", value=f"`{stats.get('komplementy_received', 0)}`", inline=True)
    embed.add_field(name="⚡ Aktywność Łączna", value=f"`{stats.get('total_activity', 0)}`", inline=True)
    embed.add_field(name="🛠️ Komendy Użyte", value=f"`{stats.get('commands_used', 0)}`", inline=True)
    
    # Typy bluzgów
    if "bluzgi_by_type" in stats and stats["bluzgi_by_type"]:
        bluzgi_types = "\n".join([f"• {k}: {v}" for k, v in stats["bluzgi_by_type"].items()])
        embed.add_field(name="🎭 Typy bluzgów", value=bluzgi_types, inline=False)
    
    embed.set_thumbnail(url=target.display_avatar.url)
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "statystyki", True, target=target.name)

@bot.command(name="globalne")
async def globalne(ctx):
    """Pokazuje globalne statystyki bota"""
    stats = db.get_global_stats()
    dict_stats = dictionary.get_stats()
    
    embed = discord.Embed(
        title="🌍 Statystyki Globalne Bluzgatora",
        color=config.EMBED_COLORS["admin"]
    )
    
    embed.add_field(name="🤖 Nazwa bota", value=config.BOT_NAME, inline=True)
    embed.add_field(name="📊 Wersja", value=config.BOT_VERSION, inline=True)
    embed.add_field(name="👥 Zarejestrowani użytkownicy", value=f"**{len(db.data['users'])}**", inline=True)
    embed.add_field(name="💬 Łącznie bluzgów", value=f"**{stats.get('total_bluzgi', 0)}**", inline=True)
    embed.add_field(name="💖 Łącznie komplementów", value=f"**{stats.get('total_komplementy', 0)}**", inline=True)
    embed.add_field(name="🛠️ Łącznie komend", value=f"**{stats.get('total_commands', 0)}**", inline=True)
    
    # Statystyki słownika
    embed.add_field(name="📚 Słownik bluzgów", value=f"**{dict_stats.get('total_bluzgi', 0)}**", inline=True)
    embed.add_field(name="📚 Słownik komplementów", value=f"**{dict_stats.get('total_komplementy', 0)}**", inline=True)
    embed.add_field(name="📚 Słownik cytatów", value=f"**{dict_stats.get('total_cytaty', 0)}**", inline=True)
    
    if "start_time" in stats:
        start_time = datetime.fromisoformat(stats["start_time"])
        uptime = datetime.now() - start_time
        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        embed.add_field(name="⏱️ Uptime", value=f"**{days}d {hours}h {minutes}m**", inline=False)
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "globalne", True)

@bot.command(name="ranking")
async def ranking(ctx):
    """Pokazuje ranking najaktywniejszych bluzgaczy"""
    top_bluzgi = db.get_top_bluzgi(10)
    
    if not top_bluzgi:
        await ctx.send("📊 Ranking jest pusty. Ktoś musi zacząć bluzgać!")
        return
    
    embed = discord.Embed(
        title="🏆 TOP 10 BLUZGACZY",
        description="Najwięcej wysłanych bluzgów",
        color=config.EMBED_COLORS["success"]
    )
    
    for i, user in enumerate(top_bluzgi, 1):
        embed.add_field(
            name=f"{i}. {user['username']}",
            value=f"**Bluzgi:** {user['bluzgi_sent']} | **Otrzymane:** {user['bluzgi_received']}",
            inline=False
        )
    
    global_stats = db.get_global_stats()
    embed.set_footer(text=f"Łącznie bluzgów: {global_stats.get('total_bluzgi', 0)}")
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "ranking", True)

@bot.command(name="ofiary")
async def ofiary(ctx):
    """Pokazuje ranking najczęściej bluzganych ofiar"""
    top_victims = db.get_top_victims(10)
    
    if not top_victims:
        await ctx.send("📊 Brak ofiar. Ktoś musi zostać zbuzgany!")
        return
    
    embed = discord.Embed(
        title="😭 TOP 10 OFIAR",
        description="Najwięcej otrzymanych bluzgów",
        color=config.EMBED_COLORS["warning"]
    )
    
    for i, victim in enumerate(top_victims, 1):
        embed.add_field(
            name=f"{i}. {victim['username']}",
            value=f"**Otrzymane:** {victim['bluzgi_received']} | **Wysłane:** {victim['bluzgi_sent']}",
            inline=False
        )
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "ofiary", True)

# === KOMENDY ROZRYWKOWE ===

@bot.command(name="cytat")
async def cytat(ctx):
    """Losowy cytat"""
    cytat_text = dictionary.generuj_cytat()
    embed = discord.Embed(
        title="💭 Losowy Cytat",
        description=cytat_text,
        color=config.EMBED_COLORS["info"]
    )
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "cytat", True)

@bot.command(name="wrozba")
async def wrozba(ctx, member: discord.Member = None):
    """Wróżba na dziś"""
    target = member if member else ctx.author
    wrozba_text = dictionary.generuj_wrozbe()
    
    embed = discord.Embed(
        title=f"🔮 Wróżba dla {target.name}",
        description=wrozba_text,
        color=config.EMBED_COLORS["info"]
    )
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "wrozba", True, target=target.name)

@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    """Pokazuje avatar użytkownika z komentarzem"""
    target = member if member else ctx.author
    komplement = dictionary.generuj_komplement(intensity=60, target_name=target.name)
    
    embed = discord.Embed(
        title=f"🖼️ Avatar: {target.name}",
        description=komplement,
        color=config.EMBED_COLORS["info"]
    )
    embed.set_image(url=target.display_avatar.url)
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "avatar", True, target=target.name)

@bot.command(name="ping")
async def ping(ctx):
    """Sprawdza ping bota"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Opóźnienie: **{latency}ms**",
        color=config.EMBED_COLORS["success"]
    )
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "ping", True, latency=latency)

@bot.command(name="info")
async def info(ctx):
    """Informacje o bocie"""
    embed = discord.Embed(
        title=f"🤖 {config.BOT_NAME} - Informacje",
        color=config.EMBED_COLORS["info"]
    )
    
    embed.add_field(name="📊 Wersja", value=config.BOT_VERSION, inline=True)
    embed.add_field(name="👑 Właściciel", value=config.OWNER_NAME, inline=True)
    embed.add_field(name="🔧 Prefix", value=f"`{config.BOT_PREFIX}`", inline=True)
    embed.add_field(name="📅 Uruchomiono", value=f"<t:{int(datetime.now().timestamp())}:R>", inline=True)
    embed.add_field(name="🏓 Ping", value=f"`{round(bot.latency * 1000)}ms`", inline=True)
    embed.add_field(name="🌐 Serwery", value=f"`{len(bot.guilds)}`", inline=True)
    
    embed.set_footer(text="Bluzgator v5.0 Armagedon - Zaawansowany system rozrywkowy")
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "info", True)

# === KOMENDY SYSTEMOWE ===

@bot.command(name="logi")
async def logi(ctx, lines: int = 20):
    """Pokazuje ostatnie logi (tylko dla właściciela)"""
    if not is_owner(ctx.author):
        await ctx.send("🚫 Tylko właściciel może przeglądać logi!")
        return
    
    log_content = logger.get_log_tail(lines)
    if not log_content:
        await ctx.send("📜 Brak logów do wyświetlenia.")
        return
    
    # Dzielimy logi na części (Discord ma limit 2000 znaków)
    if len(log_content) > 1900:
        log_content = log_content[-1900:]
    
    embed = discord.Embed(
        title="📜 Ostatnie Logi",
        description=f"```\n{log_content}\n```",
        color=config.EMBED_COLORS["admin"]
    )
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "logi", True, lines=lines)

@bot.command(name="słownik")
async def słownik(ctx):
    """Pokazuje statystyki słownika"""
    stats = dictionary.get_stats()
    
    embed = discord.Embed(
        title="📚 Statystyki Słownika",
        color=config.EMBED_COLORS["info"]
    )
    
    embed.add_field(name="📝 Bluzgi", value=f"**{stats.get('total_bluzgi', 0)}**", inline=True)
    embed.add_field(name="💖 Komplementy", value=f"**{stats.get('total_komplementy', 0)}**", inline=True)
    embed.add_field(name="💭 Cytaty", value=f"**{stats.get('total_cytaty', 0)}**", inline=True)
    embed.add_field(name="🔮 Wróżby", value=f"**{stats.get('total_wrozby', 0)}**", inline=True)
    
    # Kategorie bluzgów
    bluzgi_categories = dictionary.data["bluzgi"]
    bluzgi_info = "\n".join([f"• {k}: {len(v)}" for k, v in bluzgi_categories.items()])
    embed.add_field(name="🎭 Kategorie bluzgów", value=bluzgi_info, inline=False)
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "słownik", True)

@bot.command(name="dodaj")
async def dodaj(ctx, typ: str, *, treść: str):
    """Dodaje nową treść do słownika"""
    if not is_owner(ctx.author):
        await ctx.send("🚫 Tylko właściciel może dodawać do słownika!")
        return
    
    typ = typ.lower()
    success = False
    
    if typ in ["bluzg", "bluzga"]:
        success = dictionary.dodaj_bluzga(treść, "średnie")
        message = "✅ Dodano nowego bluzga do słownika!"
    elif typ in ["komplement", "pochwała"]:
        success = dictionary.dodaj_komplement(treść, "standard")
        message = "✅ Dodano nowy komplement do słownika!"
    else:
        message = "❌ Nieznany typ. Użyj: `bluzg` lub `komplement`"
    
    if success:
        embed = discord.Embed(
            title="📚 Słownik Zaktualizowany",
            description=message,
            color=config.EMBED_COLORS["success"]
        )
    else:
        embed = discord.Embed(
            title="⚠️ Uwaga",
            description=message,
            color=config.EMBED_COLORS["warning"]
        )
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "dodaj", success, typ=typ)

# === KOMENDY WŁAŚCICIELA ===

@bot.command(name="snajper")
async def snajper(ctx, member: discord.Member = None):
    """Włącza/wyłącza tryb snajpera (tylko właściciel)"""
    if not is_owner(ctx.author):
        await ctx.send("🚫 Tylko właściciel może używać snajpera!")
        return
    
    global snajper_cel
    if member:
        snajper_cel = member.mention
        embed = discord.Embed(
            title="🎯 Snajper Aktywny",
            description=f"Namierzono: {member.mention}\nKażda jego wiadomość zostanie zbuzgana!",
            color=config.EMBED_COLORS["admin"]
        )
    else:
        snajper_cel = None
        embed = discord.Embed(
            title="🔕 Snajper Wyłączony",
            description="Tryb snajpera został dezaktywowany.",
            color=config.EMBED_COLORS["success"]
        )
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "snajper", True, target=member.name if member else None)

@bot.command(name="autobluzg")
async def autobluzg(ctx):
    """Włącza/wyłącza auto-bluzg mode (tylko właściciel)"""
    if not is_owner(ctx.author):
        await ctx.send("🚫 Tylko właściciel może używać auto-bluzg!")
        return
    
    global auto_bluzg_mode
    auto_bluzg_mode = not auto_bluzg_mode
    
    if auto_bluzg_mode:
        embed = discord.Embed(
            title="🤖 Auto-Bluzg Aktywny",
            description="Bot będzie losowo bluzgać użytkowników!",
            color=config.EMBED_COLORS["admin"]
        )
    else:
        embed = discord.Embed(
            title="🔕 Auto-Bluzg Wyłączony",
            description="Tryb auto-bluzg został dezaktywowany.",
            color=config.EMBED_COLORS["success"]
        )
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "autobluzg", True, enabled=auto_bluzg_mode)

@bot.command(name="czysc")
async def czysc(ctx, amount: int = 5):
    """Czyści wiadomości (tylko właściciel)"""
    if not is_owner(ctx.author):
        await ctx.send("🚫 Tylko właściciel może czyścić wiadomości!")
        return
    
    if amount < 1 or amount > 100:
        await ctx.send("⚠️ Ilość musi być między 1 a 100!")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(
        title="🧹 Czyszczenie Zakończone",
        description=f"Usunięto **{len(deleted) - 1}** wiadomości.",
        color=config.EMBED_COLORS["success"]
    )
    msg = await ctx.send(embed=embed, delete_after=5)
    logger.command_log(str(ctx.author.id), ctx.author.name, "czysc", True, amount=amount)

@bot.command(name="blacklist")
async def blacklist(ctx, member: discord.Member = None):
    """Dodaje/usuwa użytkownika z blacklisty (tylko właściciel)"""
    if not is_owner(ctx.author):
        await ctx.send("🚫 Tylko właściciel może zarządzać blacklistą!")
        return
    
    if not member:
        # Pokaż blacklistę
        blacklist_entries = db.data["blacklist"]
        if not blacklist_entries:
            embed = discord.Embed(
                title="📋 Blacklista",
                description="Blacklista jest pusta.",
                color=config.EMBED_COLORS["info"]
            )
        else:
            entries_text = "\n".join([f"• <@{entry['user_id']}> - {entry['reason']}" for entry in blacklist_entries[:10]])
            embed = discord.Embed(
                title="📋 Blacklista",
                description=entries_text,
                color=config.EMBED_COLORS["warning"]
            )
            embed.set_footer(text=f"Łącznie: {len(blacklist_entries)} użytkowników")
        await ctx.send(embed=embed)
        return
    
    user_id = str(member.id)
    
    if db.is_blacklisted(user_id):
        # Usuń z blacklisty
        success = db.remove_from_blacklist(user_id)
        if success:
            embed = discord.Embed(
                title="✅ Usunięto z Blacklisty",
                description=f"{member.mention} został usunięty z blacklisty.",
                color=config.EMBED_COLORS["success"]
            )
        else:
                        embed = discord.Embed(
                title="❌ Błąd",
                description="Nie udało się usunąć z blacklisty.",
                color=config.EMBED_COLORS["error"]
            )
    else:
        # Dodaj do blacklisty
        success = db.add_to_blacklist(user_id, f"Dodany przez {ctx.author.name}")
        if success:
            embed = discord.Embed(
                title="✅ Dodano do Blacklisty",
                description=f"{member.mention} został dodany do blacklisty.",
                color=config.EMBED_COLORS["warning"]
            )
        else:
            embed = discord.Embed(
                title="❌ Błąd",
                description="Nie udało się dodać do blacklisty.",
                color=config.EMBED_COLORS["error"]
            )
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "blacklist", success, target=member.name)

@bot.command(name="poklon")
async def poklon(ctx):
    """Hołd dla właściciela"""
    if is_owner(ctx.author):
        embed = discord.Embed(
            title="👑 Witaj, Mój Panie!",
            description=f"**{config.OWNER_NAME}**, jesteś najwspanialszym władcą!",
            color=config.EMBED_COLORS["admin"]
        )
        embed.set_image(url="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif")
    else:
        embed = discord.Embed(
            title="🚫 Nie dla Ciebie!",
            description="Tylko mój Pan zasługuje na hołd!",
            color=config.EMBED_COLORS["error"]
        )
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "poklon", True)

@bot.command(name="zapisz")
async def zapisz(ctx):
    """Wymusza zapis bazy danych (tylko właściciel)"""
    if not is_owner(ctx.author):
        await ctx.send("🚫 Tylko właściciel może wymuszać zapis!")
        return
    
    success = db.save()
    if success:
        embed = discord.Embed(
            title="💾 Baza Zapisana",
            description="Baza danych została pomyślnie zapisana.",
            color=config.EMBED_COLORS["success"]
        )
    else:
        embed = discord.Embed(
            title="❌ Błąd Zapisania",
            description="Wystąpił błąd podczas zapisywania bazy danych.",
            color=config.EMBED_COLORS["error"]
        )
    
    await ctx.send(embed=embed)
    logger.command_log(str(ctx.author.id), ctx.author.name, "zapisz", success)

@bot.command(name="restart")
async def restart(ctx):
    """Restartuje bota (tylko właściciel)"""
    if not is_owner(ctx.author):
        await ctx.send("🚫 Tylko właściciel może restartować bota!")
        return
    
    embed = discord.Embed(
        title="🔄 Restartowanie...",
        description="Bot zostanie zrestartowany za 3 sekundy.",
        color=config.EMBED_COLORS["warning"]
    )
    await ctx.send(embed=embed)
    
    logger.info(f"Restart bota zainicjowany przez {ctx.author.name}")
    
    # Opóźnienie przed restartem
    await asyncio.sleep(3)
    
    # Zapisujemy bazę przed restartem
    db.save()
    
    # Wyłączamy bota
    await bot.close()

# === URUCHOMIENIE BOTA ===

def main():
    """Główna funkcja uruchamiająca bota"""
    logger.info("Uruchamianie Bluzgatora v5.0...")
    
    try:
        # Sprawdzamy czy token jest ustawiony
        if not config.DISCORD_TOKEN or config.DISCORD_TOKEN == "TUTAJ_WPISZ_SWOJ_TOKEN":
            print("❌ BŁĄD: Nie ustawiono tokenu Discord!")
            print("❌ Edytuj plik config.py i wpisz swój token w DISCORD_TOKEN")
            return
        
        # Uruchamiamy bota
        bot.run(config.DISCORD_TOKEN)
        
    except discord.LoginFailure:
        logger.error("Nieprawidłowy token Discord!")
        print("❌ BŁĄD: Nieprawidłowy token Discord!")
        print("❌ Sprawdź czy token w config.py jest poprawny")
    except Exception as e:
        logger.error(f"Błąd uruchamiania bota: {e}")
        print(f"❌ BŁĄD: {e}")

if __name__ == "__main__":
    main()
                