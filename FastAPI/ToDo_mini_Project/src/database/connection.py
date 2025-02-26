from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# register
DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

# for connection
engine = create_engine(DATABASE_URL, echo=True) # re-print sql query
SessionFactory = sessionmaker(autocommit=False, autoflush=False,bind=engine)