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
    parser.add_argument('-D', '--diagnostic', action="store_true", default = False,
                        help="Turn on diagnostic mode (no commits)")
    parser.add_argument('-b', '--batch_size',
                        help='Number of observations to insert with each batch',
                        default=250)
    parser.add_argument('-l', '--log_level', default = 'INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set log level: DEBUG, INFO, WARNING, ERROR, CRITICAL.')
    parser.add_argument('filelist', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s - %(message)s', level=args.log_level)

    log.info('Starting import')

    engine = create_engine(args.connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    log.info('Database connected')

    for line in fileinput.input(args.filelist):
        fp = line.strip()
        if not fp or fp.startswith('#'):
            continue
        log.info('Processing {}'.format(fp))
        with open(fp, 'rb') as f:
            data = csv.DictReader(f)
            r = bch.process(data, session, args.diagnostic, int(args.batch_size))
            log.info('Done file: {}'.format(r))

    session.commit()
    session.close()
    log.info('DONE')
