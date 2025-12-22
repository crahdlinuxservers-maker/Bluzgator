import discord
from discord.ext import commands
import random

# --- KONFIGURACJA ---
PAN_I_WLADCA = "Crahd"  # Twój nick na Discordzie (uważaj na wielkość liter!)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# Pamięć operacyjna bota
ranking_dzbanow = {}
snajper_cel = None

# --- BAZA SŁÓW ---
przymiotniki = [
    "miły", "sympatyczny", "uprzejmy", "dobry", "serdeczny", "życzliwy",
    "przyjacielski", "uśmiechnięty", "radośny", "szczęśliwy", "zadowolony",
    "wesoły", "optymistyczny", "pozytywny", "entuzjastyczny", "energiczny",
    "kreatywny", "pomysłowy", "utalentowany", "zdolny", "inteligentny",
    "mądry", "rozsądny", "logiczny", "analityczny", "spostrzegawczy",
    "dociekliwy", "ciekawski", "badawczy", "sumienny", "staranny",
    "dokładny", "precyzyjny", "profesjonalny", "skuteczny", "wydajny",
    "sprawny", "szybki", "zwinny", "silny", "wytrzymały", "odporny",
    "cierpliwy", "spokojny", "opanowany", "zrównoważony", "harmonijny",
    "łagodny", "delikatny", "wrażliwy", "empatyczny", "współczujący",
    "opiekuńczy", "troskliwy", "pomocny", "altruistyczny", "szlachetny",
    "uczciwy", "prawdomówny", "lojalny", "wierny", "honorowy", "rycerski",
    "odważny", "śmiały", "dzielny", "bohaterski", "waleczny", "nieustraszony"
]

rzeczowniki = [
    "przyjacielu", "kolego", "partnerze", "towarzyszu", "znajomy", "bliski",
    "serdeczny", "dobroczyńca", "opiekun", "pomocnik", "wsparcie", "filar",
    "bohaterze", "mistrzu", "ekspercie", "znawco", "mędrcze", "filozofie",
    "myślicielu", "wizjonerze", "twórco", "artysto", "geniuszu", "talent",
    "skarb", "klejnot", "perła", "diament", "złoto", "srebro", "platyna",
    "promień", "gwiazda", "słońce", "księżyc", "zorza", " tęcza", "kwiat",
    "róża", "lilia", "orchidea", "motyl", "ptak", "łabędź", "orzeł",
    "lew", "tygrys", "pantera", "wilk", "lis", "sarna", "koń",
    "delfin", "wieloryb", "ocean", "morze", "rzeka", "góra", "las",
    "łąka", "pole", "ogród", "pałac", "zamek", "świątynia", "fontanna",
    "most", "droga", "latarnia", "świeca", "iskra", "płomień", "ogień",
    "woda", "powietrze", "ziemia", "wszechświat", "galaktyka", "gwiazdozbiór",
    "planeta", "księżyc", "słońce", "atom", "cząstka", "energia", "siła",
    "moc", "harmonia", "równowaga", "spokój", "cisza", "szczęście", "radość",
    "miłość", "nadzieja", "wiara", "inspiracja", "motywacja", "pasja",
    "marzenie", "cel", "droga", "przyszłość", "wieczność", "nieskończoność"
]

dodatki = [
    "o sercu ze złota", "z uśmiechem rozjaśniającym dzień", "o duszy artysty",
    "który zawsze wie co powiedzieć", "z energią wulkanu",
    "o umyśle bystrym jak brzytwa", "z charyzmą gwiazdy filmowej",
    "którego obecność uszczęśliwia", "z wdziękiem tancerza",
    "o spojrzeniu pełnym życzliwości", "który potrafi rozśmieszyć każdego",
    "z talentem do tworzenia piękna", "o głosie anioła",
    "którego pomysły zmieniają świat", "z siłą lwa",
    "o mądrości starca", "który inspiruje innych",
    "z pasją odkrywcy", "o marzeniach sięgających gwiazd",
    "który zawsze dotrzymuje słowa", "z odwagą wojownika",
    "o sercu pełnym miłości", "z nadzieją w oczach",
    "o wierze niezachwianej", "którego optymizm jest zaraźliwy",
    "z pozytywną aurą", "o umyśle otwartym na nowe",
    "który potrafi słuchać", "z empatią wobec innych",
    "o wrażliwości poety", "który dba o bliskich",
    "z troską w sercu", "o dobroci bez granic",
    "który jest wsparciem dla przyjaciół", "z lojalnością godną podziwu",
    "o honorze rycerza", "który zawsze staje w obronie słabszych",
    "z uczciwością krystaliczną", "o prawdomówności budzącej zaufanie",
    "którego obecność przynosi spokój", "z harmonią wewnętrzną",
    "o łagodności dotyku", "który potrafi pocieszyć w trudnych chwilach",
    "z optymizmem niezniszczalnym", "o sile ducha",
    "który jest promykiem słońca w pochmurny dzień", "z iskrą w oku",
    "o płomieniu pasji", "który jest jak powiew świeżego powietrza",
    "z energią nieskończoną", "o potencjale bez granic"
]

emojis = ["😊", "🌟", "💖", "✨", "🌸", "🦋", "🌞", "👍", "👍", "💖", "🌸", "😊"]

def generuj_komplement():
    return f"{random.choice(przymiotniki)} {random.choice(rzeczowniki)} {random.choice(dodatki)}"

@bot.event
async def on_ready():
    print(f'-----------------------------------------')
    print(f'BOT KOMPLEMENTATOR 1.0 - ONLINE')
    print(f'Zalogowano jako: {bot.user.name}')
    print(f'Władca: {PAN_I_WLADCA}')
    print(f'-----------------------------------------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    global snajper_cel
    if snajper_cel and message.author.mention == snajper_cel:
        await message.channel.send(f"{message.author.mention}, jesteś {generuj_komplement()}!")
    await bot.process_commands(message)

@bot.command()
async def komplementator(ctx):
    """Główne menu pomocy - Embed"""
    embed = discord.Embed(title="💖 Centrala Komplementatora v1.0", color=0xff69b4)
    embed.add_field(name="✨ KOMPLEMENTY I ZABAWA", value="`!komplementuj @user` - Generuj komplement\n`!cytat` - Losowy pozytywny cytat\n`!avatar @user` - Miły komentarz zdjęcia", inline=False)
    embed.add_field(name="📊 ANALIZA", value="`!pozytywnosc @user` - Poziom pozytywności\n`!szczescie @user` - Wróżba szczęścia\n`!ranking` - TOP 5 osób z najwięcej komplementami", inline=False)
    embed.add_field(name="👑 DLA PANA", value="`!snajper @user` - Komplementowanie celu\n`!czysc [ile]` - Czyść czat\n`!poklon` - Hołd dla Pana\n`!changelog` - Zmiany", inline=False)
    embed.set_footer(text=f"Sługa Pana {PAN_I_WLADCA}")
    await ctx.send(embed=embed)

@bot.command()
async def komplementuj(ctx, member: discord.Member = None):
    if member and member.name == PAN_I_WLADCA:
        await ctx.send(f"🛡️ Mój Pan **{PAN_I_WLADCA}**, jesteś najwspanialszy!")
        return
    target = member if member else ctx.author
    ranking_dzbanow[target.name] = ranking_dzbanow.get(target.name, 0) + 1
    prefix = f"Mój Panie **{PAN_I_WLADCA}**, na rozkaz: " if ctx.author.name == PAN_I_WLADCA else ""
    msg = await ctx.send(f"{prefix}{target.mention}, jesteś {generuj_komplement()}!")
    await msg.add_reaction(random.choice(emojis))

@bot.command()
async def szczescie(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    wrozby = [
        "Spotkasz kogoś mądrzejszego od siebie. Będzie to miłe doświadczenie.",
        "Twoje szczęście jest jak Twój intelekt – imponujące!",
        "Gwiazdy radzą: podążaj za swoimi marzeniami.",
        "Dziś unikaj luster. Twoje piękno może oślepić!",
        "Twój mózg dziś wejdzie w tryb geniuszu!"
    ]
    await ctx.send(f"🍀 **Wróżba Szczęścia** dla {target.mention}: {random.choice(wrozby)}")

@bot.command()
async def pozytywnosc(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    await ctx.send(f"✨ Skanuję {target.mention}... Wynik: **{random.randint(50, 100)}%** pozytywności.")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    embed = discord.Embed(title=f"Piękno: {target.name}", color=0xff69b4)
    embed.set_image(url=target.display_avatar.url)
    await ctx.send(content=f"Spójrzcie na tę wspaniałą osobę: {generuj_komplement()}", embed=embed)

@bot.command()
async def cytat(ctx):
    teksty = ["Twoje IQ jest tak wysokie, że możesz dotknąć gwiazd.", "Gdyby dobro miało skrzydła, latałbyś jak anioł."]
    await ctx.send(random.choice(teksty))

@bot.command()
async def ranking(ctx):
    if not ranking_dzbanow:
        return await ctx.send("Ranking jest pusty.")
    sort = sorted(ranking_dzbanow.items(), key=lambda x: x[1], reverse=True)
    txt = "**🏆 TOP OSOBY Z KOMPLEMENTAMI:**\n"
    for i, (u, c) in enumerate(sort[:5], 1):
        txt += f"{i}. {u} — {c} komplementów\n"
    await ctx.send(txt)

@bot.command()
async def snajper(ctx, member: discord.Member = None):
    if ctx.author.name != PAN_I_WLADCA: return
    global snajper_cel
    snajper_cel = member.mention if member else None
    await ctx.send(f"🎯 Snajper namierzył: {snajper_cel}" if snajper_cel else "🔕 Snajper OFF")

@bot.command()
async def czysc(ctx, amount: int = 5):
    if ctx.author.name == PAN_I_WLADCA:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Sprzątnięto {amount} wiadomości.", delete_after=3)

@bot.command()
async def poklon(ctx):
    if ctx.author.name == PAN_I_WLADCA:
        await ctx.send(f"🙇‍♂️ Witaj, potężny **{PAN_I_WLADCA}**!")
    else:
        await ctx.send("Zjeżdżaj, tylko Pan zasługuje na hołd!")

@bot.command()
async def changelog(ctx):
    await ctx.send("✨ **v1.0:** Utworzono bota Komplementatora!")

# --- URUCHOMIENIE ---
bot.run('Tutaj wpisz swoj token')
