# Backend Developer Intern Challenge

![badge](https://github.com/danielholmes839/shopify-summer-2022/actions/workflows/actions.yml/badge.svg)


- GraphQL API
- Deployed on AWS
 
 ```
uvicorn main:app
uvicorn main:app --reload

python -m pytest -v
python -m pytest --cov-report term-missing --cov=app.db app_tests/
 ```

## Deployed on AWS

Deployed using a servless architecture on AWS with API-Gateway, Lambda, and DynamoDB.

![architecture](./screenshots/aws.png)

![dynamodb](./screenshots/dynamodb.PNG)

Environment variables
```
CONTEXT=AWS_DEV|AWS_PROD|LOCAL_DEV

AWS_REGION_NAME=ca-central-1
AWS_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXX
AWS_DYNAMODB_TABLE=table-name
```