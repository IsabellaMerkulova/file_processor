import logging
import random
import time
import uuid
from celery_app import app, process_file

logging.basicConfig(level=logging.DEBUG)


def create_file():
    lines = ''.join([
        f'{random.randint(1, 1000)} {random.randint(1000, 10000)}\n'
        for _ in range(random.randint(800000, 1000000))
    ])
    name = f'files/{int(time.time())}_{uuid.uuid4()}.csv'
    try:
        with open(name, 'w') as f:
            f.writelines(lines)
    except OSError:
        logging.exception('Cannot write to file')
        return

    process_file.delay(name)


if __name__ == '__main__':
    while 1:
        try:
            create_file()
        except Exception as ex:
            logging.exception(f'An error occurred in creating file: {ex}')
        time.sleep(10)
