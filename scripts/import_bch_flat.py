import os
import csv
import logging
import fileinput
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gulpy import bch

log = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--connection_string', required=True,
                        help='PostgreSQL connection string of form:\n\tdialect+driver://username:password@host:port/database\nExamples:\n\tpostgresql://scott:tiger@localhost/mydatabase\n\tpostgresql+psycopg2://scott:tiger@localhost/mydatabase\n\tpostgresql+pg8000://scott:tiger@localhost/mydatabase')
    parser.add_argument('-D', '--diag', action="store_true", default = False,
                        help="Turn on diagnostic mode (no commits)")
    parser.add_argument('--log_level', default = 'INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set log level: DEBUG, INFO, WARNING, ERROR, CRITICAL.')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s - %(message)s', level=args.log_level)

    log.info('Starting import')

    engine = create_engine(args.connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    log.info('Database connected')

    for line in fileinput.input(args.args):
        fp = line.strip()
        if not fp or fp.startswith('#'):
            continue
        with open(fp, 'rb') as f:
            data = csv.DictReader(f)
            r = bch.process(data, session)
            log.info(os.path.basename(fp), extra=r)
    if args.diag:
        log.info('Diagnostic mode, rolling back')
        session.rollback()
    else:
        log.info('Committing the session')
        session.commit()

    log.info('DONE')
