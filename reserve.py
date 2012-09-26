#!/usr/bin/env python
#coding=utf8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.remote.webdriver as wb
import time
import sys

#global variables
thread_num = 1

url = "https://reserve.apple.com/HK/zh_HK/reserve/iPhone"
default_store = 'R428'
default_product = 'MD297ZP/A'
default_plan = 'unlockedRadioButtonC'
default_quantity = '2'

default_first_name = u'CHAO'
default_last_name = u'LI'
default_id = 'G25192731'

def order(browser, default_email, default_id):
	browser.get(url) # Load page
	# store
	store = browser.find_element_by_id('store')
	store_options = store.find_elements_by_tag_name("option")
	for option in store_options:
		if option.get_attribute("value") == default_store:
			option.click()

	# product
	products = browser.find_elements_by_name('product')
	for p in products:
		if p.get_attribute("value") == default_product:
			p.click()
	#time.sleep(0.2)		# wait for modal cover

	# plan
	plan = browser.find_element_by_id(default_plan)
	while not plan.is_displayed():
		time.sleep(0.2)
	plan.click()
	confirm = browser.find_element_by_id("continueButtonTextC")
	confirm.click()

	# quantity
	quantity = browser.find_element_by_id('quantity')
	quantity_options = quantity.find_elements_by_tag_name("option")
	for option in quantity_options:
		if option.get_attribute("value") == default_quantity:
			option.click()

	# personal info
	firstname = browser.find_element_by_id('firstname')
	firstname.send_keys(default_first_name)

	last_name = browser.find_element_by_id('lastname')
	last_name.send_keys(default_last_name)

	email = browser.find_element_by_id('email')
	email.send_keys(default_email)

	govid = browser.find_element_by_id('govid')
	govid.send_keys(default_id)

	# submit
	submit = browser.find_element_by_xpath('//div[@id="submitButton"]/a')
	submit.click()
	redirect = browser.find_element_by_id('quantity')
	while redirect:
		time.sleep(0.2)
		try:
			redirect = browser.find_element_by_id('quantity')
		except Exception, e:
			break
		

from Queue import Queue
from threading import Lock,Thread,current_thread
class Worker(object):
	"""docstring for Worker"""
	def __init__(self, thread_num, queue):
		self.thread_num = thread_num
		self.queue = queue

	def start(self):
	    for i in range(self.thread_num):
	      t = Thread(target = self.run)
	      t.setDaemon(True)
	      t.start()

	def run(self):
		browser = webdriver.Firefox()	# Get local session of firefox
		count = 0
		while True:
			info = self.queue.get()
			count += 1
			try:
				order(browser, info['email'],info['id_card'])
			except Exception, e:
				print count,' failed ',info['email'], e
				continue
			print count,' ',info['email'], ' ', info['id_card']
			if self.queue.empty():
				break
		browser.close()
		
if __name__ == '__main__':
	queue = Queue()
	emails = open('emails.txt')
	id_cards = open('id_cards.txt')

	email = emails.readline()
	id_card = id_cards.readline()
	while email and id_card:
		info = {'email':email,'id_card':id_card}
		queue.put(info)
		email = emails.readline()
		id_card = id_cards.readline()

	print 'total num = %s' % queue.qsize()
	# start multi-thread
	Worker(thread_num,queue).start()
	queue.join()




