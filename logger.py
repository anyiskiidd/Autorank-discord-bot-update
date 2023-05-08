import discord
from datetime import datetime

class Logger:
    def __init__(self, client, settings):
        self.client = client
        self.settings = settings
        self.color = discord.Color.from_rgb(settings["color"][0], settings["color"][1], settings["color"][2])
        self.log_channel = client.get_channel(settings["logChannel"])
        self.date_str = datetime.now().strftime("%d/%m/%Y")
        self.heure_str = datetime.now().strftime("%H:%M:%S")

    async def log(self, title, fields, footer):
        log_embed = discord.Embed(title=title, color=self.color)
        for name, value in fields.items():
            log_embed.add_field(name=name, value=value)
        log_embed.set_footer(text=footer)
        try:
            if self.log_channel is None:
                self.log_channel = self.client.get_channel(self.settings["logChannel"])
            await self.log_channel.send(embed=log_embed)
        except Exception as e:
            print(e)
            print("Impossible d'envoyer le log dans le channel de logs.")

