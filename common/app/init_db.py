from app.db import engine, Base
from app.models import User, Role, Order, order_product_association, Product, Cart, CartItem, Shipment, Payment
from sqlalchemy.orm import sessionmaker
# Define schema names
schemas = ['user_schema', 'product_schema', 'order_schema', 'cart_schema', 'shipment_schema', 'payment_schema']

# Create schemas in the database
for schema_name in schemas:
    with engine.connect() as conn:
        conn.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name}')

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Define the predefined roles
roles = ['admin', 'seller', 'buyer', 'guest']

# Insert the predefined roles into the database
for role_name in roles:
    role = Role(name=role_name)
    session.add(role)

# Commit the changes to the database
session.commit()

# Close the session
session.close()
