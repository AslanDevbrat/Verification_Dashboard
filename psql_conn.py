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

def fetch_audio(w_id,category,t_id, date_category, start_date, end_date):
    if category == "Accepted":
        q_category = "(microtask.output::text like '%\"decision\":\"accept\"%' or  microtask.output::text like '%\"decision\":\"excellent\"%')" 
    else:
        q_category = "(microtask.output::text not like '%\"decision\":\"accept\"%' and  microtask.output::text not like '%\"decision\":\"excellent\"%')"
    if date_category != "Completed Between":
        temp_date_q = "microtask.input::jsonb->'chain'->>'assignmentId' = microtask_assignment.id::text"
    else:
        temp_date_q = "microtask.id = microtask_assignment.microtask_id"
    print(category,q_category, w_id)
    temp_t_id = tuple([str(x[0]) for x in t_id])
    temp_w_id = tuple([str(x[0]) for x in w_id])
    print(temp_t_id)
    print(temp_w_id)
    final_query = text(f"select microtask.input::jsonb->'files'->>'recording', microtask.output::jsonb->'data' from microtask,microtask_assignment where {temp_date_q} and  microtask.task_id in {temp_t_id} and microtask.input::jsonb->'chain'->'workerId' in {temp_w_id} and microtask.output is not null and {q_category} and date(completed_at)>='{start_date}' and date(completed_at)<='{end_date}';")

    return session.execute(final_query).fetchall()



def fetch_data(state, district, language, category,date_category, start_date, end_date):
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
             get_worker_command = f"select id from worker where profile is not null and profile::jsonb->>'primary_language' ='{language}' and profile->>'native_place_state' = '{state}' and profile->>'native_place_district' ='{district}' " 
             #print(get_worker_command)
             worker_id = session.execute(get_worker_command).fetchall()
             if len(worker_id) == 0:
                return []
             task_id = session.execute(f"select id from task where itags::jsonb->'itags' ?& array['{language.lower()}','full-verification-ai4b']").fetchall()
             if len(task_id) == 0:
                 return []
             print(worker_id)
             print(task_id)
             #cartesion = list(product([session],worker_id,task_id))
             #print(cartesion)

             #return res
             results = []
             return fetch_audio(worker_id,category, task_id, date_category, start_date, end_date)
             for w in tqdm(worker_id):

                 #global  w_id
                 #w_id = w

                 res = Parallel(n_jobs = -1,prefer="threads")(delayed(fetch_audio)(w,category, t_id) for t_id in task_id)
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
