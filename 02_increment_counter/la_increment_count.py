#!/usr/bin/env python

import logging

import la_increment_lib


def lambda_handler(event, context):
    logging.warning("DEBUG: {r}".format(r=repr(event)))
    try:
        CountName = la_increment_lib.parse_event(event, "POST")
        if 'CountName' is None:
            return la_increment_lib.make_return("event must specify CountName", 400)
        logging.warning("CountName is {r}".format(r=repr(CountName)))
        ddb, tables = la_increment_lib.ddb_connect()
        count_exists, count_value = la_increment_lib.conditional_get_count(CountName, tables)
        if count_exists is True:
            count_value['count'] = count_value['count'] + 1
        else:
            count_value = {'count': 1}
        la_increment_lib.set_count(CountName, count_value, tables)
        return la_increment_lib.make_return("count is {c}".format(c=count_value['count']), 200)
    except:
        logging.exception("Caught unknown error")
        return la_increment_lib.make_return("unknown error", 400)