import random
from dotenv import dotenv_values
import discord
from discord.ext import commands
from discord.ext import tasks
from collections import defaultdict
import datetime

from lib.db import db

days_of_week = ["lunes", "martes", "miércoles",
                "jueves", "viernes", "sábado", "domingo"]

messages_per_day = defaultdict(int)

random_morning_phrases = [
    "Buenos días, hoy es %s.",
    "Saludos en este %s.",
    "Espero que tengas un excelente %s.",
    "¡Hola! ¿Cómo va este %s?",
    "Deseándote un maravilloso %s.",
    "Que tengas un %s lleno de bendiciones.",
    "Buenos días en este %s soleado.",
    "¡Feliz %s!",
    "Comienza bien este %s.",
    "Disfruta de este %s al máximo.",
    "Te deseo un %s lleno de alegría.",
    "Buenos días, espero que este %s sea grandioso.",
    "¡Hola! ¿Listo para enfrentar este %s?",
    "Que tengas un %s productivo.",
    "Sonríe, es %s.",
    "Deseándote un %s lleno de éxitos.",
    "Que tengas un %s tranquilo y relajante.",
    "Buenos días, que %s te traiga grandes oportunidades.",
    "¡Hola! ¿Estás listo para conquistar este %s?",
    "Te deseo un %s lleno de inspiración.",
    "Espero que disfrutes de este %s al máximo.",
    "Buenos días en este %s fresco y agradable.",
    "¡Hola! ¿Qué planes tienes para este %s?",
    "Que tengas un %s lleno de buenas noticias.",
    "Deseándote un %s lleno de amor y felicidad.",
    "Disfruta de este %s soleado y radiante.",
    "Te deseo un %s lleno de sorpresas agradables.",
    "Buenos días, que este %s sea increíblemente positivo.",
    "¡Hola! ¿Listo para hacer de este %s un día increíble?",
    "Que tengas un %s lleno de energía y entusiasmo.",
    "Sonríe, es %s, la mejor excusa para ser feliz.",
    "Deseándote un %s lleno de risas y buenos momentos.",
    "Buenos días, %s es el día perfecto para brillar.",
    "¡Hola! ¿Estás preparado para aprovechar al máximo este %s?",
    "¡Feliz %s! Que todos tus sueños se hagan realidad.",
    "Espero que disfrutes cada momento de este %s.",
    "Buenos días en este %s prometedor y emocionante.",
    "¡Hola! ¿Qué aventuras te esperan en este %s?",
    "Que tengas un %s lleno de logros y satisfacciones.",
    "Deseándote un %s lleno de amor y prosperidad.",
    "Buenos días, %s te trae nuevas oportunidades.",
    "Buenos días a tod@s. ¡¡A por el %s!!"
]

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
TIME_EVERY_MINUTE = datetime.time(second=0, tzinfo=TIMEZONE)


async def send_devs_message(channel, message):
    channel = client.get_channel(int(config["CHANNEL_BOTS_ID"]))
    await channel.send(message)


@tasks.loop(time=[TIME_EVERY_MINUTE])
async def save_database():
    db.commit()


@tasks.loop(time=[TIME_MIDNIGHT])
async def reset_messages_per_day():
    # Reseteamos el contador de mensajes de cada usuario
    messages_per_day.clear()


# Tarea: enviar mensaje de buenos días cada día a las 9:00
@tasks.loop(time=[TIME_GOOD_MORNING])
async def send_morning_message():
    # Enviamos el mensaje de buenos días
    channel = client.get_channel(int(config["CHANNEL_GENERAL_ID"]))

    # Elegir una frase aleatoria de random_morning_phrases
    random_morning_phrase = random_morning_phrases[random.randint(
        0, len(random_morning_phrases) - 1)]

    await channel.send(
        random_morning_phrase % days_of_week[datetime.datetime.now().weekday()])


@client.event
async def on_ready():
    print(f'- El bot ha iniciado sesión {client}')

    # db.autosave()

    # Iniciamos sesión enviando un mensaje en el canal de bots
    channel = client.get_channel(int(config["CHANNEL_BOTS_ID"]))
    await channel.send("¡Hola, devs! He arrancado en entorno local.")

    # Tareas: Iniciamos la tarea que envía el mensaje de buenos días
    send_morning_message.start()


@client.event
async def on_message(message):
    # lower case message.content
    current_message = message.content.lower()

    if current_message == 'ping':
        await message.channel.send('¡Pong!')

    # Comprobamos si el usuario ha enviado el comando !youtube para enviarle el enlace del canal
    if current_message == '!youtube':
        await message.channel.send('Aquí tienes el canal de ADD Costa Tropical 📹💙 https://www.youtube.com/@ADDCostaTropical')

    # Comprobamos si ha enviado !meetup o !eventos
    if current_message == '!meetup' or current_message == '!eventos':
        await message.channel.send('Aquí tienes el calendario de eventos de ADD Costa Tropical 📅💙 https://www.meetup.com/addcostatropical/')

    # Comprobamos si ha enviado !twitter
    if current_message == '!twitter':
        await message.channel.send('Aquí tienes el perfil de Twitter de ADD Costa Tropical 🐦💙 https://twitter.com/addcostatropica')

    # Comprobamos si ha enviado !instagram
    if current_message == '!instagram':
        await message.channel.send('Aquí tienes el perfil de Instagram de ADD Costa Tropical 📸💙 https://www.instagram.com/addcostatropical/')

    # Contamos el número de mensajes que envía cada usuario
    messages_per_day[message.author] += 1

    # Si un usuario envía más de 10 mensajes, lo mencionamos en un canal
    if messages_per_day[message.author] == 50 and message.author != client.user:
        await message.channel.send(f"Madre mía, {message.author.mention}... Hoy no paras de escribir, colega...")

    # Si el usuario Joaquín menciona a este bot o le responde un mensaje al bot, le enviamos un mensaje
    if message.author.id == int(config['USER_ADAM']) and (client.user.mentioned_in(message) or (message.reference and message.reference.resolved.author == client.user)):
        print('Joaquín ha mencionado al bot')
        # enviamos una foto como respuesta
        # await message.channel.send(file=discord.File('../data/img/joaquinillo.jpg'))
        # obtenemos un insulto aletorio de la base de datos que sea el menos usado
        print("esta es la db:" + str(db))
        # RANDOM
        insult = db.field(
            "SELECT insulto FROM insultos_list ORDER BY veces_usado ASC LIMIT 1 OFFSET (SELECT (ABS(RANDOM()) % (SELECT COUNT(*) FROM insultos_list)))")
        print("Esto ha devuelto la consulta: " + insult)
        # respondemos el insulto al mensaje
        await message.reply(insult)

        # actualizamos el número de veces que se ha usado el insulto
        db.execute(
            "UPDATE insultos_list SET veces_usado = veces_usado + 1 WHERE insulto = '" + insult + "'")

    if message in ["pole", "subpole", "palco"]:


@client.event
async def on_error(event, *args, **kwargs):
    if event == 'on_command_error':
        await args[0].send('¡Lo siento, no he entendido el comando! 😅')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('¡Lo siento, no he entendido el comando! 😅')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('¡Lo siento, no has introducido todos los argumentos! 😅')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('¡Lo siento, no tienes permisos para ejecutar este comando! 😅')
    else:
        await ctx.send('¡Lo siento, ha ocurrido un error! 😅')


@client.event
async def on_member_join(member):
    # Obtenemos el canal de bienvenida
    welcome_channel = client.get_channel(int(config["CHANNEL_WELCOME_ID"]))
    # Enviamos el mensaje de bienvenida al nuevo miembro
    await welcome_channel.send(f"Bienvenid@ al servidor de Discord de ADD Costa Tropical 😄. No olvides leer el canal #👋 reglas-de-la-casa {member.mention}")

client.run(connection["TOKEN"])
