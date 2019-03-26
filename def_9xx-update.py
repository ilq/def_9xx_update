# -*- coding: utf-8 -*-

import sys
import urllib2
import csv

URL_DEF_9XX = 'https://rossvyaz.ru/data/DEF-9xx.csv'
REGION = 'Кировская обл.'

def get_def_9xx(url):
	response = urllib2.urlopen(url)
	def_9xx_csv = csv.reader(response)
	return def_9xx_csv


def parse_def_9xx(def_9xx):
	pass


def get_region(def_9xx_namedtuple, region):
	pass


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
	def_9xx_namedtuple = parse_def_9xx(def_9xx_csv)
	region_def_9xx = get_region(def_9xx_namedtuple, REGION)
	mysql_config = ''
	current_def_9xx = get_current_def_9xx(mysql_config)
	new_def_9xx, old_def_9xx = diff_def_9xx(region_def_9xx, current_def_9xx, ['num1', 'num2'])
	delete_old_def_9xx(old_def_9xx)
	insert_new_def_9xx(new_def_9xx)
	pass


if __name__ == '__main__':
	sys.exit(main())