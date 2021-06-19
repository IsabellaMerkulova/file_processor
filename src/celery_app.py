from celery import Celery
import os
import logging
import psycopg2

logging.basicConfig(level=logging.DEBUG)

app = Celery(broker=os.environ.get('BROKER_URL'))
db_uri = 'postgresql://postgres:123@postgres:5432/project_db'


@app.task(bind=True, max_retries=3)
def process_file(self, name):
    try:
        with psycopg2.connect(db_uri) as conn:
            with conn.cursor() as cursor:
                with open(name, 'r') as f:
                    cursor.copy_from(
                        f,
                        'users_resource_stats',
                        sep=' ',
                        columns=['user_id', 'resource_used']
                    )
    except Exception as ex:
        logging.exception(ex)
        self.retry(countdown=3 ** self.request.retries)
