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


## 🛠️ Setup Guide

### Step 1: Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/omkarponde/ecommerce-app.git
```

### Step 2: Configure Environment Variables

Create a `.env` file in the root directory of the project and add the necessary environment variables. Below is an example `.env` file:

```dotenv
# Example .env file

POSTGRES_DB=postgres
POSTGRES_USER=my_database_user
POSTGRES_PASSWORD=my_database_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Replace `my_database_user`, `my_database_password`, etc., with your actual PostgreSQL database credentials.
### Step 3: Start Docker Containers
Navigate to the project directory and start the Docker containers using the following commands:

```bash
cd ecommerce-app
```
Initialize the database. The following command creates the tables as per the models defined in the common directory:`
```bash
make init_db
```
Start the Authentication service:
```bash
make dev_up SERVICE_NAME=authentication
```
Start the Product service:
```bash
make dev_up SERVICE_NAME=product
```
Start the Order service:
```bash
make dev_up SERVICE_NAME=order
```
To see the logs of the commands run, replace service_name with authentication, order, or product, depending on which logs you want to see:
```bash
make logs SERVICE_NAME=service_name
```
