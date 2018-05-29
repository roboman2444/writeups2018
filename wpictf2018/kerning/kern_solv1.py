#! /usr/bin/python2
from pwn import *

curstring = 'WPI{'

while curstring[-1] is not '}':
	top = [0, 0]
	for i in range(0, 127):
		c = chr(i)
		teststring = curstring + c
		s = process(["ltrace", "-e", "MD5_Final", "./kerning", teststring])
		res = s.recvall().count("MD5_Final")
		s.close()

		if res >= top[0]:
			top[0] = res
			top[1] = c
	curstring += top[1]
	print(str(top[0]) + " " + top[1] + " " + curstring)
