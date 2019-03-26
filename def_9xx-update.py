# -*- coding: utf-8 -*-

import sys
import urllib2
import csv
import json
from collections import namedtuple

URL_DEF_9XX = 'https://rossvyaz.ru/data/DEF-9xx.csv'
REGION = 'Кировская обл.'
MYSQL_CONFIG = 'mysql_config.json'

def get_def_9xx(url):
	response = urllib2.urlopen(url)
	def_9xx_csv = csv.reader(response, delimiter=';')
	return def_9xx_csv


def parse_def_9xx(def_9xx_csv):
	Def_9xx_NamedTuple = namedtuple('Def_9xx_NamedTuple', 'prefix start end count operator region')
	def_9xx_list_namedtuple = []
	for item in def_9xx_csv:
		def_9xx_list_namedtuple.append(Def_9xx_NamedTuple._make(item[:6]))
	return def_9xx_list_namedtuple


def get_region(def_9xx_list_namedtuple, region):
	region_def_9xx = []
	for item in def_9xx_list_namedtuple:
		if item.region == region:
			region_def_9xx.append(item)
	return region_def_9xx


def get_mysql_config(filename_mysql_config):
	print filename_mysql_config
	with open(filename_mysql_config) as f:
		return json.loads(f.read())


def get_current_def_9xx(mysql_config):
	pass


def diff_def_9xx(first_def_9xx, second_def_9xx, fields):
	return ['', '']


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
	new_def_9xx, old_def_9xx = diff_def_9xx(region_def_9xx, current_def_9xx, ['num1', 'num2'])
	delete_old_def_9xx(old_def_9xx)
	insert_new_def_9xx(new_def_9xx)
	pass


if __name__ == '__main__':
	sys.exit(main())