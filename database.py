from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'accounting.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()