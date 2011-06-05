#imports
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String


engine = create_engine('sqlite:////tmp/sqltest.db', echo=True) #creates the database

metadata = MetaData(bind=engine)                             #provides metadata for the engine created.

users_table = Table('users', metadata,                       #table name users having id name age and password
                    Column('id', Integer, primary_key=True),
                    Column('name', String(40)),
                    Column('age', Integer),
                    Column('password', String),
                    )

addresses_table = Table('address', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user_id',None, ForeignKey('users.id')),
                        Column('email_addresses', String, nullable=False)
                        )

metadata.create_all()
#creates the tables, creates only new tables, if the table already exists it won't create a new one.

#insertions
#creating insertion object

ins = users_table.insert()

#add values
new_user = ins.values(name ="Joe", age=20, password="pass")

#create a database connection
conn = engine.connect()

#add new user to database executing SQL
conn.execute(new_user)

