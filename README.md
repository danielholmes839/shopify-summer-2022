# Backend Developer Intern Challenge

![badge](https://github.com/danielholmes839/shopify-summer-2022/actions/workflows/actions.yml/badge.svg)


- GraphQL API
- Deployed on AWS
 
 ```
uvicorn main:app
uvicorn main:app --reload

python -m pytest -v
python -m pytest --cov-report term-missing --cov=db tests/
 ```

# Deployed on AWS

- Entirely serverless using API-Gateway, Lambda, and DynamoDB

![architecture](./screenshots/aws.png)