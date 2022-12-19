import discord
from discord.ext import tasks
from collections import defaultdict

client = discord.Client()


@client.event
async def on_member_join(member):
    # Obtenemos el canal de bienvenida
    welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)
    # Enviamos el mensaje de bienvenida al nuevo miembro
    await welcome_channel.send(f"Bienvenid@ al servidor de Discord de ADD Costa Tropical 😄. No olvides leer el canal #👋 reglas-de-la-casa @{member.mention}")


# Creamos un diccionario que contará el número de mensajes de cada usuario
messages_per_day = defaultdict(int)


@tasks.loop(hours=24)
async def send_morning_message():
    # Enviamos el mensaje de buenos días
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Buenos días a tod@s")

    # Reseteamos el contador de mensajes de cada usuario
    messages_per_day.clear()


@client.event
async def on_message(message):
    # Contamos el número de mensajes que envía cada usuario
    messages_per_day[message.author] += 1

    # Si un usuario envía más de 10 mensajes, lo mencionamos en un canal
    if messages_per_day[message.author] > 10:
        channel = client.get_channel(MENTION_CHANNEL_ID)
        await channel.send(f"Madre mía illo, hoy no paras de escribir colega @{message.author.mention}")


@client.event
async def on_ready():
    # Iniciamos la tarea que envía el mensaje de buenos días
    send_morning_message.start()

client.run(TOKEN)
