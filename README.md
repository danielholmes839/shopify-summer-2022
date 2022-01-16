# Backend Developer Intern Challenge

![badge](https://github.com/danielholmes839/shopify-summer-2022/actions/workflows/actions.yml/badge.svg)

Requirements
- [Shopify Backend Developer Intern Challenge - Summer 2022](https://docs.google.com/document/d/1z9LZ_kZBUbg-O2MhZVVSqTmvDko5IJWHtuFmIu_Xg1A/edit)
- Extra feature chosen: *Ability to assign/remove inventory items to a named group/collection*

## How to run/access the application

### Option #1: Access the deployed version on Amazon Web Services

https://shopify.holmes-dev.com/graphql or [backup endpoint](https://7d03f6hr17.execute-api.ca-central-1.amazonaws.com/graphql)

### Option #2: Run with Docker

```
docker build -f docker/Dockerfile -t shopify-challenge-image .
docker run -d --name shopify-challenge-container -p 8000:8000 shopify-challenge-image
```

### Option #3: Run with Python

1. Add a `.env` file to the root directory of the repository containing `CONTEXT=LOCAL`
2. Install dependencies from `requirements.txt` using `pip install -r requirements.txt`
3. Run the application `uvicorn main:app`

#### Other

Commands
```
pip install -r requirements.txt

uvicorn main:app
uvicorn main:app --reload

python -m pytest -v
python -m pytest --cov-report term-missing --cov=app.db app_tests/
```

Environment variable options

- `CONTEXT=AWS_PROD` ignores the `AWS_ACCESS_KEY` and `AWS_SECRET_ACCESS_KEY` variables since the Lambda function is given a role with permissions to access DynamoDB.

```
CONTEXT=AWS_DEV|AWS_PROD|LOCAL

AWS_REGION_NAME=ca-central-1
AWS_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXX
AWS_DYNAMODB_TABLE=table-name
```

Deployed using a servless architecture on AWS with API-Gateway, Lambda, and DynamoDB.

![architecture](./screenshots/aws.png)

![dynamodb](./screenshots/dynamodb.PNG)
