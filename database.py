from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sql_db_url='postgresql://postgres:admin123@localhost/fastapi'  # connect to sql alchemy

engine=create_engine(sql_db_url)  # establich the connection 

# taking to a database we need a session
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()  # we neeed to define this base class  , it is confusing - just things of copy & paste dont worry 


# Dependency
def get_db():
    db = SessionLocal() # session object is responsible to talk with databases
    try:
        yield db
    finally:
        db.close()