import discord
from discord.ext import commands
from datetime import datetime
from discord import Game, Activity, ActivityType
import pytz
from datetime import datetime

tz = pytz.timezone('Europe/Paris')

date_str = datetime.now(tz).strftime('%A %d %B %Y')
heure_str = datetime.now(tz).strftime('%H:%M:%S')

date_str = datetime.utcnow().strftime('%A %d %B %Y')
heure_str = datetime.utcnow().strftime('%H:%M:%S')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

ROLE_ID = ID of the role that you want the bot to give to the user who à him
CHANNEL_ID = IF of the chanel that you want the users to @ the bot
LOG_CHANNEL_ID = the ID of the channel that you want the bot to send the logs (to who he gave the role, when, which role..)
BL_ROLE_ID = ID of the "bl role", the role that you want if a user have it and if he @ the bot, the bot don't give him the rôle.


@client.event
async def on_ready():
    await client.change_presence(activity=Activity(type=ActivityType.streaming, name="discord.gg/211"))
    print('Bot Prêt')


@client.event
async def on_member_update(before, after):
    role = after.guild.get_role(ROLE_ID)
    if role is not None:
        if ("tag1" in before.name or "tag2" in before.name) and not ("tag1" in after.name or "tag2" in after.name):
            if role in before.roles:
                await after.remove_roles(role)
                message = f"{after.mention} a perdu le rôle {role.name}"
                print(message)
        elif ("tag1" not in after.name and "tag2" not in after.name):
            if role in after.roles:
                await after.remove_roles(role)
                message = f"{after.mention} a perdu le rôle {role.name}"
                print(message)


@client.event
async def on_message(message):
    if not message.author.bot and client.user in message.mentions:
        member = message.author
        if "tag1" in member.name or "tag2" in member.name:
            if message.channel.id == CHANNEL_ID and not ("@everyone" in message.content or "@here" in message.content):
                bl_role = message.guild.get_role(BL_ROLE_ID) # Récupère le rôle "bl 211"
                role = message.guild.get_role(ROLE_ID) # Récupère le rôle à ajouter
                if role is not None:
                    if bl_role in member.roles:
                        reply_msg = f"{member.mention}, je ne peux pas vous donner le rôle {role.name} car vous avez le rôle {bl_role.name} !"
                    elif role in member.roles:
                        reply_msg = f"{member.mention}, vous avez déjà le rôle {role.name} !"
                    else:
                        await member.add_roles(role)
                        reply_msg = f'{member.mention}, le rôle "{role.name}" vous a été donné avec succès !'

                        log_embed = discord.Embed(title=f"Nouveau Log Autorank !", color=discord.Color.from_rgb(25, 25, 25))
                        log_embed.add_field(name="Modérateur", value=f"<@ID OF YOUR BOT>")
                        log_embed.add_field(name="Membre", value=f"{member.mention}")
                        log_embed.add_field(name="Rôle donné", value=f"{role.mention}")
                        log_embed.set_footer(text=f"Donné le {date_str} à {heure_str}")

                        log_channel = client.get_channel(LOG_CHANNEL_ID)
                        if log_channel is not None:
                            await log_channel.send(embed=log_embed)
                        else:
                            reply_msg = f"Une erreur est survenue, veuillez contacter un admin !"
                else:
                    reply_msg = f"Une erreur est survenue, veuillez contacter un admin !"
            else:
                reply_msg = f"{member.mention}, vous devez mentionner le bot dans le canal {client.get_channel(CHANNEL_ID).mention} pour recevoir le rôle !"
        else:
            role = message.guild.get_role(ROLE_ID)
            if role is not None and role in member.roles:
                await member.remove_roles(role)
                reply_msg = f"{member.mention}, Vous avez perdu le rôle {role.name} car vous n'avez plus le tag !"
            else:
                reply_msg = f"{member.mention}, Vous devez avoir le tag pour obtenir le rôle !"

        bot_message = await message.channel.send(reply_msg)

    await client.process_commands(message)

    




client.run('TOKEN')
