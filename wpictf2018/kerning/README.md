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
 
 
 First examination of the main function reveals loading  /usr/share/fonts/TTF/FreeSans.ttf, and then doing an md5sum on it. If this md5sum does not match 22f8930d33f395544eb0034b7de24f41, the process will exit. The challenge description "Made on an arch machine" is somewhat of a hint, as the file matches the one in the official arch repo.  https://www.archlinux.org/packages/extra/any/ttf-freefont/
 
 
 
 We can also see a loop with some calls to various STB_truetype functions. https://github.com/nothings/stb/blob/master/stb_truetype.h
 
 We can guess here that its probably rendering something using FreeSans as a font. That something further appears to be the flag we enter, as it loops through argv[1] as it is calling the STB functions.
 

 
 
 After all of that is done, there is a loop where the rendered text output has vertical slices of it hashed (using the domd5 function). Those hashes are compared to known values in obj.texthashes. If any of the hashes mismatch, it printfs "Wrong\n" and exits. Because these are only vertical slices, the changing a character will not effect the md5sums of (most of) the slices before/to the left of it.
 
 
 ## Getting the flag
 
 TODO
