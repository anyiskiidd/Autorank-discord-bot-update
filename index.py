import discord
from discord.ext import commands
from datetime import datetime
from discord import Game, Activity, ActivityType
import pytz
from datetime import datetime
import json
import logger

tz = pytz.timezone('Europe/Paris')

date_str = datetime.now(tz).strftime('%A %d %B %Y')
heure_str = datetime.now(tz).strftime('%H:%M:%S')

date_str = datetime.utcnow().strftime('%A %d %B %Y')
heure_str = datetime.utcnow().strftime('%H:%M:%S')

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

settings = json.load(open("config.json"))
LogSettings = settings["logSettings"]

logger = logger.Logger(client, LogSettings)


@client.event
async def on_ready():
    await client.change_presence(activity=Activity(type=ActivityType.streaming, name="discord.gg/211"))
    print('Bot Prêt')


@client.event
async def on_member_update(before, after):
    for tag, id in settings["autoTags"].items():
        print(tag, id)
        if tag not in after.name and tag in before.name:
            role = after.guild.get_role(id)
            await after.remove_roles(role)
            # log_embed = discord.Embed(title=f"Nouveau Log Autorank !", color=discord.Color.from_rgb(25, 25, 25))
            # log_embed.add_field(name="Modérateur", value=f"<@{client.user.id}>")
            # log_embed.add_field(name="Membre", value=f"{after.mention}")
            # log_embed.add_field(name="Rôle supprimé", value=f"{role.mention}")
            # log_embed.set_footer(text=f"Supprimé le {date_str} à {heure_str}")

            # log_channel = client.get_channel(settings["logChannel"])
            # if log_channel is not None:
            #     await log_channel.send(embed=log_embed)

            await logger.log("Nouveau Log Autorank ! (TAG)", {
                "Modérateur": f"<@{client.user.id}>",
                "Membre": f"{after.mention}",
                "Rôle supprimé": f"{role.mention}"
            }, f"Supprimé le {date_str} à {heure_str}")

        if tag in after.name and tag not in before.name:
            role = after.guild.get_role(id)
            await after.add_roles(role)
            await logger.log("Nouveau Log Autorank ! (TAG)", {
                "Modérateur": f"<@{client.user.id}>",
                "Membre": f"{after.mention}",
                "Rôle donné": f"{role.mention}"
            }, f"Donné le {date_str} à {heure_str}")


@client.event
async def on_message(message):
    reply_msg = ""
    if not message.author.bot:
        channel_id = message.channel.id
        author = message.author
        shouldContinue = False
        autoRankSettig = {}
        print(settings["autorole"])
        try:
            autoRankSettig = settings["autorole"][str(channel_id)]
            shouldContinue = True
        except:
            pass
        
        if shouldContinue and message.content == autoRankSettig["message"]:
            for role in settings["bl-role"]:
                if message.guild.get_role(role) in author.roles:
                    return
            if autoRankSettig["tagName"]["required"]:
                if autoRankSettig["tagName"]["tag"] not in author.name:
                    print("doesnt have tag")
                    shouldContinue = False
            role = message.guild.get_role(autoRankSettig["roleid"])
            if role in author.roles:
                reply_msg = f"{author.mention}, vous avez déjà le rôle {role.name} !"
            else:
                await author.add_roles(role)
                reply_msg = f'{author.mention}, le rôle "{role.name}" vous a été donné avec succès !'

                await logger.log("Nouveau Log Autorank !", {
                    "Modérateur": f"<@{client.user.id}>",
                    "Membre": f"{author.mention}",
                    "Rôle donné": f"{role.mention}"
                }, f"Donné le {date_str} à {heure_str}")

                    
        if len(reply_msg) > 0: await message.channel.send(reply_msg)




client.run(settings["token"])
