import psycopg2
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker #Run pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from tqdm import tqdm

def fetch_data(state, district, language, category):
    print("fetch_data called")
    """
    state = text(state)
    district = text(district)
    language = text(language)
    category = text(category)
    #print(type(text(state)), type(state))
    """
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
             """
             conn = psycopg2.connect(
                 host="localhost",
                 database="karya",
                 user="karya",
                 password="pg_karya",
                 port =str(server.local_bind_port)
             )"""
             local_port = str(server.local_bind_port)
             engine = create_engine('postgresql://karya:pg_karya@127.0.0.1:' + local_port +'/karya')

             Session = sessionmaker(bind=engine)
             session = Session()
        
             print('Database session created')
             #cur = conn.cursor()
             #test data retrieval
             temp = session.execute("SELECT id FROM task")
             print(temp)
             get_worker_command = f"select id from worker where profile is not null and profile::jsonb->>'primary_language' ='{language}' and profile->>'native_place_state' = '{state}' and profile->>'native_place_district' ='{district}' limit 2" 
             print(get_worker_command)
             worker_id = session.execute(get_worker_command).fetchall()
             task_id = session.execute(f"select id from task where itags::jsonb->'itags' ?& array['{language.lower()}','full-verification-ai4b']").fetchall()
             print(worker_id)
             print(task_id)
             results = []
             for w_id in worker_id:

                 for t_id in tqdm(task_id):
                    print(w_id, t_id)
                    recording_id = session.execute(text(f"select input::jsonb->'files'->>'recording',output::jsonb->'data' from microtask where task_id = '{t_id[0]}' and input::jsonb->'chain'->'workerId' = '{w_id[0]}' and output is not null and  (output::text like '%\"decision\":\"accept\"%' or  output::text like '%\"decision\":\"excellent\"%') limit 2;")).fetchall()
                    print(recording_id)
                    results.extend(recording_id)
            
             session.close()
             return results
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
