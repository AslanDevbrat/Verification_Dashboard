import psycopg2
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker #Run pip install sqlalchemy
from sqlalchemy import create_engine
try:

    with SSHTunnelForwarder(
         ('ai4bdmukaryaserver.eastus2.cloudapp.azure.com', 22),
         #ssh_private_key="</path/to/private/ssh/key>",
         ### in my case, I used a password instead of a private key
         ssh_username="karya",
         ssh_password="karya@ai4bharat", 
         remote_bind_address=('localhost', 5432)) as server:
         
         server.start()
         print("server connected")
         
         local_port = str(server.local_bind_port)
         engine = create_engine('postgresql://karya:pg_karya@127.0.0.1:' + local_port +'/karya')

         Session = sessionmaker(bind=engine)
         session = Session()
    
         print('Database session created')
    
         #test data retrieval
         test = session.execute("SELECT * FROM yesterday_sample limit 5")
         print(test)
         for row in test:
             print(row)
         session.close()
         """
         params = {
             'database': 'karya',
             'user': 'karya',
             'password': 'pg_karya',
             'host': 'localhost',
             'port': server.local_bind_port
             }

         conn = psycopg2.connect(**params)
         curs = conn.cursor()
         print("database connected")
         print(curs.execute("SELECT * FROM yesterday_sample where id=281474976952260"))
         """

except Exception as e:
    print("Connection Failed", e)
