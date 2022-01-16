# Backend Developer Intern Challenge

![badge](https://github.com/danielholmes839/shopify-summer-2022/actions/workflows/actions.yml/badge.svg)

## TLDR

- Requirements: [Shopify Backend Developer Intern Challenge - Summer 2022](https://docs.google.com/document/d/1z9LZ_kZBUbg-O2MhZVVSqTmvDko5IJWHtuFmIu_Xg1A/edit)
- Extra feature chosen: *Ability to assign/remove inventory items to a named group/collection*
- Open [shopify.holmes-dev.com](https://shopify.holmes-dev.com) to run the application

## GraphQL API 

I decided to build the application as a GraphQL API. The GraphQL API allows users to perform CRUD operations on items.

- Create: `itemCreate` mutation
- Read: `item`, `items` and `itemsByCollection` queries
- Update: `itemUpdate`, `itemUpdateCollection`, and `itemUpdateStock` mutations
- Delete: `itemDelete` mutation

test

- The `Item` `collection` field is nullable. If the collection is `null` that means the item does not belong to a collection. Therefore the `itemUpdateCollection` mutation and `itemsByCollection` query allow the collection to be null as well.
- The `Item` has a `product` field. In a full application the prudct would be an actual `Product` type instead of a string
- There are 3 mutations for updating items: `itemUpdate`, `itemUpdateCollection` and `itemUpdateStock`. The `itemUpdate` is general and can be used to update any field. However I thought adding the `itemUpdateCollection` and `itemUpdateStock` would be convenient to use as well.
- I didn't add any pagination for `items` or `itemsByCollection` but that would have been cool

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
