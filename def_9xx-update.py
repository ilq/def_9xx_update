# -*- coding: utf-8 -*-

import sys
import urllib2
import csv
import json
import MySQLdb
from collections import namedtuple

URL_DEF_9XX = 'https://rossvyaz.ru/data/DEF-9xx.csv'
REGION = 'Кировская обл.'
MYSQL_CONFIG = 'mysql_config.json'

Def_9xx_NamedTuple = namedtuple('Def_9xx_NamedTuple', 'prefix_start prefix_end region')

def get_def_9xx(url):
	response = urllib2.urlopen(url)
	def_9xx_csv = csv.reader(response, delimiter=';')
	return def_9xx_csv


def parse_def_9xx(def_9xx_csv):
	def_9xx_list_namedtuple = []
	for item in def_9xx_csv:
		item_def_9xx_namedtuple = Def_9xx_NamedTuple(
			item[0]+item[1],
			item[0]+item[2],
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


def get_current_def_9xx(mysql_config):
	db = MySQLdb.connect(
			host=mysql_config.server,
			user=mysql_config.user,
			passwd=mysql_config.password,
			db=mysql_config.database,
			use_unicode=True,
			charset="utf8")
	cursor = db.cursor()
	query = "SELECT num1, num2, operator FROM %s where priority < 100;" % mysql_config.table
	cursor.execute(query)
	result = cursor.fetchall()
	db.close()
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
				continue
			else:
				new_items.append(first_item)
	for second_item in second_def_9xx:
		for first_item in first_def_9xx:
			if first_item.prefix_start == second_item.prefix_start and \
			   first_item.prefix_end == second_item.prefix_end:
				continue
			else:
				old_items.append(second_item)
	print new_items
	print '-------'
	print old_items
	return [new_items, old_items]


def delete_old_def_9xx(old_def_9xx):
	pass


def insert_new_def_9xx(new_def_9xx):
	pass


def main():
	def_9xx_csv = get_def_9xx(URL_DEF_9XX)
	def_9xx_list_namedtuple = parse_def_9xx(def_9xx_csv)
	region_def_9xx = get_region(def_9xx_list_namedtuple, REGION)
	filename_mysql_config = MYSQL_CONFIG
	mysql_config = get_mysql_config(filename_mysql_config)
	current_def_9xx = get_current_def_9xx(mysql_config)

	new_def_9xx, old_def_9xx = diff_def_9xx(region_def_9xx, current_def_9xx, ['prefix_start', 'prefix_end'])
	delete_old_def_9xx(old_def_9xx)
	insert_new_def_9xx(new_def_9xx)
	pass


if __name__ == '__main__':
	sys.exit(main())