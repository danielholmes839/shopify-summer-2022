import discord
from datetime import datetime


class EmptyAlerter:
    def start():
        pass

    def alert():
        pass


class DiscordAlerter(discord.Client):
    def __init__(self, *args, channel_id=None, token=None, context=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        self.token = token
        self.context = context

    async def on_ready(self):
        """ on ready send a startup message"""
        dt = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        await self.alert(f'`startup {self.context}: {dt}`')

    async def alert(self, message: str):
        await self.wait_until_ready()
        channel = self.get_channel(self.channel_id)
        await channel.send(message)

    async def start(self):
        await super().start(self.token)
