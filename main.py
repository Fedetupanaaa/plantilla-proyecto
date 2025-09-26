import discord
import requests
from discord.ext import commands
import pyttsx3
from deep_translator import GoogleTranslator


def traducir(text: str) -> str:
    """Traduce de inglés a español."""
    try:
        return GoogleTranslator(source="en", target="es").translate(text)
    except Exception as e:
        print("Error al traducir:", e)
        return text


def talk(text: str):
    """Lee en voz alta un texto con pyttsx3."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 125)
    engine.setProperty("volume", 1.0)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    engine.say(text)
    engine.runAndWait()


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def hola(ctx):
    await ctx.send("Hola soy tu asistente virtual")
    talk("Hola soy tu asistente virtual")


def fun_facts() -> str:
    """Obtiene un dato curioso desde uselessfacts API."""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        return respuesta.json().get("text", "No se pudo obtener este dato")
    return "Error: no se pudo conectar a la API"


def fun_comida() -> str:
    """Obtiene una comida aleatoria desde TheMealDB."""
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        data = respuesta.json()
        if "meals" in data and data["meals"]:
            return data["meals"][0]["strMeal"]
        return "No se pudo obtener la comida"
    return "Error: no se pudo conectar a la API"


@bot.command()
async def fact(ctx):
    facto = fun_facts()
    facto = traducir(facto)
    await ctx.send(f"Tu dato curioso es: {facto}")
    talk(f"Tu dato curioso es: {facto}")


@bot.command()
async def comida(ctx):
    comida_random = fun_comida()
    comida_random = traducir(comida_random)
    await ctx.send(f"Tu comida aleatoria es: {comida_random}")
    talk(f"Tu comida aleatoria es: {comida_random}")


bot.run(
    "TOken"
)
