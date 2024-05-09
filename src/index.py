from dotenv import dotenv_values
import discord
from discord.ext import tasks
from collections import defaultdict
import datetime
import pytz

days_of_week = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

messages_per_day = defaultdict(int)

config = dotenv_values(".env")
connection = dotenv_values(".connection.env")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Definición de las zonas horarias y horas de tareas
TIMEZONE = pytz.timezone('Europe/Madrid')
TIME_MIDNIGHT = datetime.time(hour=0, minute=0, second=0, tzinfo=TIMEZONE)
TIME_GOOD_MORNING = datetime.time(hour=9, minute=0, second=0, tzinfo=TIMEZONE)

# Variables para la funcionalidad adicional
last_message_time = datetime.datetime.now(TIMEZONE)
alert_24_hours_sent = False
alert_48_hours_sent = False

async def send_devs_message(channel, message):
    await channel.send(message)

@tasks.loop(time=[TIME_MIDNIGHT])
async def reset_messages_per_day():
    messages_per_day.clear()

@tasks.loop(time=[TIME_GOOD_MORNING])
async def send_morning_message():
    channel = client.get_channel(int(config["CHANNEL_GENERAL_ID"]))
    if channel:
        weekday_index = datetime.datetime.now(TIMEZONE).weekday()
        await channel.send(f"Buenos días a tod@s. ¡¡A por el {days_of_week[weekday_index]}!!")

@tasks.loop(hours=1)
async def check_activity():
    global last_message_time, alert_24_hours_sent, alert_48_hours_sent

    now = datetime.datetime.now(TIMEZONE)
    delta = now - last_message_time
    general_channel = client.get_channel(int(config["CHANNEL_GENERAL_ID"]))

    if delta.total_seconds() >= 86400 and not alert_24_hours_sent:
        # Pasaron 24 horas sin actividad
        await general_channel.send("@everyone ¿Qué ocurre cabroncetes? Estáis muy calladas.")
        alert_24_hours_sent = True
    elif delta.total_seconds() >= 172800 and not alert_48_hours_sent:
        # Pasaron 48 horas sin actividad
        await general_channel.send("@everyone Oye, esto ya me está empezando a preocupar cabrones. Manifestaros.")
        alert_48_hours_sent = True

@client.event
async def on_ready():
    print(f'- El bot ha iniciado sesión {client}')

    # Enviar mensaje de bienvenida en el canal de bots
    channel = client.get_channel(int(config["CHANNEL_BOTS_ID"]))
    if channel:
        await channel.send("¡Hola, devs! He arrancado.")

    # Iniciar tareas periódicas
    send_morning_message.start()
    reset_messages_per_day.start()
    check_activity.start()

@client.event
async def on_message(message):
    global last_message_time, alert_24_hours_sent, alert_48_hours_sent

    if message.author.bot:
        return

    # Actualizar tiempo del último mensaje y resetear alertas
    last_message_time = datetime.datetime.now(TIMEZONE)
    alert_24_hours_sent = False
    alert_48_hours_sent = False

    current_message = message.content.lower()

    # Mapeo de comandos a mensajes de respuesta
    commands = {
        '!ping': '¡Pong!',
        '!youtube': 'El canal de ADD Costa Tropical pasó a mejor vida o más bien cambió de nombre (que es casi lo mismo), aún así te dejo el de @bienvenidosaez (es ese pero con el nombre cambiado) 📹💙 https://www.youtube.com/@bienvenidosaez',
        '!meetup': 'Aquí tienes el calendario de eventos de ADD Costa Tropical 📅💙 https://www.meetup.com/addcostatropical/',
        '!eventos': 'Aquí tienes el calendario de eventos de ADD Costa Tropical 📅💙 https://www.meetup.com/addcostatropical/',
        '!twitter': 'Aquí tienes el perfil de Twitter de ADD Costa Tropical 🐦💙 https://twitter.com/addcostatropica',
        '!instagram': 'Aquí tienes el perfil de Instagram de ADD Costa Tropical 📸💙 https://www.instagram.com/addcostatropical/'
    }

    if current_message in commands:
        await message.channel.send(commands[current_message])

    # Contar el número de mensajes por usuario
    messages_per_day[message.author] += 1

    # Mensaje especial cuando se alcanzan los 50 mensajes
    if messages_per_day[message.author] == 50:
        await message.channel.send(f"Madre mía, {message.author.mention}... Hoy no paras de escribir, colega...")

    # Respuesta específica para Joaquín
    if message.author.id == int(config['USER_JOAQUIN']) and (
            client.user.mentioned_in(message) or
            (message.reference and message.reference.resolved.author == client.user)):
        await message.channel.send(file=discord.File('../data/img/joaquinillo.jpg'))

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(int(config["CHANNEL_WELCOME_ID"]))
    if welcome_channel:
        await welcome_channel.send(f"Bienvenid@ al servidor de Discord de ADD Costa Tropical 😄. No olvides leer el canal #👋 reglas-de-la-casa {member.mention}")

client.run(connection["TOKEN"])