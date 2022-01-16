import os
import discord
from dotenv import load_dotenv
from app.middleware import ContextExtension
from .contextmakers import AWSContextMaker, LocalContextMaker
from .alerters import EmptyAlerter, DiscordAlerter

load_dotenv()

DISCORD_ENABLED = os.environ['DISCORD_ENABLED']
CONTEXT = os.environ['CONTEXT']

extensions = []

if CONTEXT == 'AWS_PROD':
    # aws context maker without credentials
    # lambda function role grants credentials
    aws = AWSContextMaker()
    extensions.append(ContextExtension(aws))


elif CONTEXT == 'AWS_DEV':
    # aws context maker with credentials
    aws = AWSContextMaker(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    extensions.append(ContextExtension(aws))

elif CONTEXT == 'LOCAL':
    # local context maker
    local = LocalContextMaker()
    extensions.append(ContextExtension(local))


alerter = EmptyAlerter()

if DISCORD_ENABLED:
    intents = discord.Intents.default()
    intents.members = True

    token = os.environ['DISCORD_TOKEN']
    channel_id = int(os.environ['DISCORD_CHANNEL'])

    alerter = DiscordAlerter(
        intents=intents,
        token=token,
        channel_id=channel_id,
        context=CONTEXT,
    )
