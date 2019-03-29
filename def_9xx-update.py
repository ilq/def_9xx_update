# -*- coding: utf-8 -*-

import sys
import urllib2
import csv
import json
import MySQLdb
import os
import logging
from collections import namedtuple

URL_DEF_9XX = 'https://rossvyaz.ru/data/DEF-9xx.csv'
REGION = 'Кировская обл.'
MYSQL_CONFIG = 'mysql_config.json'
GATEWAY = 'goip1#goip3#goip4#addpack#nsgate'

Def_9xx_NamedTuple = namedtuple('Def_9xx_NamedTuple', 'prefix_start prefix_end operator region')

curdir = os.path.abspath(os.path.dirname(sys.argv[0]))
logging.basicConfig(format=u"%(levelname)-8s [%(asctime)s] %(message)s",
                    level=logging.INFO,
                    datefmt='%m/%d/%Y %H:%M:%S',
                    filename="%s/log_def_9xx_update.log" % curdir)

def get_def_9xx(url):
    try:
        response = urllib2.urlopen(url)
    except Exception, e:
        logging.error(URL_DEF_9XX + ': ' + str(e))
        logging.info('Stop script')
        sys.exit()
    def_9xx_csv = csv.reader(response, delimiter=';')
    return def_9xx_csv


def parse_def_9xx(def_9xx_csv):
    def_9xx_list_namedtuple = []
    replace_strings = [
        'ООО "',
        'ПАО "',
        'ЗАО "',
        'ОАО "',
        'АО "',
        '"']
    for item in def_9xx_csv:
        operator = item[4]
        for string in replace_strings:
            operator = operator.replace(string, '')
        item_def_9xx_namedtuple = Def_9xx_NamedTuple(
            item[0]+item[1],
            item[0]+item[2],
            operator,
            item[5])
        def_9xx_list_namedtuple.append(item_def_9xx_namedtuple)
    return def_9xx_list_namedtuple


def get_region(def_9xx_list_namedtuple, region):
    region_def_9xx = []
    for item in def_9xx_list_namedtuple:
        if item.region == region:
            region_def_9xx.append(item)
    return region_def_9xx


def get_mysql_config(filename_mysql_config):
    MysqlConfig = namedtuple('MysqlConfig', 'server user password database table')
    with open(filename_mysql_config) as f:
        json_mysql_config = json.loads(f.read())
        return MysqlConfig(**json_mysql_config)


def get_db(mysql_config):
    db = MySQLdb.connect(
            host=mysql_config.server,
            user=mysql_config.user,
            passwd=mysql_config.password,
            db=mysql_config.database,
            use_unicode=True,
            charset="utf8")
    return db


def get_current_def_9xx(cursor, table):
    query = "SELECT num1, num2, operator, operator FROM %s where priority is NULL;" % table
    cursor.execute(query)
    result = cursor.fetchall()
    current_def_9xx = []
    for item in result:
        current_def_9xx.append(Def_9xx_NamedTuple(*item))
    return current_def_9xx


def diff_def_9xx(first_def_9xx, second_def_9xx, fields):
    new_items = []
    old_items = []
    for first_item in first_def_9xx:
        for second_item in second_def_9xx:
            if first_item.prefix_start == second_item.prefix_start and \
                first_item.prefix_end == second_item.prefix_end:
                break
        else:
            new_items.append(first_item)
    for second_item in second_def_9xx:
        for first_item in first_def_9xx:
            if first_item.prefix_start == second_item.prefix_start and \
                first_item.prefix_end == second_item.prefix_end:
                break
        else:
            old_items.append(second_item)
    return [new_items, old_items]


def delete_old_def_9xx(old_def_9xx, cursor, table):
    for item in old_def_9xx:
        query = 'DELETE FROM %s where num1="%s";' % (table, item.prefix_start)
        logging.warning(query)
        cursor.execute(query)


def insert_new_def_9xx(new_def_9xx, cursor, table):
    for item in new_def_9xx:
        operator = item.operator
        operator = operator.decode('utf-8')
        query = 'INSERT INTO %s (num1, num2, operator, gateway) ' \
                 'VALUES ("%s", "%s", "%s", "%s");' % \
                 (table, item.prefix_start, item.prefix_end, operator, GATEWAY)
        logging.warning(query)
        cursor.execute(query)
    pass


def main():
    logging.info('Start script')
    def_9xx_csv = get_def_9xx(URL_DEF_9XX)
    def_9xx_list_namedtuple = parse_def_9xx(def_9xx_csv)
    if not def_9xx_list_namedtuple:
        logging.warning('NOT GET def_9xx from rossvyaz!')
        sys.exit()
    region_def_9xx = get_region(def_9xx_list_namedtuple, REGION)
    filename_mysql_config = MYSQL_CONFIG
    mysql_config = get_mysql_config(filename_mysql_config)
    db = get_db(mysql_config)
    current_def_9xx = get_current_def_9xx(db.cursor(), mysql_config.table)
    new_def_9xx, old_def_9xx = diff_def_9xx(region_def_9xx, current_def_9xx, ['prefix_start', 'prefix_end'])
    if old_def_9xx:
        logging.info('OLD DEF 9XX:\n' + '\n'.join(['%s - %s - %s' % (item.prefix_start, item.prefix_end, item.operator) for item in old_def_9xx]))
        delete_old_def_9xx(old_def_9xx, db.cursor(), mysql_config.table)
        db.commit()
    else:
        logging.info('Not is old DEF 9xx')
    if new_def_9xx:
        logging.info('NEW DEF 9XX:\n' + '\n'.join(['%s - %s - %s' % (item.prefix_start, item.prefix_end, item.operator.decode('utf-8')) for item in new_def_9xx]))
        insert_new_def_9xx(new_def_9xx, db.cursor(), mysql_config.table)
        db.commit()
    else:
        logging.info('Not is new DEF 9xx')
    db.close()
    logging.info('Stop script')


if __name__ == '__main__':
    sys.exit(main())