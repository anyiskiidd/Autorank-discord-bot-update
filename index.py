import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

ROLE_ID = ##id du role
CHANNEL_ID = ##id du channel dans lequel vous voulez que le bot sois mentionné
LOG_CHANNEL_ID = ##id dans lequel vous voulez que les logs appraisses


@client.event
async def on_ready():
    print("Bot prêt")


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
        if "211" in member.name or "²¹¹" in member.name:
            if message.channel.id == CHANNEL_ID and not ("@everyone" in message.content or "@here" in message.content):
                role = message.guild.get_role(1086755223525130281) # Récupère le rôle avec l'ID "1086755223525130281"
                if role is not None:
                    await member.add_roles(role)
                    reply_msg = f'{member.mention}, Le rôle "{role.name}" vous a été donné avec succès !'
                    print(reply_msg)
                    
                    log_embed = discord.Embed(title=f"Nouveau Log Autorank !", color=discord.Color.from_rgb(25, 25, 25))
                    log_embed.add_field(name="Modérateur", value=f"<@(id de votre bot)>")
                    log_embed.add_field(name="Membre", value=f"{member.mention}")
                    log_embed.add_field(name="Rôle donné", value=f"{role.mention}")
                    log_embed.set_footer(text=f"Donné le {datetime.utcnow().strftime('à %Y-%m-%d %H:%M:%S')}")
                    
                    log_channel = client.get_channel(LOG_CHANNEL_ID)
                    if log_channel is not None:
                        await log_channel.send(embed=log_embed)
                else:
                    reply_msg = f"Une erreur est survenue, veuillez contacter un admin !"
            else:
                reply_msg = f"{member.mention}, vous devez mentionner le bot dans le canal {client.get_channel(CHANNEL_ID).mention} pour recevoir le rôle !"
        else:
            role = message.guild.get_role(ROLE_ID)
            if role is not None and role in member.roles:
                await member.remove_roles(role)
                reply_msg = f"{member.mention}, Vous avez perdu le rôle {role.name} car vous n'avez plus le tag !"
                print(reply_msg)
            else:
                reply_msg = f"{member.mention}, Vous devez avoir le tag pour obtenir le rôle !"

        bot_message = await message.channel.send(reply_msg)
        
    await client.process_commands(message)


client.run('token')
