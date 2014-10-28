import csv
import logging
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from pycds import Obs

log = logging.getLogger(__name__)

def process(data, sesh):
    successes, failures, skips = 0, 0, 0
    for row in data:
        t = datetime.strptime(row['obs_time'], '%Y-%m-%d %H:%M:%S')
        hist = int(row['history_id'])
        var = int(row['vars_id'])
        try:
            datum = float(row['datum'])
        except ValueError as e:
            if row['datum'] == 'NA':
                continue
            else:
                raise e
        o = Obs(time=t, datum=datum, history_id=hist, vars_id=var)
        log.debug(o)

        try:
            with sesh.begin_nested():
                sesh.add(o)
                successes += 1
                log.debug("Inserted {}".format(o))
        except IntegrityError as e:
            log.debug("Skipped, already exists: {} {}".format(o, e))
            skips += 1
        except:
            log.error("Failed to insert {}".format(o), exc_info=True)
            failures += 1

    return {'successes': successes, 'skips': skips, 'failures': failures}
