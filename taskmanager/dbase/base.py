from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from .model import Base
dbase = 'sqlite:///main.db'
engine = create_engine(dbase, echo=True)
inspector = inspect(engine)
print(inspector.get_table_names())
Session = sessionmaker(bind=engine)
def create_tables():
    Base.metadata.create_all(bind=engine)