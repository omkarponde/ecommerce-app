# E-Commerce Microservices Backend with FastAPI, SQLAlchemy, PostgreSQL, and Docker

## Overview

This project is a set of microservices for an E-Commerce backend, built using FastAPI, SQLAlchemy, PostgreSQL, and Docker. Each microservice focuses on a specific aspect of E-Commerce functionality, including authentication, product management, and order management. The microservices architecture allows for scalability, modularity, and independent deployment of each service. Docker containers encapsulate each microservice, providing consistency and portability across different environments.

## Features

- 🛠 **Microservices Architecture**: Consists of separate microservices for authentication, product management, and order management.
- 🚀 **FastAPI**: Utilizes the FastAPI framework for building high-performance asynchronous APIs.
- 🗃 **SQLAlchemy**: Integrates SQLAlchemy ORM for easy database management and querying.
- 🐳 **Dockerization**: Docker containers encapsulate each microservice for easy deployment and scalability.
- 📦 **PostgreSQL**: Uses PostgreSQL as the backend database for reliable and scalable data storage.
- 🔒 **User Authentication**: Handles user authentication using JWT tokens.
- 🔑 **Authorization**: Implements authorization using JWT tokens and FastAPI's built-in dependency injection.
- 📝 **Product Management**: Supports CRUD operations for managing products.
- 📦 **Order Management**: Enables creation, updating, and tracking of orders.
- 🌐 **RESTful API**: Follows RESTful principles for clear and standardized API endpoints.
- ⚙️ **Concurrency Control**: Utilizes pessimistic locking for ensuring data integrity and preventing race conditions in order creation.

## Authentication and Authorization

- 🔐 **JWT Tokens**: Authentication is handled using JWT tokens.
- 🛡️ **fastapi_auth_jwt**: Utilizes the `fastapi_auth_jwt` library for authentication and authorization.

  
## Role-Based Permissions

- 🛡️ **Admin**:
  - Can see all products.
  - Can see all orders.
  - Can delete a product.

- 🛍️ **Seller**:
  - Can post a product.
  - Can view only its own products.
  - Can update own product.

- 🧑‍🤝‍🧑 **Buyer**:
  - Can order a product.
  - Can see all products.
  - Can see only own orders.

## Product Microservice

- 📦 **Create Product**:
  - Only Seller roles can create new products.
  
- 🔄 **Update Product**:
  - Seller can update its own existing products.
  
- 👁️ **Read Product**:
  - All roles can read all products.

## Order Microservice

- 📦 **Create Order**:
  - Only Buyer roles can create new orders.
  
- 👁️ **Read Order**:
  - Buyer can see only its own orders.
  - Admin can view all orders.

