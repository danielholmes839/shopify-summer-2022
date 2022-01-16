# Backend Developer Intern Challenge

![badge](https://github.com/danielholmes839/shopify-summer-2022/actions/workflows/actions.yml/badge.svg)

## TLDR

- Requirements: [Shopify Backend Developer Intern Challenge - Summer 2022](https://docs.google.com/document/d/1z9LZ_kZBUbg-O2MhZVVSqTmvDko5IJWHtuFmIu_Xg1A/edit)
- Extra feature chosen: *Ability to assign/remove inventory items to a named group/collection*
- How to run: open [shopify.holmes-dev.com](https://shopify.holmes-dev.com)

## GraphQL API 

I decided to build the application as a GraphQL API. GraphQL is one of my favourite technologies and I know it's used heavily at Shopify. The GraphQL API allows users to perform CRUD ooperations on items. 

```graphql
scalar DateTime # YYYY-MM-DDTHH:MM:SSZ

type Item {
    id: ID!
    product: String!        
    cost: Float!            # unit cost of the inventory is indepedent of cost 
    stock: Int!             # units available
    collection: String
    createdAt: DateTime!
    updatedAt: DateTime!
}

type ItemPayload {
    error: String
    item: Item
}

input ItemInput {
    product: String!
    cost: Float!
    stock: Int!
    collection: String
}

type Mutation {
    itemCreate(input: ItemInput!): ItemPayload!
    itemUpdate(id: ID!, input: ItemInput!): ItemPayload!
    itemUpdateCollection(id: ID!, collection: String): ItemPayload!
    itemUpdateStock(id: ID!, change: Int!): ItemPayload!
    itemDelete(id: ID!): ItemPayload!
}

type Query {
    item(id: ID!): Item 
    items: [Item!]!
    itemsByCollection(collection: String): [Item!]!
}
```

## Amazon Web Services

The application is deployed using an entirely servless architecture on AWS with API-Gateway, Lambda, and DynamoDB.

![architecture](./documentation/screenshots/aws.png)

The data is stored on DynamoDB with the following data model:

![dynamodb](./documentation/screenshots/dynamodb.PNG)
