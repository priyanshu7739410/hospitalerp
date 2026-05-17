from sqlalchemy.orm import declarative_base

# Step 1: Create the Declarative Base
# The Base is essentially the "master blueprint".
# Every single table we create in our database (Patients, Doctors, Appointments, etc.)
# will inherit from this Base. 
# It acts like a registry, keeping track of all our models so SQLAlchemy knows how to convert our Python classes into PostgreSQL tables.
Base = declarative_base()
