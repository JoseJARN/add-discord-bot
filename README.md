# ADD Discord Bot

En unos de mis días de múltiple aburrimiento se me ocurrió la maravillosa idea de probar a hacer un Bot de Discord en Python.

## ¿Por qué en Python? 🐍

Porque la mayoría de ejemplos y documentación que encontraba era en este lenguaje y quería que fuese algo rápido y sin demasiada complicación.

## ¿Puedo usar el código? 🤝

Puedes usarlo si quieres, me da igual. De hecho lo he subido y voy a subir al repo sin las credenciales del servidor en concreto donde voy a usarlo para que pueda usarlo cualquiera sustituyendo las palabras clave.

## Extra:

La verdad es que no tengo mucho más que contar sobre ello. Si quiero actualizar más información al respecto la iré comentando a continuación.

---

## Instrucciones

```
welcome_channel = client.get_channel(CHANNEL_WELCOME_ID)
```

- **CHANNEL_WELCOME_ID** = ID del canal donde aterrizan los nuevos usuarios

```
channel = client.get_channel(CHANNEL_GENERAL_ID)
```

- **CHANNEL_GENERAL_ID** = ID del canal donde quieres que el bot de los buenos días.

```
channel = client.get_channel(CHANNEL_MENTION_ID)
```

- **CHANNEL_GENERAL_ID** = ID del canal donde quieres que el bot mencione al usuario que ha escrito más de 10 mensajes.

```
channel = client.get_channel(CHANNEL_MENTION_ID)
```

- **TOKEN** = El token que generas cuando creas una aplicación para el bot.
