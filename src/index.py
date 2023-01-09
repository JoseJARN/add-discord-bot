from dotenv import dotenv_values
import discord
from discord.ext import commands
from discord.ext import tasks
from collections import defaultdict
import datetime

days_of_week = ["lunes", "martes", "miércoles",
                "jueves", "viernes", "sábado", "domingo"]

messages_per_day = defaultdict(int)


config = dotenv_values(".env")
connection = dotenv_values(".connection.env")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Tarea: resetear el contador de mensajes cada día a las 12 de la noche
# MADRID AS TIMEZONE
TIMEZONE = datetime.timezone(datetime.timedelta(hours=1))
TIME_MIDNIGHT = datetime.time(hour=0, minute=0, second=0, tzinfo=TIMEZONE)
TIME_GOOD_MORNING = datetime.time(hour=9, minute=0, second=0, tzinfo=TIMEZONE)


@tasks.loop(time=TIME_MIDNIGHT)
async def reset_messages_per_day():
    # Reseteamos el contador de mensajes de cada usuario
    messages_per_day.clear()


# Tarea: enviar mensaje de buenos días cada día a las 9:00
@tasks.loop(time=[TIME_GOOD_MORNING])
async def send_morning_message():
    # Enviamos el mensaje de buenos días
    channel = client.get_channel(int(config["CHANNEL_GENERAL_ID"]))
    await channel.send(
        "Buenos días a tod@s. ¡¡A por el %s!!" % days_of_week[datetime.datetime.now().weekday()])


@client.event
async def on_ready():
    print(f'- El bot ha iniciado sesión {client}')

    # Iniciamos sesión enviando un mensaje en el canal de bots
    channel = client.get_channel(int(config["CHANNEL_BOTS_ID"]))
    await channel.send("¡Hola, devs! He arrancado.")

    # Tareas: Iniciamos la tarea que envía el mensaje de buenos días
    send_morning_message.start()


@client.event
async def on_message(message):
    # lower case message.content
    current_message = message.content.lower()

    if current_message == 'ping':
        await message.channel.send('¡Pong!')

    # Contamos el número de mensajes que envía cada usuario
    messages_per_day[message.author] += 1

    # Si un usuario envía más de 10 mensajes, lo mencionamos en un canal
    if messages_per_day[message.author] == 10 and message.author != client.user:
        await message.channel.send(f"Madre mía illo, hoy no paras de escribir colega {message.author.mention}")


@client.event
async def on_member_join(member):
    # Obtenemos el canal de bienvenida
    welcome_channel = client.get_channel(int(config["CHANNEL_WELCOME_ID"]))
    # Enviamos el mensaje de bienvenida al nuevo miembro
    await welcome_channel.send(f"Bienvenid@ al servidor de Discord de ADD Costa Tropical 😄. No olvides leer el canal #👋 reglas-de-la-casa {member.mention}")

client.run(connection["TOKEN"])
