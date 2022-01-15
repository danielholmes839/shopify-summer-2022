import os
from dotenv import load_dotenv
from app.middleware import ContextExtension
from .contextmakers import AWSContextMaker, LocalContextMaker

load_dotenv()


context = os.environ['CONTEXT']
extensions = []

if context == 'AWS_PROD':
    # aws context maker without credentials 
    # lambda function role grants credentials
    aws = AWSContextMaker()
    extensions.append(ContextExtension(aws))


elif context == 'AWS_DEV':
    # aws context maker with credentials
    aws = AWSContextMaker(
        aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )

    extensions.append(ContextExtension(aws))

elif context == 'LOCAL':
    # local context maker
    local = LocalContextMaker()
    extensions.append(ContextExtension(local))