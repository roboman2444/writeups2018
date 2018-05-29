# Kerning - Reversing - 150 Points

## Challenge description:

Made on an arch machine, by awg

"kerning" file from https://drive.google.com/open?id=1Ye5I5yUfuH_-ntAJMnd_ikAdb9DnszOD

## Lookin at it

Looks to be the usual reversing binary. Run the binary with the flag as the argument, and it will either tell you right or wrong.

```bash
~/kerning$ ./kerning
Usage: ./kerning WPI{some_Fl4g-to 7ry}
```
```bash
~/kerning$ ./kerning WPI{YOLOSWAGWHATSINTHEBAG}
Wrong
 ```
 
 
 First examination of the main function reveals loading  /usr/share/fonts/TTF/FreeSans.ttf, and then doing an md5sum on it. If this md5sum does not match 22f8930d33f395544eb0034b7de24f41, the process will exit. 
 
 ![main font md5 check](https://i.imgur.com/eQByKIu.png)
 ![obj.fonthash](https://i.imgur.com/5QAI3iN.png)
 
 The challenge description "Made on an arch machine" is somewhat of a hint, as the file matches the one in the official arch repo.  https://www.archlinux.org/packages/extra/any/ttf-freefont/
 
 
 
 
 We can also see a loop with some calls to various STB_truetype functions. https://github.com/nothings/stb/blob/master/stb_truetype.h
 
 ![stb calls](https://i.imgur.com/Zse4ytF.png)
 
 We can guess here that its probably rendering something using FreeSans as a font. That something further appears to be the flag we enter, as it loops through argv[1] as it is calling the STB functions.
 

 
 
 After all of that is done, there is a loop where the rendered text output has vertical slices of it hashed (using the domd5 function). Those hashes are compared to known values in obj.texthashes. If any of the hashes mismatch, it printfs "Wrong\n" and exits. 
 ![md5 check loop](https://i.imgur.com/KKqnZDE.png)
 
 Because these are only vertical slices, the changing a character will not effect the md5sums of (most of) the slices before/to the left of it. The loop only exits on the first instance of a wrong vertical slice, so we can do something similar to a timing attack on this. (we could also do a timing attack, but thats more effort)
 
 
 ## Getting the flag
 
 We can count the number of times it goes through the loop as an indicator if we got the correct sequence of letters. The loop exits at the first "wrong" vertical slice. A timing attack would work on this, but it is much simpler to use ltrace to count the number of calls to MD5_Final.

```python
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
```



This works for the first few words, but the first character of the third word has a bunch of different possibilities that all result the same score. This is due to the character 'i' fitting entirely within one vertical slice, and requiring both 'i' and the character after it to be correct in order for that vertical slice to work.

![multiple possibilities](https://i.imgur.com/841zzDe.png)





I remade my "bruteforcer" to keep a list of all the attempts that shared the same highscore. This got through that issue and ran perfectly.


```python
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

```

After we let it do its thing for a few minutes, we get the answer.

![Script working](https://i.imgur.com/QKmNaif.png)


WPI{I_majored_in_typography}
