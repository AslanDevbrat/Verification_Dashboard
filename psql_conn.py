import psycopg2
# from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import sessionmaker #Run pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from tqdm import tqdm
# from joblib import Parallel, delayed
from itertools import product

def fetch_data(state, district, language, category,date_category, start_date, end_date):
    print("fetch_data called")
    try:

        # with SSHTunnelForwarder(
        #      ('ai4bdmukaryaserver.eastus2.cloudapp.azure.com', 22),
        #      #ssh_private_key="</path/to/private/ssh/key>",
        #      ### in my case, I used a password instead of a private key
        #      ssh_username="karya",
        #      ssh_password="karya@ai4bharat", 
        #      remote_bind_address=('localhost', 5432)) as server:

        #      server.start()
        #      print("server connected")
        #      local_port = str(server.local_bind_port)

        # engine = create_engine('postgresql://karya:pg_karya@127.0.0.1:' + '5433' +'/karya')
        conn = psycopg2.connect(database = 'karya', user = 'karya', password = 'pg_karya', host = '127.0.0.1', port = '5432')
        # Session = sessionmaker(bind=engine)
        # global session
        # session = Session()

        cur = conn.cursor()
        print('Database session created')
        #cur = conn.cursor()
        #test data retrieval
        #  temp = session.execute("SELECT id FROM task")
        #print(temp)
        get_worker_command = f"select id from worker where profile is not null and profile::jsonb->>'primary_language' ='{language}' and profile->>'native_place_state' = '{state}' and profile->>'native_place_district' ='{district}' " 
        #print(get_worker_command)
        cur.execute(get_worker_command)
        worker_id = cur.fetchall()
        if len(worker_id) == 0:
            return []
        cur.execute(f"select id from task where itags::jsonb->'itags' ?& array['{language.lower()}','full-verification-ai4b','read'] or itags::jsonb->'itags' ?& array['{language.lower()}','full-verification-ai4b','extempore']")
        task_id = cur.fetchall()
        if len(task_id) == 0:
            return []
        #print(worker_id)
        #print(task_id)
        #cartesion = list(product([session],worker_id,task_id))
        #print(cartesion)

        #return res
        results = []
        def fetch_audio(w_id,category,t_id, date_category, start_date, end_date):
            if category == "Accept":
                q_category = "(microtask.output::text like '%\"decision\":\"excellent\"%')" 
            elif category == "Borderline Accept":
                q_category = "(microtask.output::text like '%\"decision\":\"accept\"%')" 
            elif category == "Reject":
                q_category = "(microtask.output::text like '%\"decision\":\"reject\"%')"
            else:
                q_category = "microtask.output is not null"
            if date_category == "Completed Between":
                #print('completed between')
                temp_date_q = "microtask.input::jsonb->'chain'->>'assignmentId' = microtask_assignment.id::text"
                completed = f'and created_at >= \'{start_date}\' and created_at<=\'{end_date}\''
                verified = ''
            else:
                #print("verified between")
                temp_date_q = "microtask.id = microtask_assignment.microtask_id"
                verified = f'and microtask_assignment.completed_at>=\'{start_date}\' and microtask_assignment.completed_at<=\'{end_date}\''
                completed = ''
                

            #print(category,q_category, w_id)
            temp_t_id = tuple([str(x[0]) for x in t_id])
            temp_w_id = tuple([str(x[0]) for x in w_id])
            # print(temp_t_id)
            # print(temp_w_id)
            # print(start_date,end_date)
            final_query = f"select microtask.input::jsonb->'files'->>'recording', microtask.output::jsonb->'data', microtask.input::jsonb->'data'->>'sentence' from microtask,microtask_assignment where {temp_date_q} and  microtask.task_id in {temp_t_id} and microtask.input::jsonb->'chain'->'workerId' in {temp_w_id} and microtask.output is not null and {q_category} and date(completed_at)>='{start_date}' and date(completed_at)<='{end_date}';"
            cur.execute(final_query)

            # print(final_query)
            read_and_extempore = cur.fetchall()
            
            cur.execute(f"select id from task where itags::jsonb->'itags' ?& array['{language.lower()}','full-verification-ai4b','conversations']")
            conversations_task = cur.fetchall()
            assert len(conversations_task) == 1
            conversations = conversations_task[0][0]


            query = f'''
            select microtask.input::jsonb->'files'->>'recording', microtask.output::jsonb->'data', microtask.input::jsonb->'data'->>'sentence' 
            from microtask,microtask_assignment 
            where microtask.task_id in ('{conversations}') and {q_category} and
                microtask.id = microtask_assignment.microtask_id and 
                microtask.output is not null and 
                microtask.input::jsonb->'files'->>'recording' in 
                    (select conversation.id||'.wav' from conversation 
                    where (sp1 in (select phone_number from worker where id in {temp_w_id}) or sp2 in (select phone_number from worker where id in {temp_w_id})) 
                    {completed}) 
                    {verified};
            '''
            #print(query)
            cur.execute(query)
            conv = cur.fetchall()
            # print(conv)
            return read_and_extempore + conv
        return fetch_audio(worker_id,category, task_id, date_category, start_date, end_date)
    except Exception as e:
        print("Connection Failed", e)
if __name__ == "__main__":
    fetch_data("West Bengal", "Birbhum", "Bengali", "accept")
    #get_database_connection()
