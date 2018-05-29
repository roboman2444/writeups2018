#! /usr/bin/python2
from pwn import *

curlist = [['WPI{', 0]]

maxscore = 0

while maxscore < 165: ## was origionally just while True, but this check just makes sure the program doesnt run on forever
	#Populate list
	tlist = []
	for j in curlist:
		tlist.append(j)
		for i in range(0, 127):
			tlist.append([j[0]+chr(i), 0])

	#score list
	jlist = []
	for j in tlist:
		if j[1] == 0: #only calculate score if not already calculated
			s = process(["ltrace", "-e", "MD5_Final", "./kerning", j[0]])
			j[1] = s.recvall().count("MD5_Final")
			s.close()
		if maxscore < j[1]: maxscore = j[1]
		jlist.append(j)

	#remove anything that isnt tied with the high score
	curlist = [j for j in jlist if j[1] >= maxscore]
	print(curlist)
