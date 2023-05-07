import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

ROLE_ID = 1234567890  
CHANNEL_ID = 1234567890  
LOG_CHANNEL_ID = 1234567890  
BL_ROLE_ID = 1234567890  

@client.event
async def on_ready():
    print("""
 ____        _     _____          _     _
|  _ \      | |   |  __ \        | |   | |
| |_) | ___ | |_  | |__) | __ ___| |_  | |
|  _ < / _ \| __| |  ___/ '__/ _ \ __| | |
| |_) | (_) | |_  | |   | | |  __/ |_  |_|
|____/ \___/ \__| |_|   |_|  \___|\__| (_)
    """)

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
                bl_role = message.guild.get_role(BL_ROLE_ID)
                role = message.guild.get_role(ROLE_ID)
                if role is not None:
                    if bl_role in member.roles:
                        reply_msg = f"{member.mention}, je ne peux pas vous donner le rôle {role.name} car vous avez le rôle {bl_role.name} !"
                    elif role in member.roles:
                        reply_msg = f"{member.mention}, vous avez déjà le rôle {role.name} !"
                    else:
                        await member.add_roles(role)
                        reply_msg = f'{member.mention}, le rôle "{role.name}" vous a été donné avec succès !'

                        log_embed = discord.Embed(title="Nouveau Log Autorank !", color=discord.Color.from_rgb(25, 25, 25))
                        log_embed.add_field(name="Modérateur", value="<@BOT_ID>")
                        log_embed.add_field(name="Membre", value=f"{member.mention}")
                        log_embed.add_field(name="Rôle donné", value=f"{role.mention}")
                        log_embed.set_footer(text=f"Donné le {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")

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

client.run('token')

