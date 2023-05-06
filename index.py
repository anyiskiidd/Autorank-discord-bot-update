import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents) ##Et ça c'est les intents pour dire que le bot dispose de la permission

ROLE_ID = "id du role que le bot va donner"
CHANNEL_ID = "id du channel spécifique dans lequel le membre devra mentionner le bot"

@client.event
async def on_ready():
    print("Bot prêt")

@client.event
async def on_message(message):
    if not message.author.bot and client.user.mentioned_in(message):
        member = message.author
        if "tag" or "tag" in member.name: ##"If" c'est pour dire que si il a tag=211 ou tag=²¹¹ la commande marche, et le "else" c'est pour le cas contraire
            if message.channel.id == CHANNEL_ID and not ("@everyone" in message.content or "@here" in message.content): ##Pour que ca ne prenne pas en compte @everyone et @here
                role = message.guild.get_role(ROLE_ID)
                if role is not None:
                    await member.add_roles(role)
                    reply_msg = f"{member.mention}, le rôle vous a été donné avec succès !"
                else:
                    reply_msg = f"Le rôle est introuvable sur ce serveur."
            else:
                reply_msg = f"{member.mention}, vous devez mentionner le bot dans le canal {client.get_channel(CHANNEL_ID).mention} pour recevoir le rôle !" ##{client.get_channel(CHANNEL_ID).mention} c'est pour que ca mentionne le channel défini par "CHANNEL_ID = "channel id""
        else:
            reply_msg = f"{member.mention}, tu n'as pas le bon pseudo pour recevoir le rôle."
        
        bot_message = await message.reply(reply_msg) ##Ca c'est pour que le bot reponde au mess
        await bot_message.delete(delay=7) ##Ca ca supprime les mess du bot après 7sec
    
    await client.process_commands(message)

client.run('token')

##Je t'ai mit toute les explications comme ca si tu veux modif le script tu peux