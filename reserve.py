#!/usr/bin/env python
#coding=utf8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.remote.webdriver as wb
import time

#global variables
thread_num = 2

url = "https://reserve.apple.com/HK/zh_HK/reserve/iPhone"
default_store = 'R428'
default_product = 'MD297ZP/A'
default_plan = 'unlockedRadioButtonC'
default_quantity = '1'

default_first_name = u'超'
default_last_name = u'王'
default_id = '410482198809215697'

def order(browser, default_email):
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
	time.sleep(3)

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
			email = self.queue.get()
			count += 1
			try:
				order(browser, email)
			except Exception, e:
				print count,' failed ',email
				continue
			print count,' ',email
			if count >= 2000 or self.queue.empty():
				break
		browser.close()
		
if __name__ == '__main__':
	queue = Queue()
	f = open('emails.txt')
	for email in f:
		queue.put(email)
	# start multi-thread
	Worker(thread_num,queue).start()
	queue.join()
