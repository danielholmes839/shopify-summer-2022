# Backend Developer Intern Challenge

![badge](https://github.com/danielholmes839/shopify-summer-2022/actions/workflows/actions.yml/badge.svg)

## TLDR

- Requirements: [Shopify Backend Developer Intern Challenge - Summer 2022](https://docs.google.com/document/d/1z9LZ_kZBUbg-O2MhZVVSqTmvDko5IJWHtuFmIu_Xg1A/edit)
- Extra feature chosen: *Ability to assign/remove inventory items to a named group/collection*
- The application is deployed to AWS: 

## Amazon Web Services

The application is deployed using an entirely servless architecture on AWS with API-Gateway, Lambda, and DynamoDB.

![architecture](./documentation/screenshots/aws.png)

The data is stored on DynamoDB with the following data model:

![dynamodb](./documentation/screenshots/dynamodb.PNG)
