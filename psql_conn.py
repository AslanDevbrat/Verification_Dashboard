import psycopg2
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker #Run pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from tqdm import tqdm
from joblib import Parallel, delayed
from itertools import product

def get_database_connection():
    server = SSHTunnelForwarder(
             ('ai4bdmukaryaserver.eastus2.cloudapp.azure.com', 22),
             #ssh_private_key="</path/to/private/ssh/key>",
             ### in my case, I used a password instead of a private key
             ssh_username="karya",
             ssh_password="karya@ai4bharat", 
             remote_bind_address=('localhost', 5432))
    server.start()
    local_port = str(server.local_bind_port)
    engine = create_engine('postgresql://karya:pg_karya@127.0.0.1:' + local_port +'/karya')

    Session = sessionmaker(bind=engine)
    session = Session()

    print('Database session created')
    return session

def fetch_audio(t_id):
    return session.execute(text(f"select input::jsonb->'files'->>'recording',output::jsonb->'data' from microtask where task_id = '{t_id[0]}' and input::jsonb->'chain'->'workerId' = '{w_id[0]}' and output is not null and  (output::text like '%\"decision\":\"accept\"%' or  output::text like '%\"decision\":\"excellent\"%');")).fetchall()
def fetch_data(state, district, language, category, offset):
    if offset == None:
        offset = 0
    else:
        offset = int(offset)
    print("fetch_data called")
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
             global session
             session = Session()
             

             print('Database session created')
             #cur = conn.cursor()
             #test data retrieval
             temp = session.execute("SELECT id FROM task")
             #print(temp)
             get_worker_command = f"select id from worker where profile is not null and profile::jsonb->>'primary_language' ='{language}' and profile->>'native_place_state' = '{state}' and profile->>'native_place_district' ='{district}' OFFSET {offset*5} ROWS FETCH FIRST 5 ROW ONLY;" 
             #print(get_worker_command)
             worker_id = session.execute(get_worker_command).fetchall()
             task_id = session.execute(f"select id from task where itags::jsonb->'itags' ?& array['{language.lower()}','full-verification-ai4b']").fetchall()
             #print(worker_id)
             #print(task_id)
             #cartesion = list(product([session],worker_id,task_id))
             #print(cartesion)

             #return res
             results = []
             for w in tqdm(worker_id):

                 global  w_id
                 w_id = w
                
                 res = Parallel(n_jobs = -1,prefer="threads")(delayed(fetch_audio)(t_id) for t_id in task_id)
                 #print("res")
                 for r in res:
                     if len(r)!=0:
                         results.extend(r)
                 #print("res")
                 #if len(res)!=0:
                    #results.extend(res)
             #print(results)
             session.close()
             return results, offset + 1
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
if __name__ == "__main__":
    fetch_data("West Bengal", "Birbhum", "Bengali", "accept")
    #get_database_connection()
